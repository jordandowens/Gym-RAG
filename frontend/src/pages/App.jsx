"use client";

import { useState } from "react";
import ChatWindow from "../components/ChatWindow";
import InputBar from "../components/InputBar";
import sendMessage from "../api/backendClient";
import "../styles/main.css";

export default function App() {
  const [messages, setMessages] = useState([]);

  async function handleSend(userMessage) {
    const newMessages = [...messages, { sender: "user", text: userMessage }];
    setMessages(newMessages);

    const response = await sendMessage(userMessage);

    setMessages([
      ...newMessages,
      { sender: "agent", text: response.response || "No response" }
    ]);
  }

  return (
    <div className="chat-container">
      <ChatWindow messages={messages} />
      <InputBar onSend={handleSend} />
    </div>
  );
}
