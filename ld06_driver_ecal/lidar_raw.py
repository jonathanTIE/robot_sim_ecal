import serial, time

buffer = list()

SERIAL_PORT = 'COM4'

ser = serial.Serial(port=SERIAL_PORT,
                    baudrate=230400,
                    timeout=5.0,
                    bytesize=8,
                    parity='N',
                    stopbits=1)
    
while True:
    b = ser.read()
    tmpInt = int.from_bytes(b, 'big')
    if tmpInt == 0x54:
        print(time.time())


    """

    buffer.append(tmpInt)
    if len(buffer) > 100:
        print(buffer)
        print("\n")
        buffer = list()
    """
