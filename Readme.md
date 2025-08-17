# 🎭 Polylogue Autogen

An experimental project that demonstrates **multi-agent storytelling with LLMs**. The setup uses **two Docker containers** (frontend + backend) that communicate over a Docker network to transform a simple scene description into a dynamic play.  

---

## 📌 Overview

This project showcases how **agents can create new agents on the fly** to build a collaborative narrative.  

- **Frontend (Docker 1):** React-based UI that allows you to enter a scene description.  
- **Backend (Docker 2):** FastAPI + LLM runtime that processes requests.  

Workflow:  
1. Frontend sends your scene description → Backend.  
2. **Director Agent** interprets the prompt and converts it into a meaningful play.  
3. **Creator Agent** takes the director’s vision and **spawns new agents (characters)** dynamically.  
4. These character agents interact to act out the play.  
5. The final play is sent back to the frontend for visualization.  

The highlight 🚀: **An agent (the creator) has the capability to generate new agents at runtime, enabling open-ended, adaptive storytelling.**

---

## 🛠 Project Architecture

```
+----------------+         +-------------------+
|   Frontend     | <-----> |   Backend LLM     |
| (Docker 1)     |   API   | (Docker 2: FastAPI|
| React + WS     |         |   + Uvicorn)      |
+----------------+         +-------------------+
         |                           |
         | Scene description         |
         |-------------------------->|
         |                           |
         |  Director → Creator → Play|
         |<--------------------------|
         |         Response           |
```

- **Communication:** Over Docker network (`ws://backend:8000/ws/scene`).  
- **Backend Framework:** FastAPI + Uvicorn.  
- **Frontend Framework:** React + WebSocket client.  

---

## 🚀 Getting Started

### 🛠️ Prerequisites

Before you begin, ensure you have:

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose **installed and running**.
- A valid **Gemini API key** for the Assistant. [the API key is free for use]

---

### Clone the Repository
```bash
git clone https://github.com/yourusername/polylogue-autogen.git
cd polylogue-autogen
```

### Setup Enviornment
- Create a ".env" in the root folder with the following configs:
```dotenv
# LLM model identifier (e.g., Gemini Flash)
MODEL=gemini/gemini-2.0-flash-001


# API key for your LLM provider
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

# Google Base URL for using Gemini with OpenAI wrapper
GOOGLE_API_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

### Build and Start Containers
```bash
docker-compose up --build
```

This will start:
- **Frontend** → on [http://localhost:5173](http://localhost:5173)  
- **Backend** → on [http://localhost:8000](http://localhost:8000)  

### Usage
1. Open the frontend in your browser.  
2. Enter a **scene description** (e.g., “A detective interrogates a suspect under dim light”).  
3. The system will:  
   - Ask the **Director Agent** to interpret your description into a structured play.  
   - Use the **Creator Agent** to dynamically generate characters.  
   - Play out the scene with agent dialogue.  

---

## ⚡ Key Features

- 🧠 **LLM-driven agents**: Director & Creator collaborate to build plays.  
- 🎭 **Dynamic agent creation**: Creator Agent can spawn new character agents.  
- 🔌 **Full-stack setup in Docker**: Backend (FastAPI) + Frontend (React).  
- 🌐 **WebSocket communication**: Real-time play generation.  

---

## 🧑‍💻 Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, Websockets, LLM integration  
- **Frontend:** React, WebSockets  
- **Containerization:** Docker & Docker Compose  

---

## 🎯 Future Enhancements

- 🎨 Richer frontend visualization (character avatars, dialogues in bubbles).  
- 🔊 Voice synthesis for characters.  
- 🧩 More agent archetypes (e.g., stage manager, critic).  

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.  
