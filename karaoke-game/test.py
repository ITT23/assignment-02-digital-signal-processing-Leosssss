import wave
import numpy as np
import matplotlib.pyplot as plt

# 打开WAV文件
wav_file = wave.open("Counting_Song_Chinese_Rhyme_with_Pinyin.wav", "r")

# 读取数据
data = wav_file.readframes(-1)
data = np.fromstring(data, dtype=np.int16)

# 获取音频采样率
framerate = wav_file.getframerate()

# 设置时间轴
time = np.linspace(0, len(data) / framerate, num=len(data))

# 绘制波形图
plt.plot(time, data)
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Waveform")
plt.ylim(-1000, 1000)
plt.show()
