import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
# python read and play wav file cite from: https://www.cnblogs.com/douzujun/p/10699160.html
# ChatGPT. (2023, Mai 03). How can I display real-time frequency while playing audio? [Response to user question]. Retrieved from https://github.com/openai/gpt-3

CHUNK = 1024*2
# read file data
SOUND = wave.open('hajimi.wav', 'rb')
data = SOUND.readframes(CHUNK)
# create audio player
p = pyaudio.PyAudio()

# get parameters from file
FORMAT = p.get_format_from_width(SOUND.getsampwidth())
CHANNELS = SOUND.getnchannels()
RATE = SOUND.getframerate()

print('FORMAT: {} \nCHANNELS: {} \nRATE: {}'.format(FORMAT, CHANNELS, RATE))

# open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=CHUNK,
                output=True)
# play stream
while len(data) > 0:
    stream.write(data)
    data = SOUND.readframes(CHUNK)
    
    # Convert audio data to numpy array
    data_array = np.frombuffer(data, dtype=np.int16)
    # calculate spectrum
    spectrum = np.fft.fft(data_array)
    freqs = np.fft.fftfreq(data_array.size, 1/RATE)
    # draw plot
    plt.plot(freqs[:len(freqs)//2], np.abs(spectrum)[:len(spectrum)//2])
    plt.show(block=False)
    plt.pause(0.01)
    plt.clf()
