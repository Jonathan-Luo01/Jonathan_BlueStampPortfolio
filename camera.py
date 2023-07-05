#import libraries
import cv2
import imutils
import time
import numpy as np

class VideoCamera(object):
    #camera constructor
    def __init__(self, flip = False):
        self.vs = cv2.VideoCapture(0) #use cv2's video capture function
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

    def get_video(self):
 	      out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, (int(self.vs.get(3)), int(self.vs.get(4)))) #Create a VideoWriter object
  	    t_end = time.time() + 20
   	    while(time.time() < t_end): #loop for 20 seconds
    	      ret, frame = self.vs.read() #read from camera

  	        if ret == True:
       		      out.write(frame) #Add frame to the video

    	      else:
	 	            break
   	    out.release() #Release VideoWriter
        cv2.destroyAllWindows() #Deallocate data
  
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
