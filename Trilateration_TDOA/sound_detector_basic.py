# source https://stackoverflow.com/questions/4160175/detect-tap-with-pyaudio-from-live-mic

import pyaudio
import struct
import math
import datetime
from scipy import signal
import numpy as np

FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
#RATE = 44100 
RATE = 48000 
INPUT_BLOCK_TIME = 1
FRAMES = 1024

# Filter requirements.
center_freq = 7250
bandwidth = 100

def design_filter(sample_rate, center_freq, bandwidth):
    norm_center_freq = center_freq / (sample_rate / 2)
    norm_bandwidth = bandwidth / (sample_rate / 2)

    # Design the IIR filter coefficients
    b, a = signal.butter(4, [norm_center_freq - norm_bandwidth/2, norm_center_freq + norm_bandwidth/2], btype='band')
    return b,a 

def apply_narrow_band_filter(sig, b,a):
    # Normalize the center frequency and bandwidth
    
    # Apply the filter to the signal
    filtered_signal = signal.lfilter(b, a, sig)
    
    return filtered_signal

# Example usage

b,a = design_filter(RATE, center_freq, bandwidth)

def normalize(block):
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )
    doubles = [x * SHORT_NORMALIZE for x in shorts]
    return doubles

pa = pyaudio.PyAudio()                                 

stream = pa.open(format = FORMAT,                      
         channels = CHANNELS,                          
         rate = RATE,                                  
         input = True,                                 
         frames_per_buffer = FRAMES)   

while True:
    block = stream.read(FRAMES)
    normalized = normalize(block)
    filtered = apply_narrow_band_filter(normalized, b,a )
    if max(filtered) > 0.001:
        print(max(normalized))
        print(max(filtered))

