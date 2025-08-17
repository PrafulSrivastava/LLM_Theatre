import { useState, useRef } from "react";
import ReactMarkdown from "react-markdown";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [director, setDirector] = useState("");
  const [scene, setScene] = useState([]);
  const [loading, setLoading] = useState(false);
  const ws = useRef(null);

  const startScene = () => {
    if (ws.current) ws.current.close();
    setLoading(true);

    ws.current = new WebSocket("ws://localhost:8000/ws/scene");

    ws.current.onopen = () => {
      ws.current.send(JSON.stringify({ prompt }));
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Panel Update:", data.content);

        if (data.panel === "director") {
          setDirector(data.content.message);
        } else if (data.panel === "status") {
          console.log("Status Update:", data.message);
        } else if (data.panel === "scene" && Array.isArray(data.content)) {
          const newMessages = data.content.map((msg) => ({
            speaker: msg.speaker || "Unknown",
            content: msg.content || "",
            stage_warning: msg.stage_warning || null,
          }));
          console.log("Scene Update:", newMessages);

          setScene((prevScene) => [...prevScene, ...newMessages]);
          setLoading(false);
        }
      } catch (err) {
        console.error("Error parsing message:", err);
        setLoading(false);
      }
    };

    ws.current.onerror = (err) => {
      console.error("WebSocket error:", err);
      setLoading(false);
    };

    ws.current.onclose = () => console.log("WebSocket connection closed");
  };

  return (
    <div
      style={{
        fontFamily: "Inter, sans-serif",
        width: "100vw",
        height: "100vh",
        padding: "1rem",
        backgroundColor: "#f9fafb",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Header */}
      <h1
        style={{
          textAlign: "center",
          fontSize: "2.5rem",
          marginBottom: "1rem",
          color: "#1f2937",
        }}
      >
        🎭 Play Director Simulator
      </h1>

      {/* Prompt Input */}
      <div style={{ marginBottom: "1rem" }}>
        <h2 style={{ fontSize: "1.25rem", fontWeight: "600", marginBottom: "0.5rem", color: "#374151" }}>
          Enter Scene Prompt
        </h2>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe your scene..."
          style={{
            width: "100%",
            minHeight: "120px",
            padding: "0.75rem",
            fontSize: "1rem",
            borderRadius: "8px",
            border: "1px solid #e5e7eb",
            resize: "vertical",
            backgroundColor: "#1f2937",
            color: "#e5e7eb",
            boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
          }}
        />
        <button
          onClick={startScene}
          disabled={loading}
          style={{
            marginTop: "0.75rem",
            padding: "0.6rem 1.5rem",
            fontSize: "1rem",
            fontWeight: "600",
            cursor: "pointer",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#4f46e5",
            color: "#fff",
            boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
            opacity: loading ? 0.7 : 1,
          }}
        >
          {loading ? "Loading..." : "🚀 Start Scene"}
        </button>
      </div>

      {/* Panels */}
      <div
        style={{
          display: "flex",
          flex: 1,
          gap: "1rem",
          overflow: "hidden",
        }}
      >
        {/* Director Panel */}
        <div
          style={{
            flex: 1,
            padding: "1rem",
            borderRadius: "12px",
            backgroundColor: "#1f2937",
            color: "#e5e7eb",
            overflowY: "auto",
          }}
        >
          <h2 style={{ marginTop: 0, marginBottom: "1rem", fontSize: "1.2rem", fontWeight: "700", color: "#60a5fa" }}>
            🎬 Director’s Vision
          </h2>
          {director ? (
            <ReactMarkdown>{director}</ReactMarkdown>
          ) : (
            <p style={{ color: "#9ca3af" }}>Waiting for director's output...</p>
          )}
        </div>

        {/* Scene Panel */}
        <div
          style={{
            flex: 2,
            padding: "1rem",
            borderRadius: "12px",
            backgroundColor: "#fff",
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "0.5rem",
          }}
        >
          <h2 style={{ marginTop: 0, marginBottom: "0.5rem", fontSize: "1.2rem", fontWeight: "700", color: "#374151" }}>
            🎤 Scene Play
          </h2>
          {scene.length === 0 && <p style={{ color: "#6b7280" }}>Scene will appear here...</p>}
          {scene.map((msg, idx) => (
            <div
              key={idx}
              style={{
                alignSelf: "flex-start",
                padding: "1rem 1.25rem",
                borderRadius: "16px 16px 16px 4px",
                background: msg.stage_warning ? "#fef2f2" : "#e5e7eb",
                color: msg.stage_warning ? "#b91c1c" : "#1f2937",
                boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
                maxWidth: "90%",
                lineHeight: "1.5",
              }}
            >
              <strong>{msg.speaker || "Unknown"}</strong>:{" "}
              <ReactMarkdown>{msg.content}</ReactMarkdown>
              {msg.stage_warning && <span> ⚠️ {msg.stage_warning}</span>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
