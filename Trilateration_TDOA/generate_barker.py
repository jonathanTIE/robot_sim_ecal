import wave
import numpy as np

def generate_barker_code(length):
    barker_code = np.array([1])
    while len(barker_code) < length:
        barker_code = np.concatenate((barker_code, -barker_code[::-1]))
    return barker_code[:length]

# Define the Barker code length
barker_code_length = 13

# Generate the Barker code sequence
barker_code = generate_barker_code(barker_code_length)

# Create an array of audio samples
sample_width = 2  # 2 bytes for 16-bit audio
sample_rate = 44100  # sample rate in Hz
duration = 0.1  # duration of the audio in seconds
num_samples = int(sample_rate * duration)
audio_data = np.tile(barker_code, num_samples // barker_code_length + 1)[:num_samples]

# Normalize the audio samples to the appropriate range
audio_data = audio_data * 32767  # 16-bit signed range
print(audio_data)

# Convert the audio samples to the byte format required for the WAV file
audio_bytes = audio_data.astype(np.int16).tobytes()

# Create a WAV file with the Barker code audio
with wave.open('../../barker_code.wav', 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono audio
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(audio_bytes)

print("Barker code 13 saved as 'barker_code.wav'.")
