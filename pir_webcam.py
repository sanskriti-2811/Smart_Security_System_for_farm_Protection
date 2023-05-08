import RPi.GPIO as GPIO
import time
import cv2

# set up GPIO
pirPin = 12


# set up camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def setup():
        GPIO.setmode(GPIO.BOARD)
       
        GPIO.setup(pirPin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                   
def loop():
        while True:
              pirPin_state = GPIO.input(pirPin)
              if pirPin_state == True:
                   print('Motion Detected !')
                   print("Lights  on")        # motion detected
                   ret, frame = cam.read()
                   if ret:
            # save the image
                      filename = time.strftime("%Y-%m-%d_%H-%M-%S.jpg")
                      cv2.imwrite(filename, frame)
                      print("Image saved: {}".format(filename))
                      time.sleep(2) # wait for 2 seconds to avoid multiple captures
#                  time.sleep(0.1) # wait for 0.1 seconds before checking again
                   
            
                   while GPIO.input(pirPin) == True:
                          time.sleep(0.2)
                  
              else:
                  pass

if _name== "main_":
   setup()
          
   loop()