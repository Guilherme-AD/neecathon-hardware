import speech_recognition as sr
import pyaudio
import wave
from os import path
import os
from gpiozero import LED, Button
import time
import requests
from requests import get

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

#Recognizing
audio_file = path.join(path.dirname(path.realpath(__file__)), "audio_file"+ str(fileDate) +".wav")

r = sr.Recognizer()
with sr.AudioFile(audio_file) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Google Speech Recognition
comment = str("placeholder")

try:
    comment = str(r.recognize_google(audio, language = 'en-US'))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio - Switching to Sphinx")
    try:
        comment = str(r.recognize_sphinx(audio, language = 'en-US'))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e)) 
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    try:
        comment = str(r.recognize_sphinx(audio, language = 'en-US'))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e)) 

#Deleting the audio file
os.remove("audio_file"+ str(fileDate) +".wav")

#Sending to backend
try:
    comment_analysis = requests.get(f"http://3.88.45.53:8000/appForNlp/nlp_result?comentario={comment}&id_pessoa={0}", timeout=5)
except:
    print("Connection Failed")
    comment_analysis = "placeholder"

print(comment_analysis)
print(comment)