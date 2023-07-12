# import libraries
import pyaudio 
import wave
import threading
import time

class Microphone():

	def __init__(self):

		self.open = True
		self.frames_per_buffer = 1024
		self.channels = 1
		self.input_device_index
		self.rate = 48000
		self.format = pyaudio.paInt16
		self.audio_filename = 'audio.wav'
		self.audio = pyaudio.PyAudio()
		# These parameters are different for each audio device.

		# The following code reveals the parameters of your own device.
  		'''
		for i in range(self.audio.get_device_count()):
			print(self.audio.get_device_info_by_index(i))
		'''

		self.stream = self.audio.open(format=self.format,
						channels = self.channels,
						rate = self.rate,
						input = True,
						input_device_index = self.input_device_index,
						frames_per_buffer = self.frames_per_buffer)
		self.audio_frames = []

	def get_audio(self):
		self.stream.start_stream()
		t_end = time.time() + 20
		while(time.time() < t_end): #loop for 20 seconds
			data = self.stream.read(self.frames_per_buffer, exception_on_overflow = False)
			self.audio_frames.append(data)

		self.stream.stop_stream()

    # create audio file
		waveFile = wave.open(self.audio_filename, 'wb')
		waveFile.setnchannels(self.channels)
		waveFile.setsampwidth(self.audio.get_sample_size(self.format))
		waveFile.setframerate(self.rate)
		waveFile.writeframes(b''.join(self.audio_frames))
		waveFile.close()

	def start(self):
		audio_thread = threading.Thread(target=self.get_audio)
		audio_thread.start()
