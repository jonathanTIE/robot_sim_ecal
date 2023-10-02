import wave
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import time
import struct
#Read the wav file and put it in a list

output_wav_file = "C:\\Users\\Jonathan\\Downloads\\DTMF_noised_hair3.wav"
inted_frames = []
with wave.open(output_wav_file, 'rb') as wav_file:
    # Get basic information.
    nchannels = wav_file.getnchannels()
    sampwidth = wav_file.getsampwidth()
    framerate = wav_file.getframerate()
    nframes = wav_file.getnframes()

    for i in range(nframes):
        frame = wav_file.readframes(1)
        inted_frames.append(struct.unpack('<h', frame)[0])


duration = 0.1
sample_rate = 44100
f = 7500
f_2 = 4987


reference_signal = np.sin(2 * np.pi * np.arange(sample_rate * duration) * f / sample_rate) * 0.5
reference_signal += (np.sin(2 * np.pi * np.arange(sample_rate * duration) * f_2 / sample_rate) * 0.5)

cross_correlation = signal.correlate(inted_frames, reference_signal, mode='same')


#plot filtered frames
print("nframes", nframes)
print(len(cross_correlation))
plt.plot(cross_correlation)
plt.show()
