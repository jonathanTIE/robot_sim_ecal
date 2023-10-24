import wave
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import time
import struct
import tdoa

#Read the wav file and put it in a list

output_wav_file = "C:\\Users\\Jonathan\\Downloads\\PN_7500_rec.wav"
input_wav_file = "C:\\Users\\Jonathan\\Downloads\\rec_6.wav"

def read_wav(fname: str) -> [int]:
    frames = []
    with wave.open(fname, 'rb') as wav_file:
        # Get basic information.
        nchannels = wav_file.getnchannels()
        sampwidth = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        nframes = wav_file.getnframes()

        for i in range(nframes):
            frame = wav_file.readframes(1)
            frames.append(struct.unpack('<h', frame)[0])
        return frames

# /32768 -> -1 to 1 or else cross correlation won't work 
reference = (np.array(read_wav(input_wav_file))  / 32768).astype(np.float16)
analyzed = (np.array(read_wav(output_wav_file))  / 32768).astype(np.float16)


def calculate_tdoa(indexs: [int], delay_sample: float, delay_emission: float) -> [float]:
    if len(indexs) != 3:
        raise ValueError("This trilateration algorithm requires three TDOA values.")
    
    timings = [x * delay_sample for x in indexs]
    timings[1] = timings[1] - delay_emission
    timings[2] = timings[2] - (delay_emission * 2)
    
    tdoa1 = timings[1] - timings[0]
    tdoa2 = timings[2] - timings[0]
    tdoa3 = timings[2] - timings[1]

    return [tdoa1, tdoa2, tdoa3]


cross_correlation = np.correlate(reference, analyzed, mode='full')

anal_buff = 205 # 0.01s
threshold = 2500	
peaks_arr = []

min_t_delay = 0.005 #s (close to 0ms)
max_t_delay = 0.025 #s (close to 30 ms <=> 5m distance)
delay_emission = 0.015
expected_signals = 3
sample_rate = 44100
delay_sample = 1/sample_rate
buffer = []
threshold = 2800
t_under_threshold = 0
is_above_threshold = False
max_val = 0
i_max_val = 0
max_i_for_iter = anal_buff * (len(cross_correlation) // anal_buff) # used to simulate continuous treatement & appropriate buffer size

for i in range(0, max_i_for_iter, anal_buff):
    #tempo fix
    last_cross_correlation_i = i+anal_buff
    for x in range(i, last_cross_correlation_i):
        val = cross_correlation[x]
        if val > threshold: #if above threshold
            is_above_threshold = True
            t_under_threshold = 0
            if val > max_val:
                max_val = val
                i_max_val = x

        if is_above_threshold and val < threshold: #if going under the threshold
            t_under_threshold+=1
            if t_under_threshold >= 10: #if confirmed under threshold for "long time"
                is_above_threshold = False
                buffer.append(i_max_val)
                max_val = 0
                t_under_threshold = 0
                if len(buffer) == expected_signals: #if signal found
                    print("buffer", buffer)
                    tdoas = calculate_tdoa(buffer, delay_sample, delay_emission)
                    print("tdoas", tdoas)
                    print("position", tdoa.find_position(tdoas))
                    buffer = []

print(buffer)
#plot filtered frames
print(len(cross_correlation))
plt.plot(cross_correlation)
plt.show()
