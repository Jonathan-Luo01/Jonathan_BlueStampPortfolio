# Computer Vision Security Camera
Hi! <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="30" height="30" /> I'm Jonathan. My project is the Computer Vision Security Camera. This project uses a Raspberry Pi Zero Wireless and an USB Camera to detect moving objects and alert the user. Python and openCV is used to detect objects in the video feed and when movement is detected, two emails will be sent. The initial email contains a photo of the object, while the next email contains a twenty-second short video. I used the libraries pyaudio, wave, threading, and fmmpeg to sync the audio and video. The user can also choose to view the live video feed of the security camera if the Raspberry Pi and their personal device is connected to the same network.

## Setup

This project uses a USB camera to stream video. Before running the code, make sure to configure the USB camera on your device.

Open the terminal and run

```
sudo raspi-config
```

Select `Interface Options`, then `Camera` and toggle on. Press `Finish` and exit.

To make sure that the USB camera is connected, type `lsusb` into the terminal. You should be able to see the different devices connected to the Pi.

To verify that the camera worked, I used the `guvcview` program. To install it type this into your terminal: 

```
sudo apt-get install guvcview
```

Another alternative is the package `fswebcam` which can be used to take pictures with the camera. To install:

```
sudo apt-get install fswebcam
```

To take a picture, use the command `fswebcam`:

```
fswebcam imagename.jpg
```

## Installing Dependencies

I used the following [tutorial](https://www.hackster.io/hackershack/smart-security-camera-90d7bd#toc-code-6/) from Hackershack and [this download tutorial](http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/) for this project. However, instead of using the Python 2.7 version that they used, I used Python 3.9.2. Though I followed most of the instructions in the tutorial, the Raspberry Pi Zero was unable to work with the latest versions of the software, so I directly ran:

```
pip install opencv-python==4.5.3.56
python -c "import cv2"
```

for openCV and python.


To create a virtual environment to work with Python, run the following commands:

```bash
source ~/.profile
workon cv
```

Remember to also install the dependencies for this project with:

```
pip install -r requirements.txt
```

or directly installing each of the libraries in the file.

## Customization

To get emails when objects are detected, you'll need to make a couple modifications to the `mail.py` file.

Open `mail.py` with Geany, and scroll down to the following section

```
# Email you want to send the update from (only works with gmail)
fromEmail = 'myemail@gmail.com'
fromEmailPassword = 'password1234'

# Email you want to send the update to
toEmail = 'anotheremail@gmail.com'
```
and replace with your own email/credentials. The `mail.py` file logs into a gmail SMTP server and sends an email with an image of the object detected by the security camera. 

Press `ctrl + s` to save.

You can also modify the `main.py` file to change some other properties.

```
email_update_interval = 60 # sends an email only once in this time interval
video_camera = VideoCamera(flip=True) # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("models/upperbody_recognition_model.xml") # an opencv classifier
```
I recommend using the upper body recognition model, but you can also experiment with different object detectors by changing the path `"models/upperbody_recognition_model.xml"` in `object_classifier = cv2.CascadeClassifier("models/upperbody_recognition_model.xml")`.

to a new model in the models directory.

```
facial_recognition_model.xml
fullbody_recognition_model.xml
upperbody_recognition_model.xml
```

## Running the Program

Run the program

```
python main.py
```

You can view a live stream by visiting the ip address of your pi in a browser on the same network. You can find the ip address of your Raspberry Pi by typing `ifconfig` in the terminal and looking for the `inet` address. 

Visit `<raspberrypi_ip>:5000` in your browser to view the stream.

Note: To view the live stream on a different network than your Raspberry Pi, you can use [ngrok](https://ngrok.com/) to expose a local tunnel. Once downloaded, run ngrok with `./ngrok http 5000` and visit one of the generated links in your browser.

Note: The video stream will not start automatically on startup. To start the video stream automatically, you will need to run the program from your `/etc/rc.local` file, which can be done with:

```
sudo nano -w /etc/rc.local
```

-----

File info:

- **models**: This folder contains three XML files used as models for facial recognition, full body recognition, and upper body recognition in the program.

- **static**: This folder contains the style.css file used to style the website that contains the live video feed of the camera.

- **templates**: This folder contains the about.html, code.html, and index.html files that are used for the website with the live video feed. index.html is the main file that displays the video, while code.html and about.html describe my project and its code.

- **camera.py**: This file contains the code for the camera module, and the main class in this file, `VideoCamera()`, has the method `get_object()` for object detection, which returns an image and a boolean showing if an object has been detected or not. I also implemented the `get_video()` method,
 which records a short twenty-second video that will be sent through email.

- **mail.py**: This file contains the code for sending the security update emails. When an object is detected, the `sendEmail()` method is called from `main.py`. `mail.py` creates an email attached with an image displaying the objects that were detected. I also added the functionality to send another email shortly after containing a twenty-second video with audio. `mail.py` uses the library `smtplib` to log into and send an email from the designated gmail account.

- **main.py**: This file initializes the other classes and is run with `python main.py` to start the security camera. This file handles `Flask` and `basicAuth` to set up a server for the live video feed. The method `check_for_objects()` uses `get_object()` to determine if an object was detected, and if an email was already sent in the designated time interval. If an object is detected and enough time has passed, the method calls `record()` from `recorder.py` and `sendEmail()` from `mail.py` to send the emails.

- **mic.py**: This file utilizes the libraries `pyaudio` and `wave` to record audio. The method `get_audio()` starts recording the audio for twenty seconds, and then creates an audio file using `wave`.

- **recorder.py**: This file receives the video and audio threads from `main.py`, and simultaneously records both audio and video at the same time using multithreading in the method `record()`. After the threads have finished, the method uses `ffmpeg` to mux both the audio and video together into a single .avi file. Another method `clean_up_files()` removes the old video and audio files that have already been sent through email. 
