import cv2
import os 
import serial
from utils import load_model,preprocess,frame_size
from laser import *

# load camera
cap = cv2.VideoCapture("video.mp4")

# load model 
model_path = r"C:\Users\US593\OneDrive\Desktop\automated-weed-killing-with-camera-guided-atomstack-laser\custom_yolov8\runs\detect\train\weights\last.pt"
model = load_model(model_path)

# laser initial setup
laserInitialSetup()

# laser pyserial connection checkup
print(getResponse())

ret = True 
frame_number = 0

# atomstackLaser dimensions (in mm)
atomstackLaserWidth = 400
atomstackLaserLength = 410

for x in range(atomstackLaserLength):
    for y in range(atomstackLaserWidth):
        if ret: 
            # read frames
            ret,frame = cap.read()
            frame_number += 1

            # frames preprocessing
            frame = preprocess(frame)

            # detection
            detections  = model(frame)   
            detections_ = []
            for detection in detections[0].boxes.data.tolist():
                if detection is not None: 
                    x1, y1, x2, y2, score, class_id = detection
                    if score > 0.65:
                        detections_.append([x1, y1, x2, y2])
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                        cv2.putText(frame,f"Dandelion {score}",(int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # show bboxes on frames
            cv2.imshow('frame',frame)
            if cv2.waitKey(25) & 0xFF == ord('n'):
                break

            # bbox middle condition
            for x_1,y_1,x_2,y_2 in detections_:
                if ((x_1 + x_2)/2 in range((frame_size/2)-10,(frame_size/2)+10)) and ((y_1 + y_2)/2 in range((frame_size/2)-10,(frame_size/2)+10)):
                    print(f"Dandelion found at {x},{y}")
                    laserOn()
                    time.sleep(3)
                    laserOff()
                    print("Dandelion killed")
                    print("----------------------------------------")

            # laser commands
            time.sleep(1)
            laserMove(x,y)
            time.sleep(1)

cap.release()
cv2.destroyAllWindows()

# move laser to x0,y0
laserHome()


