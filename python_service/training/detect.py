from ultralytics import YOLO
import cv2

# 1. Load your trained YOLOv8 model
model_path = "runs/detect/train7/weights/best.pt"
model = YOLO(model_path)

# 2. Load the image you want to test
image_path = "olive_trees_dataset/test/image9.png"
image = cv2.imread(image_path)

# 3. Run inference
results = model.predict(image, conf=0.5)  # confidence threshold 0.5

# # 4. Visualize results
# # results[0].plot() returns an image with boxes drawn
# result_img = results[0].plot()

# 4. Draw only bounding boxes in black & white
for box in results[0].boxes.xyxy:  # xyxy format: [x1, y1, x2, y2]
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), 2)  # white box

# 5. Show the image
cv2.imshow("Olive Trees Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 6. Optional: save the result
output_path = "result1.jpg"
cv2.imwrite(output_path, image)
print(f"Result saved to {output_path}")