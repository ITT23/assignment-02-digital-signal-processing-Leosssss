import numpy as np
import pyaudio 
import struct 
import matplotlib.pyplot as plt 

# cite from: https://fazals.ddns.net/spectrum-analyser-part-2/ & audio-sample.py
CHUNK_SIZE = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Audio sampling rate (Hz)
p = pyaudio.PyAudio()

'''
# print info about audio devices
# let user select audio device
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

print('select audio device:')
'''
input_device = int(1)

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK_SIZE
)

# set up interactive plot
fig, (ax,ax1) = plt.subplots(2)
fig.set_size_inches(8,10)
x_fft = np.linspace(0, RATE, CHUNK_SIZE)
x = np.arange(0,2*CHUNK_SIZE,2)
line, = ax.plot(x, np.random.rand(CHUNK_SIZE),'r')
line_fft, = ax1.semilogx(x_fft, np.random.rand(CHUNK_SIZE), 'b')
ax.set_ylim(-30000,30000)
ax.ser_xlim = (0,CHUNK_SIZE)
ax.set_title('Audio Input')
ax1.set_xlim(20,RATE/2)
ax1.set_ylim(0,1)
ax1.set_title('Frequency')
fig.show()

# continuously capture and plot audio singal
while True:
    # Read audio data from stream
    data = stream.read(CHUNK_SIZE)
    dataInt = struct.unpack(str(CHUNK_SIZE) + 'h', data)

    line.set_ydata(dataInt)
    # frequency: https://fazals.ddns.net/spectrum-analyser-part-2/
    line_fft.set_ydata(np.abs(np.fft.fft(dataInt))*2/(11000*CHUNK_SIZE)) 
    print(np.abs(np.fft.fft(dataInt))*2/(11000*CHUNK_SIZE))

    # Redraw plot
    fig.canvas.draw()
    fig.canvas.flush_events()