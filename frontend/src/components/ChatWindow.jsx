export default function ChatWindow({ messages }) {
  return (
    <div
      style={{
        height: "500px",
        overflowY: "auto",
        padding: "10px",
        border: "1px solid #444",
        borderRadius: "8px",
        marginBottom: "20px"
      }}
    >
      {messages.map((msg, idx) => (
        <div key={idx} style={{ marginBottom: "12px" }}>
          <strong style={{ color: msg.sender === "user" ? "#4da6ff" : "#7dff7d" }}>
            {msg.sender === "user" ? "You" : "Agent"}
          </strong>
          <p style={{ margin: "4px 0" }}>{msg.text}</p>
        </div>
      ))}
    </div>
  );
}
