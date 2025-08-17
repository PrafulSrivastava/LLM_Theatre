from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from polylogue.app.websocket_handler import scene_stream

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Agent is running!"}

app.websocket("/ws/scene")(scene_stream)