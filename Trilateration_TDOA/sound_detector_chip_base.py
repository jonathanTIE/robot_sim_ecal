import numpy as np
import scipy.signal as sps
import pyaudio

# Parameters
sample_rate = 44100  # Adjust based on your Arduino setup
duration = 5.0
chunk_size = 1024  # Adjust buffer size as per your requirement

# Generate the known chirp signal
start_freq = 1000  # Hz
end_freq = 5000  # Hz
chirp_duration = 0.1  # seconds
t = np.linspace(0, chirp_duration, int(sample_rate * chirp_duration), endpoint=False)
chirp = np.sin(2 * np.pi * np.linspace(start_freq, end_freq, int(chirp_duration * sample_rate)) * t)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the microphone stream
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk_size)

# Read and process the audio stream in chunks
recorded_signal = []
try:
    while True:
        data = stream.read(chunk_size)
        samples = np.frombuffer(data, dtype=np.float32)
        recorded_signal.extend(samples)

        if len(recorded_signal) >= len(chirp):
            # Perform cross-correlation between the recorded signal and the known chirp signal
            corr = sps.correlate(recorded_signal, chirp, mode='full')

            # Find the index of the maximum correlation
            max_index = np.argmax(np.abs(corr))

            # Calculate the end timestamp of the chirp signal
            time_delay = max_index / sample_rate
            chirp_end_timestamp = time_delay - chirp_duration

            print("Chirp End Timestamp:", chirp_end_timestamp)
            break

except KeyboardInterrupt:
    print("Recording stopped by user.")

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()
