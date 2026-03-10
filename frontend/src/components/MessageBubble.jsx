export default function MessageBubble({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div
      style={{
        textAlign: isUser ? "right" : "left",
        marginBottom: "10px"
      }}
    >
      <span
        style={{
          display: "inline-block",
          padding: "10px",
          borderRadius: "12px",
          background: isUser ? "#4da6ff" : "#333",
          color: isUser ? "black" : "white",
          maxWidth: "70%"
        }}
      >
        {text}
      </span>
    </div>
  );
}
