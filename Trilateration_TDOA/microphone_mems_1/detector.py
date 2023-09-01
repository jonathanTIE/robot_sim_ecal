import wave
import numpy as np
import matplotlib.pyplot as plt
import struct

#Read the wav file and put it in a list

output_wav_file = "C:\\Users\\Jonathan\\output.wav"
with wave.open(output_wav_file, 'rb') as wav_file:
    # Get basic information.
    nchannels = wav_file.getnchannels()
    sampwidth = wav_file.getsampwidth()
    framerate = wav_file.getframerate()
    nframes = wav_file.getnframes()
    # Read data.
    frames = wav_file.readframes(nframes)

#Conversions

# -----FILTERING ----
bandpass_coeffs = (
    -0.000000386445025700,
    -0.000000119790027224,
    0.000000904795499723,
    0.000000273080771463,
    -0.000001685312444765,
    -0.000000500695963247,
    0.000002924996196051,
    0.000000851058165465,
    -0.000004880552445069,
    -0.000001383364938863,
    0.000007891246439399,
    0.000002171183264035,
    -0.000012407942728373,
    -0.000003306499673693,
    0.000019030044010883,
    0.000004904321339323,
    -0.000028552885153841,
    -0.000007108022311094,
    0.000042029540710880,
    0.000010095799092381,
    -0.000060853423256879,
    -0.000014088899670609,
    0.000086872423370700,
    0.000019362843648965,
    -0.000122553740286485,
    -0.000026263936677840,
    0.000171235965007749,
    0.000035235682946187,
    -0.000237544812603212,
    -0.000046865076934451,
    0.000328152531648517,
    0.000061973021567057,
    -0.000453382011851378,
    -0.000081818028635418,
    0.000631437538685595,
    0.000108663704813296,
    -0.000904819192907702,
    -0.000148069313580578,
    0.001506307893056674,
    0.000257813386579321,
    -0.001621991571330602,
    -0.000244521924215183,
    0.001939543065642985,
    0.000277543162693416,
    -0.002407289799796463,
    -0.000322198799141464,
    0.002980937178549668,
    0.000370591304033209,
    -0.003637150200102608,
    -0.000418168523454366,
    0.004357715931591122,
    0.000461531732466652,
    -0.005125861934465360,
    -0.000497946981374157,
    0.005925138306408388,
    0.000525208889753265,
    -0.006739106074128238,
    -0.000541607356785277,
    0.007551347176033400,
    0.000545927908701219,
    -0.008345623247453585,
    -0.000537461710460334,
    0.009106108216974280,
    0.000516016974422953,
    -0.009817656032134244,
    -0.000481932192308432,
    0.010466080196899038,
    0.000436102189496024,
    -0.011038429115771978,
    -0.000380053154702274,
    0.011523245187550095,
    0.000316188258638512,
    -0.011910798062211628,
    -0.000248714861007238,
    0.012193284286697643,
    0.000188485709608345,
    -0.012364987093378393,
    -0.000216683652712459,
    0.012151291002151877,
    -0.000216683652712489,
    -0.012364987093379892,
    0.000188485709608346,
    0.012193284286697371,
    -0.000248714861007244,
    -0.011910798062212116,
    0.000316188258638520,
    0.011523245187550161,
    -0.000380053154702279,
    -0.011038429115772241,
    0.000436102189496022,
    0.010466080196898941,
    -0.000481932192308438,
    -0.009817656032134393,
    0.000516016974422955,
    0.009106108216974275,
    -0.000537461710460335,
    -0.008345623247453672,
    0.000545927908701219,
    0.007551347176033348,
    -0.000541607356785279,
    -0.006739106074128278,
    0.000525208889753269,
    0.005925138306408369,
    -0.000497946981374159,
    -0.005125861934465387,
    0.000461531732466654,
    0.004357715931591096,
    -0.000418168523454368,
    -0.003637150200102614,
    0.000370591304033209,
    0.002980937178549654,
    -0.000322198799141461,
    -0.002407289799796474,
    0.000277543162693412,
    0.001939543065642980,
    -0.000244521924215188,
    -0.001621991571330602,
    0.000257813386579321,
    0.001506307893056673,
    -0.000148069313580579,
    -0.000904819192907701,
    0.000108663704813295,
    0.000631437538685585,
    -0.000081818028635415,
    -0.000453382011851371,
    0.000061973021567057,
    0.000328152531648519,
    -0.000046865076934455,
    -0.000237544812603211,
    0.000035235682946186,
    0.000171235965007750,
    -0.000026263936677842,
    -0.000122553740286486,
    0.000019362843648966,
    0.000086872423370701,
    -0.000014088899670608,
    -0.000060853423256877,
    0.000010095799092379,
    0.000042029540710874,
    -0.000007108022311091,
    -0.000028552885153840,
    0.000004904321339321,
    0.000019030044010894,
    -0.000003306499673685,
    -0.000012407942728372,
    0.000002171183264035,
    0.000007891246439399,
    -0.000001383364938858,
    -0.000004880552445070,
    0.000000851058165466,
    0.000002924996196050,
    -0.000000500695963250,
    -0.000001685312444764,
    0.000000273080771464,
    0.000000904795499720,
    -0.000000119790027228,
    -0.000000386445025695,
)
bandpass_buffer = 512
def apply_bandpass_filter(i2s_read_buffer, bandpass_coeffs):
    bytes_read = len(i2s_read_buffer)
    filtered_buffer = np.empty(bytes_read, dtype=np.int16)
    
    for i in range(bytes_read):
        filtered_sample = 0.0
        for j, coeff in enumerate(bandpass_coeffs):
            if i >= j:
                filtered_sample += coeff * i2s_read_buffer[i - j]
        filtered_buffer[i] = abs(int(filtered_sample)) #ABS THE VALUE
    
    return filtered_buffer

#apply the filter to data buffered in frames
filtered_frames = []
inted_frames = []
for i in range(0, nframes * 2, 2):
    inted_frames.append( int.from_bytes(frames[i:i+2], 'little', signed=True))

for i in range(0, nframes, bandpass_buffer):
    filtered_frames.extend(apply_bandpass_filter(inted_frames[i:i+bandpass_buffer], bandpass_coeffs))

# ---- threshold detection ---

threshold = 150
is_above_threshold = False
for i, frame in enumerate(filtered_frames):
    if is_above_threshold and frame < threshold:
        is_above_threshold = False
        print("peak at", i, "  ", frame)
    if frame > threshold:
        is_above_threshold = True

#plot filtered frames
print("nframes", nframes)
print(len(filtered_frames))
plt.plot(filtered_frames)
plt.show()
