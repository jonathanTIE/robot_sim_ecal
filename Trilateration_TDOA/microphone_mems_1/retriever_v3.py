import serial
import time
import wave
import matplotlib as mpl
import matplotlib.pyplot as plt
import struct
import soundfile as sf

# Serial port configuration
serial_port = "COM4"  # Replace with the actual serial port
baud_rate = 1000000

# Open the serial port
# Read audio data from the serial port
audio_data = []
ser = serial.Serial(serial_port, baud_rate,timeout=0.01)

timing = time.time()
total = 0

audio_data = bytearray()

while True:
    try:
        output = ser.read(1024)
        audio_data.extend(output)
        if ser.in_waiting >= 1000:
            print(ser.in_waiting)
    except ValueError or IndexError as e :
        print(e)
    except KeyboardInterrupt:
        break

stop_timing = time.time()
ser.close()

buffer = bytearray()
bytes_data = []
int_data = []
for byte in audio_data:
    if byte == 10: #"\n":
        continue
    if byte == 43 or byte == 45:
        try:
            sound_data = int(bytes(buffer)) * 10 # amplify the sound
            int_data.append(sound_data)
            bytes_data.append(struct.pack('<i', sound_data))
        except ValueError as e:
            print(e)
        buffer = bytearray()
    buffer.append(byte)



output_wav_file = "C:\\Users\\Jonathan\\output.wav"
sample_width = 3
sample_rate = 12000 #len(audio_data) / (time.time()-a)
num_channels = 1

sf.write(output_wav_file, int_data, sample_rate, subtype='PCM_24')
#with wave.open(output_wav_file, 'wb') as wav_file:
#    wav_file.setnchannels(num_channels)
#    wav_file.setsampwidth(sample_width)
#    wav_file.setframerate(sample_rate)
#    wav_file.writeframes(b''.join(bytes_data))

print('calculated sample rate', len(int_data) / (stop_timing-timing))
print("WAV file saved:", output_wav_file)