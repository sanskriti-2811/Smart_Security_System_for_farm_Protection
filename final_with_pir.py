import cv2
import torch
import numpy as np
import os
import RPi.GPIO as GPIO
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib

# PIR sensor pin
pir_pin = 14

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)

path = 'C:/Users/ksans/OneDrive/Desktop/yolov5win11customobj-main/best.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path, force_reload=True)
email_sender = 'nvarshney174@gmail.com'
email_password = 'ykxcjhlaewigcvhp'
email_receiver = 'shailjaagrawal27035@gmail.com'

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
    if GPIO.input(pir_pin):
        # Motion detected by PIR sensor
        if not intruder_detected:
            ret, frame = cap.read()
            frame = cv2.resize(frame, (640, 480))
            results = model(frame)
            frame = np.squeeze(results.render())
            cv2.imshow("Test Window", frame)  # Show image in window

            if len(results.pred) > 0:
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

                cpt += 1  # Increment the counter for image file name

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()