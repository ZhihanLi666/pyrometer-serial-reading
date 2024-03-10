#pyrometer serial reading ieee754
import serial
import struct

# Configure the serial port
def decode_ieee754(data):
    if len(data) != 4:
        raise ValueError("Buffer length must be 4 bytes for IEEE 754 single precision float")
    return struct.unpack('f', data)[0]
while 1:
    try:
    # Configure the serial port
        ser = serial.Serial(
        port='COM1',  # Change this to the appropriate serial port on your system
        baudrate=115200,         # Set the baud rate
        timeout=1,              # Set timeout (in seconds) for reading
         bytesize=8,  # Set data bits (5, 6, 7, 8)
    #parity=None,  # Set parity (NONE, EVEN, ODD)
         stopbits=serial.STOPBITS_ONE,  # Set stop bits (ONE, ONE_POINT_FIVE, TWO)
       parity=serial.PARITY_NONE)

    # Open the serial port
    #ser.open()

        try:
        # Send command to the device to request data
            command = b'\x82'  # Assuming 0x82 is the command to request data
            ser.write(command)

        # Read response from the device
            response = ser.read(4)  # Assuming the data packet is 4 bytes long

        # Parse the data packet and decode IEEE 754 floating-point representation
            if response:
                data_value = decode_ieee754(response)
                print("Received data:", data_value)
            else:
               print("No response received from the device.")
        except serial.SerialException as e:
               print("Serial communication error:", e)
        finally:
        # Close the serial port
               ser.close()
    except serial.SerialException as e:
        print("Failed to open serial port:", e)



