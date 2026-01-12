import { useState } from "react";

export default function ChatBot() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = () => {
    if (!input.trim()) return;

    setMessages([...messages, { text: input, sender: "user" }]);
    setInput("");
  };

  return (
    <div className="tool-card">
      <div className="tool-header">Chat Bot</div>

      {/* Messages area */}
      <div className="tool-body tool-messages">
        {messages.length === 0 ? (
          <p className="tool-placeholder">Messages will appear here</p>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className="chat-message">
              {msg.text}
            </div>
          ))
        )}
      </div>

      {/* Input */}
      <div className="tool-footer">
        <input
          type="text"
          value={input}
          placeholder="Type your question..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
      </div>
    </div>
  );
}
