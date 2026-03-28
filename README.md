# OOlive Tree Detector

Web app for detecting olive trees in aerial images with a React frontend, a Node.js API gateway, and a Python YOLO inference service.

## Architecture

```text
Frontend (React, port 3000)
  -> Backend API (Node, port 5000)
     -> Python Service (FastAPI + YOLO, port 8000)
```

The Python service processes the uploaded image and writes the result into `python_service/uploads/`.
This directory is shared with the backend, so the backend can return a browser-accessible image URL to the frontend.

## Requirements

- Docker Desktop

## Run The App

From the repository root:

```powershell
docker compose up --build
```

Then open:

```text
http://localhost:3000
```

## How It Works

1. The frontend uploads an image to `POST /detect` on the backend.
2. The backend stores the upload temporarily and forwards it to the Python service.
3. The Python service runs YOLO detection, saves the annotated result image, and returns the result path plus detection count.
4. The backend responds with:
   - `count`
   - `image_url`
5. The frontend displays the detected tree count and rendered result image.

## Service Ports

- Frontend: `3000`
- Backend: `5000`
- Python service: `8000`

## Project Structure

```text
frontend/         React app
backend/          Express API gateway
python_service/   FastAPI + YOLO model service
docker-compose.yml
```

## Example Output

Sample result image:

![Detected Olive Trees](python_service/training/result1.jpg)