import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
# python read and play wav file cite from: https://www.cnblogs.com/douzujun/p/10699160.html
# ChatGPT. (2023, Mai 03). How can I display real-time frequency while playing audio? [Response to user question]. Retrieved from https://github.com/openai/gpt-3

CHUNK_SIZE = 1024*3
# read file data
SOUND = wave.open('Counting_Song_Chinese_Rhyme_with_Pinyin.wav', 'rb') #audio from YouTube: https://www.youtube.com/watch?v=o1tC7eJVh2E&ab_channel=LiverpoolCDC
data = SOUND.readframes(-1)
data = np.fromstring(data, dtype=np.int16)

framerate = SOUND.getframerate()

# 设置时间轴
time = np.linspace(0, len(data) / framerate, num=len(data))

plt.plot(time, data)
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Waveform")
plt.ylim(-1000, 1000)
plt.show()

# create audio player
p = pyaudio.PyAudio()

# get input audio data
INPUT_FORMAT = pyaudio.paInt16  # Audio format
INPUT_CHANNELS = 1  # Mono audio
INPUT_RATE = 44100  # Audio sampling rate (Hz)
input_p = pyaudio.PyAudio()

# get parameters from file
FORMAT = p.get_format_from_width(SOUND.getsampwidth())
CHANNELS = SOUND.getnchannels()
RATE = SOUND.getframerate()

# print('FORMAT: {} \nCHANNELS: {} \nRATE: {}'.format(FORMAT, CHANNELS, RATE))

# open sample file stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=CHUNK_SIZE,
                output=True)

# print info about audio devices
# let user select audio device
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

print('select audio device:')
input_device = int(input())

# open audio input stream
input_stream = input_p.open(format=INPUT_FORMAT,
                            channels=INPUT_CHANNELS,
                            rate=INPUT_RATE,
                            input=True,
                            frames_per_buffer=CHUNK_SIZE,
                            input_device_index=input_device)
fig = plt.figure()
ax = plt.gca()
line, = ax.plot(np.zeros(CHUNK_SIZE))

plt.ion()

# play stream
while len(data) > 0:

    # Read audio data from stream
    input_data = input_stream.read(CHUNK_SIZE)

    # Convert audio data to numpy array
    input_data = np.frombuffer(input_data, dtype=np.int16)
    line.set_ydata(input_data)

    stream.write(data)
    data = SOUND.readframes(CHUNK_SIZE)
    

    # Convert audio data to numpy array
    data_array = np.frombuffer(data, dtype=np.int16)
 
    # calculate spectrum
    spectrum = np.fft.fft(data_array)
    freqs = np.fft.fftfreq(data_array.size, 1/RATE)
    # draw plot
    plt.plot(freqs[:len(freqs)//2], np.abs(spectrum)[:len(spectrum)//2], color='green', label='Sample sound')
    plt.ylim(bottom=-20000,top=100000)
    plt.xlim(left=0,right=2000)
    plt.show(block=False)
    plt.pause(0.01)
    plt.clf()
