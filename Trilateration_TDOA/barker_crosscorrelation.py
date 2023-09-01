barker13 = [1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1, 1, -1]

import wave
import numpy as np

def detect_barker_code(filename, barker_file):
    # Open the WAV file
    with wave.open(filename, 'rb') as wav_file:
        # Get the audio file properties
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

        # Read the audio data from the WAV file
        audio_data = np.frombuffer(wav_file.readframes(num_frames), dtype=np.int16)

    with wave.open(barker_file, 'rb') as wav_file:
        # Get the audio file properties
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

        # Read the audio data from the WAV file
        barker_code = np.frombuffer(wav_file.readframes(num_frames), dtype=np.int16)

    correlation = np.correlate(audio_data, barker_code, mode='same')

    print(len(correlation))
    print(np.argmax(correlation))
    print(np.max(correlation))
    print("////")
    #print(list(np.argwhere(correlation > 30000)))


# Define the Barker code
barker_code_13 = np.array([1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1, 1, -1])

# Specify the WAV file path
wav_file_path = 'C:\\Users\\Jonathan\\Documents\\ecal_test_2022\\Trilateration_TDOA\\barker13_6.wav'
barker_file_path = 'C:\\Users\\Jonathan\\Documents\\ecal_test_2022\\Trilateration_TDOA\\barker_test.wav'
# Detect the presence of Barker code 13 and retrieve its timestamp
detect_barker_code(wav_file_path, barker_file_path)