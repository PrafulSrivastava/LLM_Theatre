import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from polylogue.app.agents.manager import get_director_vision, create_agents_yaml, run_final_performance

async def scene_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            prompt = data.get("prompt")
            if not prompt:
                continue

            director_output = await get_director_vision(prompt)
            await websocket.send_json({
                "panel": "director",
                "content": {
                    "title": "Director's Vision",
                    "message": director_output
                }
            })

            await create_agents_yaml(director_output)
            await websocket.send_json({"panel": "status", "message": "Agents generated and saved."})

            async for message in run_final_performance(director_output):
                await asyncio.sleep(0.5)
                await websocket.send_json({"panel": "scene", "content": [message]})

    except WebSocketDisconnect:
        print("Client disconnected")