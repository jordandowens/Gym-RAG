import { useState } from "react";

export default function InputBar({ onSend }) {
  const [input, setInput] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", gap: "10px" }}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask the agent something..."
        style={{
          flex: 1,
          padding: "12px",
          borderRadius: "8px",
          border: "1px solid #444",
          background: "#222",
          color: "white"
        }}
      />
      <button
        type="submit"
        style={{
          padding: "12px 20px",
          borderRadius: "8px",
          background: "#4da6ff",
          border: "none",
          cursor: "pointer"
        }}
      >
        Send
      </button>
    </form>
  );
}
