import cv2
import time
import torch
import numpy as np
path='C:/Users/ksans/OneDrive/Desktop/yolov5win11customobj-main/best.pt'
model = torch.hub.load('ultralytics/yolov5','custom', path ,force_reload=True)
cpt = 0
maxFrames = 30 # if you want 5 frames only.

cap=cv2.VideoCapture(0)

while cpt < maxFrames:
    ret, frame = cap.read()
    frame=cv2.resize(frame,(640,480))
    results=model(frame)
    frame=np.squeeze(results.render())
 
    cv2.imshow("test window", frame) # show image in window
    cv2.imwrite("C:/Users/ksans/OneDrive/Desktop/yolov5win11customobj-main/img/Arduino_%d.jpg" %cpt, frame)
    time.sleep(0.5)
    cpt += 1
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()


