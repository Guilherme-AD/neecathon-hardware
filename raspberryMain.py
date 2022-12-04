from gpiozero import LED, Button
import speech_recognition as sr
import pyaudio
import wave
from os import path
import os
from gpiozero import LED, Button
import time
from time import sleep
import requests
from requests import get


#GPIO
BUT_1 = Button(27)
LED_R = LED(25)
LED_G = LED(23)
LED_B = LED(24)


#Main loop
while True:
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
    print("recording")
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the audio frames as .wav file
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
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition
    comment = str("NOT_RECOGNIZED_BY_ANY")

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
        print("Could not request results from Google Speech Recognition service - Switching to Sphinx; {0}".format(e))
        try:
            comment = str(r.recognize_sphinx(audio, language = 'en-US'))
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e)) 

    #Sending to backend
    try:
        comment_analysis = requests.get(f"http://3.88.45.53:8000/appForNlp/nlp_result?comentario={comment}&id_pessoa={0}", timeout=5)
    except:
        print("Connection Failed")
        comment_analysis = "CONNECTION_FAILED"

    #Deleting the audio file
    os.remove("test1.wav")

    #Indicator light off
    sleep(2)
    LED_G.off
        