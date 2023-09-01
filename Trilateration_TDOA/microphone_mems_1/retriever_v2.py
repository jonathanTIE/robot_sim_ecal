import serial
import time
import wave
import matplotlib as mpl
import matplotlib.pyplot as plt
import struct

# Serial port configuration
serial_port = "COM4"  # Replace with the actual serial port
baud_rate = 1000000

# Open the serial port
# Read audio data from the serial port
audio_data = []
ser = serial.Serial(serial_port, baud_rate,timeout=0.01)

timing = time.time()
a, b = 0, 0
uncomplete_buffer = bytearray()
total = 0
audio_data = bytearray()
while True:
    try:
        output = ser.read(1024)
        print(ser.in_waiting)
        for i, x in enumerate(output):
            if x == 10: #10 is \n
                audio_data.extend(output[:i])
                a = i
                break
        for i, x in enumerate(output[::-1][:100]):
            uncomplete_buffer = []
            if i == 0 and x == 10:
                break
            if x == 10: #10 is \n
                uncomplete_buffer.extend(output[-i:])
                break
            b = i
        audio_data.extend(output[a:-b]) # remove the uncomplete buffer
        total += 1

        # print(output)


        #sliced = output.split()
        #audio_data.extend(sliced)
    except ValueError or IndexError as e :
        print(e)
    except KeyboardInterrupt:
        break
print(ser.in_waiting)
ser.close()

# decode the data
int_audio = []
mini_buffer = []
sign = 0 #0 is nothing, 43 is +, 45 is -
for x in audio_data:
    #initializing until first + or -
    if sign == 0:
        if x != 43 and x != 45:
            pass
        else:
            sign = x
        continue

    #if sign is + or -
    if x == 43 or x == 45: #43 is +
        #decode mini_buffer from ascii to int
        mini_buffer = [chr(x) for x in mini_buffer]
        mini_buffer = ''.join(mini_buffer)
        try:
            int_audio.append(int(mini_buffer))
        except ValueError as e:
            print(e)
        
        sign = x
        mini_buffer = []
    else:
        mini_buffer.append(x)

print("total", total)
print("time", time.time()-timing)

output_wav_file = "C:\\Users\\Jonathan\\output.wav"
sample_width = 2
sample_rate = 16000 #len(audio_data) / (time.time()-a)
num_channels = 1

bytes_audio = [struct.pack('<h', x) for x in int_audio]
print(len(int_audio))
print(int_audio[:5000])

#save the audio data to a wav file
with wave.open(output_wav_file, 'wb') as wav_file:
    wav_file.setnchannels(num_channels)
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(b''.join(bytes_audio))

print("WAV file saved:", output_wav_file)