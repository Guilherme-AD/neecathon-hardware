import speech_recognition as sr
from gpiozero import LED, Button
from time import sleep

#GPIO
BUT_1 = Button(2)
LED_1 = LED(17)

#Main loop
while True:
    #FACE_RECOGNITION State
    if BUT_1.is_active:
        faceFlag = True
        while not(faceFlag):
            pass
        LED_1.on
        #BUTTON_PRESSED
        if faceFlag and