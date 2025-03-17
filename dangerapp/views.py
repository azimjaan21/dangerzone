import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


VIDEO_PATH = "./dangerapp/static/data/cam4.mp4"

# Function to generate video frames
def generate_frames():
    cap = cv2.VideoCapture(VIDEO_PATH)
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video if it ends
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Store polygons in memory (for now)
polygons = []

@csrf_exempt
def save_polygons(request):
    if request.method == "POST":
        data = json.loads(request.body)
        global polygons
        polygons = data.get("polygons", [])
        return JsonResponse({"message": "Polygons saved successfully!"})
    return JsonResponse({"error": "Invalid request"}, status=400)

# New function to send saved polygons to frontend
def get_polygons(request):
    return JsonResponse({"polygons": polygons})

# Video streaming endpoint
def video_feed(request):
    return StreamingHttpResponse(generate_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

# Render the main page
def index(request):
    return render(request, 'dangerapp/index.html')
