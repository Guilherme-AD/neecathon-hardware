import pyaudio
import wave
from gpiozero import LED, Button
import time

#GPIO
BUT_1 = Button(27)
LED_R = LED(25)
LED_G = LED(23)
LED_B = LED(24)

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 3 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
print("init")
frames = []
try:
    while True:
        if(BUT_1.is_active):
            LED_G.on()
            time.sleep(0.5)
            print("recording")
            for ii in range(0,int((samp_rate/chunk)*1)):
                print(ii)
                data = stream.read(chunk)
                frames.append(data)
            print("recording2")
            while True:
                if(BUT_1.is_active):
                    LED_G.off()
                    time.sleep(0.5)
                    print("2")
                    break
except Exception as e: 
    print(e)
    print("orra")
    audio.terminate()