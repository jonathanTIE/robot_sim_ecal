import wave
import numpy as np
import matplotlib.pyplot as plt

# Load the WAV file
wav_file_path = 'C:\\Users\\Jonathan\\Documents\\ecal_test_2022\\Trilateration_TDOA\\chirp_hidden_5.wav'
signal_file_path = 'C:\\Users\\Jonathan\\Documents\\ecal_test_2022\\Trilateration_TDOA\\chirp_originalwav'
with wave.open(wav_file_path, 'rb') as wav_file:
    audio_params = wav_file.getparams()
    audio_frames = wav_file.readframes(audio_params.nframes)

    # Convert audio data to numpy array
    audio = np.frombuffer(audio_frames, dtype=np.int16)
    sr = audio_params.framerate

    

# Rest of the code remains the same
# Define the parameters of the chirp signal
chirp_duration = 0.1  # Chirp duration in seconds
chirp_start_freq = 5000  # Chirp start frequency in Hz
chirp_end_freq = 6000  # Chirp end frequency in Hz

# Generate the template chirp signal
t = np.linspace(0, chirp_duration, int(chirp_duration * sr), endpoint=False)
chirp_signal = np.sin(2 * np.pi * (chirp_start_freq * t + (chirp_end_freq - chirp_start_freq) / (2 * chirp_duration) * t**2))

# Perform cross-correlation
corr = np.correlate(audio, chirp_signal, mode='valid')

# Set a threshold to detect chirp occurrences
threshold = 4000
chirp_indices = np.where(corr > threshold)[0]

# Calculate the timestamps of chirp occurrences
timestamps = chirp_indices / (sr * 2)

print(np.max(corr))
print(np.mean(corr))
# Print the timestamps of chirp occurrences
for i, timestamp in enumerate(timestamps):
    print(f'Chirp detected at timestamp: {timestamp:.2f} seconds', corr[chirp_indices[i]])

