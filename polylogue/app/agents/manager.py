import yaml
from pathlib import Path
from typing import List, Any, Optional, AsyncGenerator
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from polylogue.app.agents.loader import init_agents, build_agents_from_yaml
from autogen_agentchat.teams import RoundRobinGroupChat
from polylogue.app.config import OUTPUT_DIR

termination = TextMentionTermination("end of scene")

troupe_agents = init_agents()

def safe_parse_yaml(yaml_text: str) -> List[dict]:
    try:
        docs = list(yaml.safe_load_all(yaml_text.strip()))
    except yaml.YAMLError as e:
        print(f"[WARN] YAML parse error: {e}")
        return []
    collected = []
    for doc in docs:
        if isinstance(doc, list):
            collected.extend(doc)
        elif isinstance(doc, dict):
            if {"name", "role", "system_message"}.issubset(doc.keys()):
                collected.append(doc)
            else:
                for v in doc.values():
                    if isinstance(v, list):
                        collected.extend(v)
    return collected

def validate_agents(agent_list: List[dict]) -> List[dict]:
    return [
        a for a in agent_list
        if isinstance(a, dict) and all(k in a for k in ("name", "role", "system_message"))
    ]

def write_agents_list(path: Path, agents_list: List[Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"agents": agents_list}, f, sort_keys=False, default_flow_style=False)

async def get_director_vision(prompt: str) -> Optional[str]:
    
    message = TextMessage(
        content=f"Given the scene: {prompt}, decide the types of agents needed and their personas. Output instructions for the creator agent.",
        source="User"
    )
    response = await troupe_agents["Director"].on_messages([message], cancellation_token=CancellationToken())
    return response.chat_message.content.strip()

async def create_agents_yaml(vision: str) -> Optional[List[dict]]:
    creator = RoundRobinGroupChat(
        [troupe_agents["Creator"]],
        termination_condition=termination,
        max_turns=2
    )
    creator_result = await creator.run(task=f"Create agents in YAML based on this vision:{vision}")

    created_entries = None
    for msg in creator_result.messages:
        parsed = safe_parse_yaml(msg.content or "")
        valid_entries = validate_agents(parsed)
        if valid_entries:
            created_entries = valid_entries
            break

    if not created_entries:
        print("❌ No valid agents created.")
        return None

    for agent in created_entries:
        character_name = agent["name"]
        character_file = OUTPUT_DIR / f"{character_name}.yaml"
        write_agents_list(character_file, [agent])
        print(f"✅ Character saved: {character_file}")

    return created_entries

async def run_final_performance(prompt: str) -> AsyncGenerator[dict, None]:
        stage_manager = [troupe_agents["StageManager"]]

        fresh_agents = []
        for file in (OUTPUT_DIR / "characters").glob("*.yaml"):
            fresh_agents.extend(build_agents_from_yaml(file))

        performance_team = RoundRobinGroupChat(
            stage_manager + fresh_agents,
            termination_condition=termination,
            max_turns=3
        )
        final_result = await performance_team.run(task=prompt)

        for msg in final_result.messages:
            if msg.source.lower() == "user":
                continue
            if len(msg.content) == 0:
                continue
            yield {
                "speaker": msg.source,
                "content": msg.content,
                "stage_warning": getattr(msg, "stage_warning", None)
            }