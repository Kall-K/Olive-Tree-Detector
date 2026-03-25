import json
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--coco_file", type=str, default="python_service/olive_trees_dataset/train/annotations/instances_default.json", help="Path to the COCO JSON file")
parser.add_argument("--labels_file", type=str, default="python_service/olive_trees_dataset/train/labels", help="Path to the labels directory")

args = parser.parse_args()
coco_file = args.coco_file
labels_file = args.labels_file

with open(coco_file) as f:
    coco = json.load(f)

images = {img["id"]: img for img in coco["images"]}

os.makedirs(labels_file, exist_ok=True)

for ann in coco["annotations"]:
    
    img = images[ann["image_id"]]
    w = img["width"]
    h = img["height"]
    
    x, y, bw, bh = ann["bbox"]
    
    x_center = (x + bw/2) / w
    y_center = (y + bh/2) / h
    bw /= w
    bh /= h
    
    label = f"0 {x_center} {y_center} {bw} {bh}\n"
    
    name = img["file_name"].replace(".png", ".txt").replace(".jpeg", ".txt").replace(".jpg", ".txt")

    
    with open(f"{labels_file}/{name}","a") as f:
        f.write(label)