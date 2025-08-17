from pathlib import Path
import yaml
from typing import List
from autogen_agentchat.agents import AssistantAgent
from polylogue.app.agents.tools import build_search_tool
from polylogue.app.config import AGENT_CONFIG_FILE, GEMINI_API_KEY, GOOGLE_API_BASE_URL, MODEL_NAME
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient


# ---------------- Model Client ---------------- #
model_client = OpenAIChatCompletionClient(
    model=MODEL_NAME,
    api_key=GEMINI_API_KEY,
    base_url=GOOGLE_API_BASE_URL,
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": ModelFamily.GEMINI_2_0_FLASH,
        "structured_output": True,
    },
)


TOOLS_MAP = {"internet_search": build_search_tool()}

def build_agents_from_yaml(agent_config_path: Path) -> List[AssistantAgent]:
    if not agent_config_path.exists():
        raise FileNotFoundError(f"YAML file not found: {agent_config_path}")

    with open(agent_config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    agents = []
    for agent_def in config.get("agents", []):
        tools = [TOOLS_MAP[t] for t in agent_def.get("tools", []) if t in TOOLS_MAP]
        name = agent_def["name"]

        agent = AssistantAgent(
            name=name,
            model_client=model_client,
            system_message=agent_def["system_message"],
            tools=tools
        )
        agents.append(agent)
    return agents


def load_troupe(agent_config_file: Path):
    return 

def init_agents():
    if not AGENT_CONFIG_FILE.exists():
        raise FileNotFoundError(f"Agent config file not found: {AGENT_CONFIG_FILE}")
    

    troupe = build_agents_from_yaml(AGENT_CONFIG_FILE)
    stagemanager = next((a for a in troupe if a.name.lower() == "stagemanager"), None)
    if not stagemanager:
        raise ValueError("StageManager agent not found in troupe agents.")
    creator = next((a for a in troupe if a.name.lower() == "creator"), None)
    if not creator:
        raise ValueError("Creator agent not found in troupe agents.")
    director = next((a for a in troupe if a.name.lower() == "director"), None)
    if not director:
        raise ValueError("Director agent not found in troupe agents.")
    return {"StageManager":stagemanager, "Creator":creator, "Director":director}