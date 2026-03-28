import React, { useState } from "react";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const [resultCount, setResultCount] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setResultImage(null);
    setResultCount(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select an image first");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/detect`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Detection failed");
      }

      setResultImage(`${API_BASE_URL}${data.image_url}`);
      setResultCount(data.count);
    } catch (error) {
      console.error(error);
      alert(error.message || "Upload failed");
    }

    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Olive Tree Detector 🌿</h1>

      <input type="file" onChange={handleFileChange} />
      <br /><br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Upload & Detect"}
      </button>

      <br /><br />

      {resultImage && (
        <div>
          <h3>Result:</h3>
          <p>Number of detected trees: {resultCount}</p>
          <p>Detected olive trees are highlighted in the image below:</p>
          <img
            src={resultImage}
            alt="result"
            style={{ width: "500px", border: "2px solid black" }}
          />
        </div>
      )}
    </div>
  );
}

export default App;
