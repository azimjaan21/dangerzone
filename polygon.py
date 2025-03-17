import cv2
import numpy as np

import torch
from shapely.geometry import Point, Polygon

from ultralytics import YOLO, solutions
from ultralytics.utils.plotting import Annotator, colors
from collections import defaultdict


drawing = False  # True if mouse is pressed
mode = None  # Can be 'draw', 'move', or 'resize'
start_idx = -1  # Starting index for moving or resizing
move_idx = -1  # Index of the moving vertex
polygon = []  # Current polygon (list of points)
polygons = []  # List of polygons
counting_in_polygons = []
dist_thresh = 10

polygon_ndx = None
point_ndx = None


track_history = defaultdict(list)


def draw_polygon(tmp_img):
    if len(polygons) > 0:
        for poly in polygons:
            cv2.polylines(tmp_img, [np.array(poly)], isClosed=True, color=(0, 0, 255), thickness=2)
        
            for p in poly:
                cv2.circle(tmp_img, p, 6, color=(0, 0, 255), thickness=-1)
                
        
    if len(polygon) > 0:
        for p in polygon:
            cv2.circle(tmp_img, p, 6, color=(255, 0, 0), thickness=-1)
        
        if len(polygon) > 1:
            for i in range(len(polygon)-1):
                cv2.line(tmp_img, polygon[i], polygon[i+1], color=(255, 0, 0), thickness=2)
                
        
def mouse_event(event, x, y, flags, param): 
    global polygon, polygons, polygon_ndx, point_ndx
    
    point = (x, y)
    
    
    tmp_img = img.copy()
    # draw_polygon(tmp_img)
        
    cv2.circle(tmp_img, point, 6, color=(255, 0, 0), thickness=-1)
    
    if event == cv2.EVENT_LBUTTONDOWN:
        
        if polygon_ndx is not None and point_ndx is not None:
            polygon_ndx = None
            point_ndx = None
            
            return
        
        
        if len(polygon) == 0:
            for i, polygon_ in enumerate(polygons):
                for j, point_ in enumerate(polygon_):
                    dist = np.linalg.norm(np.array(point_)-np.array(point))
                    if dist <= dist_thresh:
                        polygon_ndx = i
                        point_ndx = j
                        
                        return
                        
                 
        cv2.circle(tmp_img, point, 6, color=(255, 0,  0), thickness=-1)
        
        if len(polygon) > 2:
            dist = np.linalg.norm(np.array(polygon[0])-np.array(point))
            if dist <= dist_thresh:
                point = polygon[0]
                polygons.append(polygon)
                
                # counting_regions.append({
                #     'name': f'Region: {len(counting_regions)+1}',
                #     'polygon': polygon,
                #     'counts': 0
                # })
                polygon = []
            else:
                polygon.append(point)
        else:
            polygon.append(point)
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if polygon_ndx is not None and point_ndx is not None:
        
            polygons[polygon_ndx][point_ndx] = point
        
        # print(polygon_ndx,point_ndx )
        
    if event == cv2.EVENT_RBUTTONDOWN:
        if polygon_ndx is not None and point_ndx is not None:
            del polygons[polygon_ndx]
            polygon_ndx = None
            point_ndx = None
            
        
        
    cv2.imshow("image", tmp_img)
    
        
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_event)


cap_path = './../data/zone4.mp4'
cap_window = 'Frame with Danger Zone'
cap = cv2.VideoCapture(cap_path)


model = YOLO("./../pts/yolov8m.pt")
model.to("cuda") if torch.cuda.is_available() else model.to("cpu")

names = ['Person']

cap.set(cv2.CAP_PROP_POS_FRAMES, 200)

while True:
    ret, img = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    
    
    counting_in_polygons = [0]*len(polygons)
    img = cv2.resize(img, (800, 600), interpolation = cv2.INTER_AREA)
    
    
    result = model.track(img, persist=True, classes=[0], tracker='./../pts/botsort.yaml',  verbose=False)[0]
    
    
    draw_polygon(img)
    
    
    if result.boxes.id is not None:
        boxes = result.boxes.xyxy.cpu()
        track_ids = result.boxes.id.int().cpu().tolist()
        clss = result.boxes.cls.cpu().tolist()
        
        annotator = Annotator(img, line_width=2, example=str(names))
        
        for box, track_id, cls in zip(boxes, track_ids, clss):
            annotator.box_label(box, f"{str(names[int(cls)])}: {track_id}", color=colors(cls, True))
            
            bbox_center = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2 
            
            # bbox_center = (box[0] + box[2]) / 2, box[3]
             
            
            track = track_history[track_id]
            track.append((float(bbox_center[0]), float(bbox_center[1])))
            if len(track) > 30:
                track.pop(0)
                
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(img, [points], isClosed=False, color=colors(cls, True), thickness=2)
            
            
            for i, polygon_ in enumerate(polygons):
                if Polygon(polygon_).contains(Point((bbox_center[0], bbox_center[1]))):
                    counting_in_polygons[i] += 1
                
    
    
    for i, co in enumerate(counting_in_polygons):
        polygon_ = Polygon(polygons[i])
        
        region_label = f"{co}"
        
        polygon_coordinates = np.array(polygon_.exterior.coords, dtype=np.int32)
        centroid_x, centroid_y = int(polygon_.centroid.x), int(polygon_.centroid.y)
        
        text_size, _ = cv2.getTextSize(region_label, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7, thickness=2)
        text_x = centroid_x - text_size[0] // 2
        text_y = centroid_y + text_size[1] // 2
        
        cv2.putText(img, region_label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    
    
    cv2.imshow("image", img)
    if cv2.waitKey(0) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()