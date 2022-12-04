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

print("init")
try:
    while True:
        if(BUT_1.is_active):
            time.sleep(0.5)
            while True:
                LED_G.on()
                print("RECOGNIZING")

                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)

                # recognize speech using Google Speech Recognition
                try:
                    # for testing purposes, we're just using the default API key
                    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                    # instead of `r.recognize_google(audio)`
                    print(str(r.recognize_google(audio)))
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

                try:
                    comment_analysis = requests.get(f"http://3.88.45.53:8000/appForNlp/nlp_result?comentario={comment}&id_pessoa={0}", timeout=5)
                except:
                    print("Connection Failed")
                    comment_analysis = "CONNECTION_FAILED"

                if BUT_1.is_active:
                    LED_G.off()
                    time.sleep(0.5)
                    print("2")
                    break

except Exception as e: 
    print(e)
    print("orra")