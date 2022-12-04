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
            while True:
                data = stream.read(chunk)
                frames.append(data)
                if BUT_1.is_active:
                    break
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
                comment = str(r.recognize_google(audio2, language = 'en-US'))
                print(comment)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio - Switching to Sphinx")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service - Switching to Sphinx; {0}".format(e))

            os.remove("test1.wav")

            try:
                comment_analysis = requests.get(f"http://3.88.45.53:8000/appForNlp/nlp_result?comentario={comment}&id_pessoa={0}", timeout=5)
            except:
                print("Connection Failed")
                comment_analysis = "CONNECTION_FAILED"

            LED_G.off()
            time.sleep(0.5)
            print("2")

except Exception as e: 
    print(e)
    print("orra")
    audio.terminate()