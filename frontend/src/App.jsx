import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Select image first");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await axios.post("http://127.0.0.1:8000/predict", formData);
      setResult(res.data);
    } catch (err) {
      alert("API error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🫁 PneumoScan AI</h1>
      </header>

      <div className="hero">
        <div className="left">
          <h2>
            The Future of <span>Chest Imaging</span>
          </h2>
          <p>AI-powered pneumonia detection using deep learning.</p>

          <div className="stats">
            <div>95% Accuracy</div>
            <div>Instant Results</div>
          </div>
        </div>

        <img src="lungs_image.png" alt="lungs" />
      </div>

      <div className="upload-box">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Predict</button>

        {loading && <p>Processing...</p>}

        {result && (
          <div className="result">
            <h3>{result.prediction}</h3>
            <p>{(result.confidence * 100).toFixed(2)}%</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;