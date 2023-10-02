import wave
import numpy as np
import matplotlib.pyplot as plt
import struct
import time

#Read the wav file and put it in a list

output_wav_file = "C:\\Users\\Jonathan\\output2.wav"
with wave.open(output_wav_file, 'rb') as wav_file:
    # Get basic information.
    nchannels = wav_file.getnchannels()
    sampwidth = wav_file.getsampwidth()
    framerate = wav_file.getframerate()
    nframes = wav_file.getnframes()
    # Read data.
    frames = wav_file.readframes(nframes)

with wave.open("C:\\Users\\Jonathan\\pure_4000.wav", 'rb') as wav_file:
    # Get basic information.
    pure_nchannels = wav_file.getnchannels()
    pure_sampwidth = wav_file.getsampwidth()
    pure_framerate = wav_file.getframerate()
    pure_nframes = wav_file.getnframes()
    # Read data.
    pure_frames = wav_file.readframes(nframes)
#Conversions

# -----FILTERING ----
filtered_frames = []
inted_frames = []
for i in range(0, nframes * 2, 2):
    inted_frames.append( int.from_bytes(frames[i:i+2], 'little', signed=True))



duration = 0.001
sampling_rate = 44100
frequency = 4000
#perform cross correlation to find a 11025 Hz signal
t_ref = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
reference_signal = np.sin(2 * np.pi * frequency * t_ref)

a = time.time()
cross_correlation = np.correlate(inted_frames, reference_signal, mode='full')
print(time.time() - a)

plt.plot(cross_correlation)
plt.show()
