import { useState } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!inputText) return;

    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: 'User', text: inputText },
    ]);

    setInputText('');
    setIsLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/generate?input_text=${inputText}`);
      const data = await response.json();

      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'Model', text: data.response },
      ]);
    } catch (error) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'Model', text: 'An error occurred. Please try again.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Therapy Chatbot</h1>
      <div className="chat-box">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.sender === 'User' ? 'user' : 'model'}`}
          >
            <strong>{message.sender}: </strong>{message.text}
          </div>
        ))}
        {isLoading && <div className="message loading">Model is thinking...</div>}
      </div>
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type your message..."
          required
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default App;
