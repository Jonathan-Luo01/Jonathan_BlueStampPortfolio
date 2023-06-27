# Computer Vision Security Camera
This project uses a Raspberry Pi Zero Wireless and an USB Camera to detect moving objects and alert the user. Python and openCV is used to detect objects in the video feed and when movement is detected, an email containing an image of the object will be sent. The user can also view the live video feed of the security camera if the Raspberry Pi and their personal device is connected to the same network. 

| **Engineer** | **School** | **Area of Interest** | **Grade** |
|:--:|:--:|:--:|:--:|
| Jonathan L | Monta Vista High School | Computer Science | Incoming Junior

<!--- ![Headstone Image](headshot.png) -->
<!--- ![Project Image](project.jpg) -->
  
<!--- # Final Milestone
<iframe width="560" height="315" src="https://www.youtube.com/embed/F7M7imOVGug" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

My final milestone was to completely assemble the Computer Vision Security Camera by inserting the Raspberry Pi and USB camera inside the casing. In the beginning, I wasn't sure if I wanted to tape or glue the top of the case to the body. Taping it would make it easier to remove, but gluing it to the body would keep it more secure. In the end, I decided to tape the top of the casing to the rest of the case. To keep the USB camera from moving inside the case, I glued the front of the camera to the hole. 

-->

# Second Milestone

<iframe width="560" height="315" src="https://www.youtube.com/embed/UjM6q9UVsvU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
 
My second milestone was creating the casing of the security camera. Using Onshape, I created a 3D model of the exterior casing and added the holes needed to plug in the cables for the camera and the Raspberry Pi. The main difficulty was actually learning how to use CAD to create a 3D model and getting used to the different functions provided by Onshape. I also had to check the dimensions of the casing to make sure that it could be printed out correctly in the first attempt. However, when I printed the casing out, I forgot to account for the mini SD card inserted into the Raspberry Pi, since it added a few more millimeters of length. Since the holes created for each of the cables were too small, I had to sand the holes down with a file. To add on, the hole for the camera's cable was also too small, since I did not account for the width of the USB connector at the end of the cable. To solve this, I learned how to use the drill to create a larger hole in the back of the casing. My next goal is to completely assemble the security camera by adding the Raspberry Pi and USB camera into the casing.


# First Milestone
<iframe width="560" height="315" src="https://www.youtube.com/embed/gXoERpw7gXo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

My first milestone was setting the Raspberry Pi up and installing the necessary programs to run the code. I installed Raspberry Pi Imager and OBS Studio to set up the SD card for the Raspberry Pi and connect the Pi to my laptop. I used openCV to detect objects in the video and send emails with an image of the object boxed in green. In this section of the project, I faced the most challenges when I was first trying to set up the Raspberry Pi. It took around ten hours to install openCV and the necessary libraries needed to actually start programming. The Raspberry Pi Zero was not able to handle the latest versions of the software, and so I had to search for a compatible older version of openCV. Additionally, when I first installed the Raspberry Pi OS on the SD card, it was corrupted, and so I had to reinstall it again. 

Another big problem was the Raspberry Pi's plastic connector, which broke before I could use it. I tried to hot-glue the camera cable to the connector, but the Pi was still unable to detect the Pi Camera module, so I settled for using the USB camera. Since I changed the camera I was using, I had to modify the code to use the USB camera instead of the Pi Camera. Instead of using PiVideoStream, I used the default functions of cv2 for the USB camera. I also need to redesign the outer casing I was using, since the larger USB camera would no longer fit in the previous camera case, and so my next goal is to create a 3D model for the new componenents.

# Schematics 
Camera:

![Schematics](camera_schematic.png) 

Casing:

![Schematics](casing_schematic.png) 

# Code
Main:
```python
# import libraries
import cv2 
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading

email_update_interval = 120 # sends an email only once in this time interval
video_camera = VideoCamera(flip=True) # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("models/fullbody_recognition_model.xml") # an opencv classifier

# App Globals for viewing live video feed
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'DEFAULT_USERNAME' #Change username and password
app.config['BASIC_AUTH_PASSWORD'] = 'DEFAULT_PASSWORD'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0

def check_for_objects():
	global last_epoch
	while True:
		try:
			frame, found_obj = video_camera.get_object(object_classifier)
			if found_obj and (time.time() - last_epoch) > email_update_interval: #check if enough time is elapsed and if object is found
				last_epoch = time.time()
				print("Sending email...")
				sendEmail(frame)
				print("done!")
		except:
			print ("Error sending email: "), sys.exc_info()[0]

#launch basic server 
@app.route('/')
@basic_auth.required 
def index():
    return render_template('index.html')

#return frame
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#Generate video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False) #make it accessible to every device on the network
```
Camera:
```python
#import libraries
import cv2
import imutils
import time
import numpy as np

class VideoCamera(object):
    #camera constructor
    def __init__(self, flip = False):
        self.vs = cv2.VideoCapture(0)
        self.flip = flip
        time.sleep(2.0)

    #delete camera object
    def __del__(self):
        self.vs.stop()

    #flips camera object
    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    #Return a single frame taken by the camera
    def get_frame(self):
        ret, frame = self.vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    #Look for an object and return image
    def get_object(self, classifier):
        found_objects = False
        ret, frame = self.vs.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(objects) > 0:
            found_objects = True

        # Draw a rectangle around the objects
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame) 
        return (jpeg.tobytes(), found_objects)
```
Mail:
```python
#import libraries
import smtplib
from email.mime.Multipart import MIMEMultipart
from email.mime.Text import MIMEText
from email.mime.Image import MIMEImage

# Email you want to send the update from (only works with gmail)
fromEmail = 'email@gmail.com'
# You have to generate an app password since Gmail does not allow less secure apps anymore
# https://support.google.com/accounts/answer/185833?hl=en
fromEmailPassword = 'password'

# Email you want to send the update to
toEmail = 'email2@gmail.com'

def sendEmail(image):
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Security Update'
	msgRoot['From'] = fromEmail
	msgRoot['To'] = toEmail
	msgRoot.preamble = 'Raspberry pi security camera update'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('Smart security cam found object') #add description
	msgAlternative.attach(msgText) 

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)

	msgImage = MIMEImage(image)
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage) #add the image taken

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(fromEmail, fromEmailPassword) #access gmail
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
	smtp.quit()
```

# Bill of Materials

| **Part** | **Note** | **Price** | **Link** |
|:--:|:--:|:--:|:--:|
| Raspberry Pi Zero Wireless | Core of the project | $47.98 | <a href="https://www.amazon.com/Raspberry-Pi-Zero-Wireless-model/dp/B06XFZC3BX"> Link </a> |
|:--:|:--:|:--:|:--:|
| USB Camera | Camera for video/pictures | $13.17 | <a href="https://us.amazon.com/Serounder-Microphone-Megapixel-Computer-Broadcasting/dp/B07P8Z3MSN"> Link </a> |
|:--:|:--:|:--:|:--:|
| Adafruit Raspberry Pi Zero Camera Cable | Needed to replace the cable that comes with the camera module | $8.99 | <a href="https://www.amazon.com/Arducam-Raspberry-Camera-Ribbon-Extension/dp/B085RW9K13"> Link </a> |
|:--:|:--:|:--:|:--:|
| Micro-USB to USB Cable (Generic) | For connection to Raspberry Pi | $2.10 | <a href="https://www.sparkfun.com/products/13244"> Link </a> |
|:--:|:--:|:--:|:--:|
| 4K HDMI Video Capture | Used to connect HDMI cable to laptop | $22.99 | <a href="https://www.amazon.com/Capture-Streaming-Broadcasting-Conference-Teaching/dp/B09FLN63B3"> Link </a> |
|:--:|:--:|:--:|:--:|
| 2.5A Power Supply Bank | Used to connect power to the Pi | $19.95 | <a href="https://www.amazon.com/CanaKit-Raspberry-Supply-Adapter-Listed/dp/B00MARDJZ4"> Link </a> |
|:--:|:--:|:--:|:--:|
| Micro USB OTG Hub | Used to connect more devices to the Pi | $14.99 | <a href="https://www.amazon.com/AuviPal-Adapter-Playstation-Classic-Raspberry/dp/B083WML1XB"> Link </a> |
|:--:|:--:|:--:|:--:|
| Amazon Basics Mini-HDMI to HDMI Adapter Cable | Used to connect to the display | $8.79 | <a href="https://www.amazon.com/AmazonBasics-High-Speed-Mini-HDMI-Adapter-Cable/dp/B014I8UEGY"> Link </a> |
|:--:|:--:|:--:|:--:|
| Micro SD Card | Transfer Raspberry Pi data | $17.09 | <a href="https://www.amazon.com/Amazon-Basics-microSDXC-Memory-Adapter/dp/B08TJRVWV1"> Link </a> |
|:--:|:--:|:--:|:--:|

# Starter Project
<iframe width="560" height="315" src="https://www.youtube.com/embed/WCWzYgzLuSQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

My first project was the Mini Cat Lamp. This project uses a simple circuit which was soldered together to create a mini cat that has an LED on its back that lights up when it becomes dark. In this project, I learned how to properly use tools for soldering and apply what I learned to a real-life creation. I first had to completely assemble the cat body board. I inserted the LED, transistor, resistor, and photoresistor into the cat body board. Then, I proceeded to use the soldering iron to solder each of these parts into the board. At first, I was unfamiliar with soldering, and so the initial soldering was messy, requiring me to clean up the solder left outside the pins. The most important part was the photoresistor, which would limit the electricity flow if light was detected. 

After completing this, I would need to assemble the base of the Mini Cat Lamp. I soldered the battery holder and switch into the base. It was imporant to pay attention to the orientation of each part to prevent soldering them on incorrectly, since desoldering the parts would be tedious. I was surprised at how the soldering iron would also melt the plastic circuit board, and so I tried to minimize the time taken to finish soldering. 

To completely assemble the Mini Cat Lamp, I combined both the cat body circuit board and the base. Soldering the cat's arms to its torso, I inserted the cat body into the gold tabs in the base. I inserted the standoffs needed to keep the base upright into the sides and soldered each part together. Then, I inserted a battery into the bottom of the base. Finally, when the switch was turned on, the Mini Cat Lamp's LED light would turn on when it turned dark. Through this project, I learned how to solder and how an electrical circuit worked.


