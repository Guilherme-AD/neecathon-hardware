import pyaudio
import wave
from gpiozero import LED, Button
import speech_recognition as sr
from os import path
import time
import os

#GPIO
BUT_1 = Button(27)
LED_R = LED(25)
LED_G = LED(23)
LED_B = LED(24)

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 1024 # 2^12 samples for buffer
record_secs = 3 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

print("init")
frames = []
try:
    while True:
        if(BUT_1.is_active):
            LED_G.on()
            time.sleep(0.5)
            # create pyaudio stream
            stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
            print("recording")
            for ii in range(0,int((samp_rate/chunk)*3)):
                print(ii)
                data = stream.read(chunk, False)
                frames.append(data)
            print("recording2")
            stream.stop_stream()
            stream.close()
            wavefile = wave.open(wav_output_filename,'wb')
            wavefile.setnchannels(chans)
            wavefile.setsampwidth(audio.get_sample_size(form_1))
            wavefile.setframerate(samp_rate)
            wavefile.writeframes(b''.join(frames))
            wavefile.close()

            #Recognizing
            audio_file = path.join(path.dirname(path.realpath(__file__)), "test1.wav")

            r = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio2 = r.record(source)  # read the entire audio file

            # recognize speech using Google Speech Recognition
            comment = str("NOT_RECOGNIZED_BY_ANY")

            try:
                print(str(r.recognize_google(audio2, language = 'en-US')))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio - Switching to Sphinx")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service - Switching to Sphinx; {0}".format(e))

            os.remove("test1.wav")

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