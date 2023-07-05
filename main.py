# import libraries
import cv2 
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from mic import Microphone
from recorder import record
from flask_basicauth import BasicAuth
import time
import threading

email_update_interval = 60 # sends an email only once in this time interval
video_camera = VideoCamera(flip=True) # creates a camera object, flip vertically
mic = Microphone()
object_classifier = cv2.CascadeClassifier("models/upperbody_recognition_model.xml") # an opencv classifier

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
        			sendImage(frame) #Send image
        			record(video_camera, mic)
				sendVideo() #Send video
				print("done!")
		except Exception as e:
			print("Error sending email: ", __type(e).__name__, e) #Return exception
			

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
