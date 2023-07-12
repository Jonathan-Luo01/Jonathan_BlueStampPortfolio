# import libraries
import threading
import os
import time
import subprocess

def record(video_camera, mic):

	global video_thread
	global audio_thread

	print('Recording..')
  
	video_thread = video_camera
	audio_thread = mic

	print('Starting threads..')

	audio_thread.start()
	video_thread.start()

	while threading.active_count() > 2:
		time.sleep(1)

	print('Threads finished..')

	frame_counts = video_thread.frame_counts
	elapsed_time = 20
	recorded_fps = frame_counts / elapsed_time

	filename = 'final'

	if abs(recorded_fps - 10) >= 0.01:
		print('Re-encoding..')
		cmd = "ffmpeg -r " + str(recorded_fps) + " -i output.avi -pix_fmt yuv420p -r 6 output2.avi"
		subprocess.call(cmd, shell = True)

		print('Muxing..')
		cmd = "ffmpeg -ac 2 -channel_layout stereo -i audio.wav -i output2.avi -pix_fmt yuv420p  " + filename + ".avi"
		subprocess.call(cmd, shell = True)
	else:
		print('Normal Muxing..')
		cmd = "ffmpeg -ac 2 -channel_layout stereo -i audio.wav -i output.avi -pix_fmt yuv420p " + filename + ".avi"
		subprocess.call(cmd, shell = True)

	print("..")

def clean_up_files():
	filename = 'final'
	local_path = os.getcwd()

	if os.path.exists(str(local_path) + "/audio.wav"):
		os.remove(str(local_path) + "/audio.wav")

	if os.path.exists(str(local_path) + "/output.avi"):
		os.remove(str(local_path) + "/output.avi")

	if os.path.exists(str(local_path) + "/output2.avi"):
		os.remove(str(local_path) + "/output2.avi")

	if os.path.exists(str(local_path) + "/" + filename + ".avi"):
		os.remove(str(local_path) + "/" + filename + ".avi")
