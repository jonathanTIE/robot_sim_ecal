import wave
import numpy as np
import matplotlib.pyplot as plt

# Create an array of audio samples
sample_width = 2  # 2 bytes for 16-bit audio
sample_rate = 44100  # sample rate in Hz
duration = 0.00084  # duration of the audio in seconds
f = 7500


code = '100001100010100111101000111001001011011101100110101011111100000'
samples = []
for i in range(len(code)):
    t = i / sample_rate 
    cur_code = int(code[i])
    bpsk = np.pi if cur_code == 1 else 0
    #https://homepages.laas.fr/dubuc/Teaching/MODEM_BPSK.pdf
    samples.append(np.sin(2 * np.pi * f * t + bpsk).astype(np.float16))

samples = np.array(samples)
output_bytes = samples.tobytes()
# Convert the audio samples to the byte format required for the WAV file

# Create a WAV file with the Barker code audio
fname = f'../../PN_{f}.wav'
with wave.open(fname, 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono audio
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(output_bytes)

print(f"signal sound PN saved as {fname}.")

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result

print(samples)
plt.plot(autocorr(samples))
plt.show()