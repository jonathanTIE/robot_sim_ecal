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
cross_correlation = []
for byte in audio_data:
    try:
        if byte == 10: #"\n":
            continue
        if byte == 13: #"\r":
            cross_correlation.append(float(bytes(buffer)))
            buffer = bytearray()
            continue
        buffer.append(byte)
    except ValueError as e:
        buffer = bytearray() #reset buffer to prevent infinite problem
        print(e)

print("nb of samples:", len(cross_correlation))
print("Time taken:", stop_timing - timing)

plt.plot(cross_correlation)
plt.show()