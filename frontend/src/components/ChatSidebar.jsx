import { useState } from "react";

export default function ChatSidebar() {
  const [userId, setUserId] = useState("");
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const sendQuery = async () => {
    if (!userId) return;

    setResponse("Loading...");

    const res = await fetch("http://localhost:5000/rag", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        user_id: Number(userId)
      })
    });

    const data = await res.json();
    setResponse(data.answer || "No response");
  };

  const locked = !userId;

  return (
    <div className="chat-container">
      <h2 className="chat-title">AI Coach</h2>

      {/* User ID gate */}
      <input
        className="chat-user-input"
        placeholder="Enter User ID to unlock chat"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />

      {/* If locked, show only this */}
      {locked && (
        <div className="chat-locked">
          <p>Chat is locked</p>
          <p>Enter a User ID above to continue</p>
        </div>
      )}

      {/* If unlocked, show full chat UI */}
      {!locked && (
        <>
          <textarea
            className="chat-input"
            placeholder="Ask something..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <button className="chat-send-btn" onClick={sendQuery}>
            Send
          </button>

          <pre className="chat-response">{response}</pre>
        </>
      )}
    </div>
  );
}
