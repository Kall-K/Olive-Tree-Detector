import numpy as np

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import shutil
import os
import uuid
import cv2

app = FastAPI()

# Allow requests from other containers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
MODEL_PATH = "model/best.pt"

os.makedirs(UPLOAD_DIR, exist_ok=True)

print("Loading YOLO model...")
model = YOLO(MODEL_PATH)
print("Model loaded!")

@app.post("/detect")
async def detect(image: UploadFile = File(...)):

    unique_id = str(uuid.uuid4())

    input_path = os.path.join(UPLOAD_DIR, f"{unique_id}_{image.filename}")
    output_path = os.path.join(UPLOAD_DIR, f"result_{unique_id}_{image.filename}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    img = cv2.imread(input_path)

    if img is None:
        return {"error": "Failed to read image"}

    results = model.predict(img)

    # annotated = results[0].plot()
    for box in results[0].boxes.xyxy:  # xyxy format: [x1, y1, x2, y2]
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)  # white box

    cv2.imwrite(output_path, img)

    return {
        "result_path": output_path,
        "count": len(results[0].boxes)
    }


# Serve result images
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")