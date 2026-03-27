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

    # Save uploaded file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    img = cv2.imread(input_path)
    results = model.predict(img)

    # Save annotated result
    annotated = results[0].plot()

    cv2.imwrite(output_path, annotated)

    # Count detected trees
    tree_count = len(results[0].boxes)

    return {
        "count": tree_count,
        "image_url": f"/uploads/{os.path.basename(output_path)}"
    }


# Serve result images
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")