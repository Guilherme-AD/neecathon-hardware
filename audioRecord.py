import speech_recognition as sr
import pyaudio
import wave
from gpiozero import LED, Button
import time, datetime

#def recordAudio():
#PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024, input_device_index=1)
frames = []

#Recording
try:
    while True:
        data=stream.read(1024)
        frames.append(data)
except KeyboardInterrupt:
    pass

stream.stop_stream()
stream.close()
audio.terminate()

fileDate = time.strftime("%Y%m%d-%H%M%S")
audio_file = wave.open("audio_file"+ str(fileDate) +".wav", "wb")
audio_file.setnchannels(1)
audio_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
audio_file.setframerate(44100)
audio_file.writeframes(b''.join(frames))
audio_file.close()