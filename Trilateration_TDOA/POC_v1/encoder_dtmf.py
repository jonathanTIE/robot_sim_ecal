import wave
import numpy as np

# Create an array of audio samples
sample_width = 2  # 2 bytes for 16-bit audio
sample_rate = 44100  # sample rate in Hz
duration = 0.00084  # duration of the audio in seconds
f = 7500
f_2 = 4987

samples = (np.sin(2 * np.pi * np.arange(sample_rate * duration) * f / sample_rate) * 0.5).astype(np.float16)
samples += (np.sin(2 * np.pi * np.arange(sample_rate * duration) * f_2 / sample_rate) * 0.5).astype(np.float16)
output_bytes = samples.tobytes()
# Convert the audio samples to the byte format required for the WAV file

# Create a WAV file with the Barker code audio
fname = f'../../DTMF_{f}_{f_2}.wav'
with wave.open(fname, 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono audio
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(output_bytes)

print(f"signal sound DTM saved as {fname}.")
