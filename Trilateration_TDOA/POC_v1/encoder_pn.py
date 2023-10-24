import wave
import struct
import numpy as np
import matplotlib.pyplot as plt
from __config import FREQUENCY, PRBS_SEQ, SAMPLE_RATE, REPETITION, DELAY_SIGNAL

# Create an array of audio samples
sample_width = 2  # 2 bytes for 16-bit audio
samples = []
for i in range(len(PRBS_SEQ)):
    t = i / SAMPLE_RATE 
    cur_code = int(PRBS_SEQ[i])
    bpsk = np.pi if cur_code == 1 else 0
    #https://homepages.laas.fr/dubuc/Teaching/MODEM_BPSK.pdf
    samples.append(np.sin(2 * np.pi * FREQUENCY * t + bpsk).astype(np.float16))

#convert float to int16 (wav file specific)
samples = np.array(samples)
inted_samples = (samples * 32768).astype(np.int16)

if REPETITION > 1:
    delay = (DELAY_SIGNAL / 1000) * SAMPLE_RATE
    signal = inted_samples.copy()
    for x in range(REPETITION):
        #TODO : below method is extremely inneficient due to np array
        inted_samples = np.concatenate((inted_samples, np.zeros(int(delay)).astype(np.int16)))
        inted_samples = np.concatenate((inted_samples, signal))

# Convert the audio samples to the byte format required for the WAV file
output_bytes = struct.pack('<' + ('h'*len(inted_samples)), *inted_samples)

# Create a WAV file with the PN code audio
fname = f'../../PN_{FREQUENCY}.wav'
with wave.open(fname, 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono audio
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(SAMPLE_RATE)
    wav_file.writeframes(output_bytes)

print(f"signal sound PN saved as {fname}.")