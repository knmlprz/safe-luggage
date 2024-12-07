from ultralytics import YOLO
import cv2
import math
import datetime

# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

is_recording = False
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Adjust video codec if needed
out_video = None

# model
model = YOLO("yolo-Weights/yolov8n.pt")

# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

selectedClass = {0:"person", 26:"handbag",28:"suitcase",24:"backpack"}
color2 = (0, 255, 0)
amount_luggage = 0
amount_people = 0

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes
        person_in_boxes = [int(bx.cls[0]) == 0 for bx in boxes]
        for box in boxes:
            confidence = math.ceil((box.conf[0]*100))/100
            cls = int(box.cls[0])
            if cls in selectedClass.keys() and confidence >=0:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                if cls == 0:
                    # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
                else:
                    if True in person_in_boxes:
                        cv2.rectangle(img, (x1, y1), (x2, y2), color2, 3)
                    else:
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

                # confidence
                
                print("Confidence --->",confidence)

                # class name
                print("Class name -->", classNames[cls])

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                
    if is_recording:
        out_video.write(img)
    cv2.imshow('Webcam', img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r'):
        if not is_recording:  # Start recording only if not already recording
            is_recording = True
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Create unique filename
            out_video = cv2.VideoWriter(f"recording_{timestamp}.avi", fourcc, 20.0, (img.shape[1], img.shape[0]))  # Adjust output video settings

    # Stop recording on 's' key press
    elif key == ord('s'):
        if is_recording:  # Stop recording only if currently recording
            is_recording = False
            out_video.release()
            out_video = None
            break


cap.release()
cv2.destroyAllWindows()