import wave
import numpy as np
import csv

class Goertzel:
    def __init__(self, sample_rate, target_frequency):
        """Initialize the Goertzel algorithm."""
        self.sample_rate = sample_rate
        self.target_frequency = target_frequency
        self.coeff = 2.0 * np.cos(2.0 * np.pi * self.target_frequency / self.sample_rate)
        self.q1 = 0.0
        self.q2 = 0.0
        
    def magnitude(self, samples):
        """Apply the Goertzel filter to samples."""
        q1, q2 = 0, 0
        for sample in samples:
            q0 = sample + self.coeff * q1 - q2
            q2 = q1
            q1 = q0
        magnitude = np.sqrt(q1**2 + q2**2 - self.coeff * q1 * q2)
        return magnitude
    
    def infinite_magnitude(self, sample):
        """Apply the Goertzel filter to a single sample."""
        q0 = sample + self.coeff * self.q1 - self.q2
        self.q2 = self.q1 * 0.999
        self.q1 = q0 * 0.999
        magnitude = np.sqrt(self.q1**2 + self.q2**2 - self.coeff * self.q1 * self.q2)
        return magnitude

def detect_tone(goertzel, filename):
    """Detect the timestamps when a tone of the target frequency is heard."""
    wf = wave.open(filename, 'rb')
    sample_width = wf.getsampwidth()
    sample_rate = wf.getframerate()
    n_frames = wf.getnframes()
    
    samples = wf.readframes(n_frames)
    samples = np.frombuffer(samples, dtype=np.int16)

    for i in range(0, n_frames, 500):
        timestamp = i / sample_rate
        frame = samples[i:i + 500]
        magnitude = goertzel.magnitude(frame)
        magnitude_500 = goertzel2.magnitude(frame)
        magnitude_1000 = goertzel3.magnitude(frame)
        if magnitude > 1000:
            print(timestamp, magnitude, magnitude/magnitude_500, magnitude/magnitude_1000)
    #timestamps = []
    #frame_size = 1  # Adjust this value as per your requirement
    #column1_data = []
    #column2_data = []
    #list_of_magnitudes = []
    #is_increase = False
    #for i in range(0, n_frames, frame_size):
    #    frame = samples[i:i + frame_size]
    #    magnitude = goertzel.infinite_magnitude(frame[0])
    #    magnitude_bis = goertzel.magnitude(frame[-10:])
    #    timestamp = i / sample_rate
#
    #    print(timestamp, magnitude, magnitude_bis)
    #    list_of_magnitudes.append(magnitude)
    #    if len(list_of_magnitudes) > 10:
    #        mag_5_10 = sum(list_of_magnitudes[-20:-10]) / len(list_of_magnitudes[-20:-10])
    #        mag_0_5 = sum(list_of_magnitudes[-10:]) / len(list_of_magnitudes[-10:])
    #        if mag_0_5 > mag_5_10 and not is_increase and list_of_magnitudes[-10] < list_of_magnitudes[-1]:
    #            is_increase = True
    #        if is_increase and mag_0_5 < mag_5_10:
    #            is_increase = False
    #            print(timestamp)



    print(n_frames/sample_rate)
    wf.close()
    # Zip the data together to pair the elements
    data = zip(column1_data, column2_data)

    # Specify the filename for the CSV file
    csv_filename = 'C:\\Users\\Jonathan\\output.csv'

    # Write the data to the CSV file
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['stamp', 'magnitude'])  # Write the header row
        writer.writerows(data)  # Write the data rows
    return timestamps

# Usage example
filename = 'C:\\Users\\Jonathan\\Documents\\ecal_test_2022\\Trilateration_TDOA\\3080_phone.wav'
target_frequency = 3087  # Frequency to detect (in Hz)

# Initialize the Goertzel algorithm
goertzel = Goertzel(sample_rate=44100, target_frequency=target_frequency)
goertzel2 = Goertzel(sample_rate=44100, target_frequency=500)
goertzel3 = Goertzel(sample_rate=44100, target_frequency=1000)

timestamps = detect_tone(goertzel, filename)
print("Tone detected at timestamps:", timestamps)

