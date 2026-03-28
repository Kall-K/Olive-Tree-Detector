const express = require("express");
const multer = require("multer");
const axios = require("axios");
const cors = require("cors");
const fs = require("fs");
const FormData = require("form-data");
const path = require("path");

const app = express();
app.use(cors());

const PORT = Number(process.env.PORT || 5000);
const PYTHON_SERVICE_URL =
  process.env.PYTHON_SERVICE_URL || "http://localhost:8000/detect";

// Serve uploaded images
app.use("/uploads", express.static("uploads"));

// Local temp upload folder
const storage = multer.diskStorage({
  destination: "uploads/",
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    cb(null, Date.now() + ext);
  },
});

const upload = multer({ storage });
// const upload = multer({ dest: "uploads/" });

/**
 * POST /detect
 * Receives image → sends to Python → returns result
 */
app.post("/detect", upload.single("image"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }
    console.log("File received:", req.file);// Debug log to check file details
    // Create form data to send to Python
    const formData = new FormData();
    console.log("File exists:", fs.existsSync(req.file.path));// Debug log to confirm file existence before sending to Python
    formData.append("image", fs.createReadStream(req.file.path));
    console.log("Sending to Python...");// Debug log to confirm we're sending the file to Python
    // Send request to Python service
    const response = await axios.post(
      PYTHON_SERVICE_URL,
      formData,
      {
        headers: formData.getHeaders(),
        // maxContentLength: Infinity,
        // maxBodyLength: Infinity,
      }
    );
    console.log("Python response:", response.data);// Debug log to check Python response
    // Delete temp file after sending
    fs.unlinkSync(req.file.path);

    // Python should return processed image path or file
    const resultPath = String(response.data.result_path || "").replace(/\\/g, "/");
    const resultCount = response.data.count;

    // Return URL to frontend
    res.json({
      count: resultCount,
      image_url: `/${resultPath}`,
    });

  } catch (error) {
    console.error("Error:", error.message);
    res.status(500).json({ error: "Detection failed" });
  }
});

app.get("/", (req, res) => {
  res.send("Node.js API Gateway running");
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
