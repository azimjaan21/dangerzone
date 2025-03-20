import cv2
from django.shortcuts import render
import numpy as np
import json
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO
from shapely.geometry import Point, Polygon
import torch

VIDEO_PATH = "./dangerapp/static/data/cam4.mp4"

# ✅ Load the optimized YOLOv8 nano model
model = YOLO("yolov8m.pt")  # Using YOLOv8-nano for faster inference

# ✅ Enable GPU acceleration if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Store polygons
polygons = []

@csrf_exempt
def save_polygons(request):
    """ Save drawn polygons from the frontend and adjust scaling dynamically """
    if request.method == "POST":
        data = json.loads(request.body)
        global polygons

        # Get actual video dimensions
        cap = cv2.VideoCapture(VIDEO_PATH)
        ORIGINAL_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        ORIGINAL_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        # New displayed video size (adjust if needed)
        NEW_WIDTH = 1280  # Change based on actual video display size
        NEW_HEIGHT = 720

        # Compute scale factors dynamically
        scale_x = ORIGINAL_WIDTH / NEW_WIDTH
        scale_y = ORIGINAL_HEIGHT / NEW_HEIGHT

        # Rescale polygon coordinates to match original video
        polygons = [
            Polygon([(p["x"] * scale_x, p["y"] * scale_y) for p in poly])
            for poly in data.get("polygons", [])
        ]

        return JsonResponse({"message": "Polygons saved successfully!"})
    return JsonResponse({"error": "Invalid request"}, status=400)



def get_polygons(request):
    """ Send saved polygons to frontend """
    return JsonResponse({"polygons": [[{"x": p.x, "y": p.y} for p in poly.exterior.coords] for poly in polygons]})


def generate_frames():
    """ Process video frames, run YOLO every 3rd frame, and check for danger zones """

    cap = cv2.VideoCapture(VIDEO_PATH)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)  # ✅ Reduce buffering lag

    # Get original video dimensions
    ORIGINAL_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    ORIGINAL_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # New displayed video size
    NEW_WIDTH = 1280  # Adjust based on your actual display size
    NEW_HEIGHT = 720

    scale_x = NEW_WIDTH / ORIGINAL_WIDTH
    scale_y = NEW_HEIGHT / ORIGINAL_HEIGHT

    frame_count = 0  # Frame counter
    last_results = None  # Store last YOLO detection

    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.resize(frame, (NEW_WIDTH, NEW_HEIGHT))  # ✅ Resize for display
        frame_count += 1

        # ✅ Run YOLO only every 3rd frame
        if frame_count % 3 == 0:
            last_results = model(frame, device=device)  # Run YOLO
        results = last_results if last_results else model(frame, device=device)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
                cls = int(box.cls[0])  # Class ID
                center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2  # Get center of bounding box

                # Scale detection coordinates back to original space
                orig_center_x = center_x * scale_x
                orig_center_y = center_y * scale_y

                if cls == 0:  # Person class
                    point = Point(orig_center_x, orig_center_y)
                    in_danger = any(poly.contains(point) for poly in polygons)

                    color = (0, 0, 255) if in_danger else (0, 255, 0)  # Red if in danger, Green if safe
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.circle(frame, (center_x, center_y), 5, color, -1)
                    cv2.putText(frame, "DANGER!" if in_danger else "SAFE", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def video_feed(request):
    """ Stream video with YOLO detection and danger zone alerts """
    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace; boundary=frame")


def index(request):
    """ Render the main page """
    return render(request, 'dangerapp/index.html')
