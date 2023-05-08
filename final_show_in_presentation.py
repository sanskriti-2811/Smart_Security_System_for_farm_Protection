import cv2
import torch
import numpy as np
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib

path = 'C:/Users/ksans/OneDrive/Desktop/yolov5win11customobj-main/best.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path, force_reload=True)
email_sender = 'nvarshney174@gmail.com'
email_password = 'ykxcjhlaewigcvhp'
email_receiver = 'ksanskriti008@gmail.com'

subject = 'Intruder Alert!'
body = 'An intruder has been detected by the security camera.'

em = MIMEMultipart()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.attach(MIMEText(body))

context = ssl.create_default_context()

cap = cv2.VideoCapture(0)
cpt = 0  # Counter for image file name
intruder_detected = False  # Flag to track intruder detection
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    results = model(frame)
    frame = np.squeeze(results.render())
    cv2.imshow("Test Window", frame)  # Show image in window

    if len(results.pred) > 0 and not intruder_detected:
        intruder_detected = True
        cv2.imwrite("C:/Users/ksans/OneDrive/Desktop/yolov5win11customobj-main/img/Arduino_%d.jpg" % cpt, frame)
        img_path = "C:/Users/ksans/OneDrive/Desktop/yolov5win11customobj-main/img/Arduino_%d.jpg" % cpt
        with open(img_path, 'rb') as img_file:
            img_data = img_file.read()

        img = MIMEImage(img_data)
        img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(img_path))
        em.attach(img)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    cpt += 1  # Increment the counter for image file name

cap.release()
cv2.destroyAllWindows()