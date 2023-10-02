import wave
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
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

#Conversions
duration = 0.001
sampling_rate = 44100
frequency = 4000
#FFT LENGTH
fft_length = 32 #sampling_rate * duration
#perform cross correlation to find a 4000 Hz signal
t_ref = np.linspace(0, duration, int(32), endpoint=False)
reference_signal = np.sin(2 * np.pi * frequency * t_ref)

#apply the filter to data buffered in frames
filtered_frames = []
inted_frames = []
for i in range(0, nframes * 2, 2):
    inted_frames.append( int.from_bytes(frames[i:i+2], 'little', signed=True))

a = time.time()
cross_correlation = signal.fftconvolve(inted_frames, np.flip(reference_signal), mode='full')
print(time.time() - a)
# ---- threshold detection ---

threshold = 150
is_above_threshold = False
for i, frame in enumerate(cross_correlation):
    if is_above_threshold and frame < threshold:
        is_above_threshold = False
    if frame > threshold:
        is_above_threshold = True

#plot filtered frames
print("nframes", nframes)
print(len(cross_correlation))
plt.plot(cross_correlation)
plt.show()
