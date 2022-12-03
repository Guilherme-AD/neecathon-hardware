import speech_recognition as sr
import pyaudio
from gpiozero import LED, Button
from time import sleep

#GPIO
BUT_1 = Button(2)
LED_1 = LED(17)

#PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
frames = []

#Main loop
while True:
    #FACE_RECOGNITION State
    if BUT_1.is_active:
        faceFlag = True
        while not(faceFlag):
            pass
        LED_1.on
        #BUTTON_PRESSED
        while not(BUT_1.is_active and faceFlag):
            pass
        