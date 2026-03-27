import os, shutil

from ultralytics import YOLO

if __name__ == '__main__':

    model = YOLO("yolov8n.pt")

    results = model.train(
        data="config.yaml",
        epochs=100,
        imgsz=640,
        batch=2,
        device=0,
        project="runs/train",
        name="yolov8n_custom",
    )

    exported_path = model.export(format="onnx")

    target_dir = os.path.join("..", "model")
    target_path = os.path.join(target_dir, os.path.basename(exported_path))
    os.makedirs(target_dir, exist_ok=True)
    shutil.move(exported_path, target_path)

    print(f"Saved to: {os.path.abspath(target_path)}")
