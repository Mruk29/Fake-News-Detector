import { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [newsText, setNewsText] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCheckNews = async () => {
    if (!newsText.trim()) {
      alert("Please enter news text");
      return;
    }

    setLoading(true);
    setResult("");

    try {
      const response = await axios.post("http://127.0.0.1:8080/api/predict", {
        text: newsText,
      });

      setResult(response.data.result); // "Fake" or "Real"
    } catch (error) {
      console.error("Error during prediction:", error);
      setResult("Error occurred");
    }

    setLoading(false);
  };

  return (
    <div className="app-container">
      <h1>📰 Fake News Detector</h1>

      <textarea
        rows="10"
        cols="80"
        placeholder="Paste news article or text here..."
        value={newsText}
        onChange={(e) => setNewsText(e.target.value)}
        className="news-input"
      ></textarea>

      <br />

      <button onClick={handleCheckNews} className="check-button" disabled={loading}>
        {loading ? "Checking..." : "Check if Fake"}
      </button>

      {result && (
        <div className={`result ${result.toLowerCase()}`}>
          <strong>Result:</strong> {result}
        </div>
      )}
    </div>
  );
}

export default App;
