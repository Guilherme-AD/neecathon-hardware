import pyaudio
import wave
from gpiozero import LED, Button
import speech_recognition as sr
from os import path
import time
import os
import requests

#GPIO
BUT_1 = Button(27)
LED_R = LED(25)
LED_G = LED(23)
LED_B = LED(24)

r = sr.Recognizer()
m = sr.Microphone()

print("init")
while True:
    if(BUT_1.is_active):
        LED_G.on()
        time.sleep(0.5)

        with m as source: audioSrc = r.listen(source)
    
        # recognize speech using Google Speech Recognition
        comment = str("NOT_RECOGNIZED_BY_ANY")

        try:
            comment = str(r.recognize_google(audioSrc, language = 'pt-BR'))
            print(comment)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        os.remove("audio.wav")

        try:
            comment_analysis = requests.get(f"http://3.88.45.53:8000/appForNlp/nlp_result?comentario={comment}&id_pessoa={0}", timeout=5)
        except:
            print("Connection Failed")
            comment_analysis = "CONNECTION_FAILED"

        LED_G.off()
        time.sleep(0.5)
        print("2")