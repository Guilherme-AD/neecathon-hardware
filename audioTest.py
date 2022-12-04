import pyaudio

#PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024, input_device_index=0)
frames = []

#Recording
data=stream.read(1024)
frames.append(data)

stream.stop_stream()
stream.close()
audio.terminate()