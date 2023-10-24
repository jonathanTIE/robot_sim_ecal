import pyaudio
import wave
import asyncio
from time import time, sleep

from __config import SAMPLE_RATE, AMP_WIDTH, CHANNELS, BUFFER

def read_wav(fname: str) -> [int]:
    frames = []
    with wave.open(fname, 'rb') as wav_file:
        # Get basic information.
        nframes = wav_file.getnframes()

        for i in range(0, nframes, BUFFER):
            frame = wav_file.readframes(BUFFER)
            frames.append(frame)
        return frames
    
async def play_sample(stream, frames):
    for frame in frames:
        stream.write(frame)
    print(time())

async def main():
    frames = read_wav("C:/Users/Jonathan/Documents/ecal_test_2022/Trilateration_TDOA/POC_v1/reference_23_10_2023.wav")
    print(frames)


    p = pyaudio.PyAudio()
    stream = p.open(format = AMP_WIDTH,
                channels = CHANNELS,
                rate = SAMPLE_RATE,
                output = True)

    while True:
        await play_sample(stream, frames)
        await asyncio.sleep(0.1)


    stream.close()    
    p.terminate()
    
if __name__ == "__main__":
    asyncio.run(main())