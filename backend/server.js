const express = require("express");
const multer = require("multer");
const axios = require("axios");
const cors = require("cors");
const fs = require("fs");
const FormData = require("form-data");
const path = require("path");

const app = express();
app.use(cors());

// Docker service name (IMPORTANT)
const PYTHON_SERVICE_URL = "http://python_service:8000/detect";

// Local temp upload folder
const upload = multer({ dest: "uploads/" });

/**
 * POST /detect
 * Receives image → sends to Python → returns result
 */
app.post("/detect", upload.single("image"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    // Create form data to send to Python
    const formData = new FormData();
    formData.append("image", fs.createReadStream(req.file.path));

    // Send request to Python service
    const response = await axios.post(
      PYTHON_SERVICE_URL,
      formData,
      {
        headers: formData.getHeaders(),
        maxContentLength: Infinity,
        maxBodyLength: Infinity,
      }
    );

    // Delete temp file after sending
    fs.unlinkSync(req.file.path);

    // Return Python response to frontend
    res.json(response.data);

  } catch (error) {
    console.error("Error:", error.message);
    res.status(500).json({ error: "Detection failed" });
  }
});

app.get("/", (req, res) => {
  res.send("Node.js API Gateway running");
});

app.listen(5000, () => {
  console.log("Server running on port 5000");
});