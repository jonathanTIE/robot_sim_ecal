import wave
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import time
import struct
import tdoa
#Read the wav file and put it in a list

output_wav_file = "C:\\Users\\Jonathan\\Downloads\\DTMF_POS_1.wav"
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

def calculate_tdoa(timings: [int], delay_sample: float) -> [float]:
    if len(timings) != 3:
        raise ValueError("This trilateration algorithm requires three TDOA values.")
    tdoa1 = (timings[1] - timings[0]) * delay_sample
    tdoa2 = (timings[2] - timings[0]) * delay_sample
    tdoa3 = (timings[2] - timings[1]) * delay_sample
    return [tdoa1, tdoa2, tdoa3]

duration = 0.00084
sample_rate = 44100
f = 7500
f_2 = 4987


reference_signal = np.sin(2 * np.pi * np.arange(sample_rate * duration) * f / sample_rate) * 0.5
reference_signal += (np.sin(2 * np.pi * np.arange(sample_rate * duration) * f_2 / sample_rate) * 0.5)

cross_correlation = signal.correlate(inted_frames, reference_signal, mode='same')

anal_buff = 205 # 0.01s
threshold = 2500	
peaks_arr = []

min_t_delay = 0.005 #s (close to 0ms)
max_t_delay = 0.025 #s (close to 30 ms <=> 5m distance)
delay_emission = 0.015
expected_signals = 3
delay_sample = 1/sample_rate
buffer = []
for i in range(0, len(cross_correlation), anal_buff):
    peak_i = i + np.argmax(cross_correlation[i:i+anal_buff])
    if cross_correlation[peak_i] > 2800:
        peaks_arr.append(peak_i)
        buffer.append(peak_i)
        if len(buffer) == expected_signals:
            print(buffer)
            buffer[1] = buffer[1] - delay_emission
            buffer[2] = buffer[2] - (delay_emission * 2)
            print(buffer)
            tdoas = calculate_tdoa(buffer, delay_sample)
            print(tdoas)
            print("position", tdoa.find_position(tdoas))




#plot filtered frames
print("nframes", nframes)
print(len(cross_correlation))
plt.plot(cross_correlation)
plt.show()
