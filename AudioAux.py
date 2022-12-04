import pyaudio
import wave
from gpiozero import LED, Button

#GPIO
BUT_1 = Button(27)
LED_R = LED(25)
LED_G = LED(23)
LED_B = LED(24)

while True:
    if(BUT_1.is_active):
        LED_G.on()
    while True:
        if(BUT_1.is_active):
            LED_G.off()