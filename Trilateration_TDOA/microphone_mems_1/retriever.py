import serial
import wave
import struct
import time

# Serial port configuration
serial_port = "COM4"  # Replace with the actual serial port
baud_rate = 1000000

# WAV file configuration
output_wav_file = "C:\\Users\\Jonathan\\output.wav"
sample_width = 2
sample_rate = 44100
num_channels = 1

# Open the serial port
ser = serial.Serial(serial_port, baud_rate,timeout=0.001)

# Read audio data from the serial port
audio_data = []
a = time.time()
while True:
    try:
        buffer = bytearray(1024)
        bytes_read = ser.readinto(buffer)
        #output = ser.read(64)
        # make a bytes array of the output and split with \n
        bytes_array = buffer.split(b'\r\n')
        audio_data.extend([int(x) for x in bytes_array if x != b'' and x != b'-'])
        
    except ValueError as e:
        print(e)
    except KeyboardInterrupt:
        break

ser.close()

print(len(audio_data))
print(time.time() - a)
print(audio_data)
# Convert the list of integers to bytes with appropriate width
bytes_data = b''.join(struct.pack('<h', sample) for sample in audio_data)
sample_rate = int(len(audio_data) / (time.time() - a))
print("sample_rate:", sample_rate)
# Save audio data as a WAV file
with wave.open(output_wav_file, 'wb') as wav_file:
    wav_file.setnchannels(num_channels)
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(bytes_data)

print("WAV file saved:", output_wav_file)