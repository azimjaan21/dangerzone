import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render


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

# Video streaming endpoint
def video_feed(request):
    return StreamingHttpResponse(generate_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

# Render the main page
def index(request):
    return render(request, 'dangerapp/index.html')
