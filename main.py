# pyrometer serial reading ieee754
import struct
import photrix

import matplotlib.pyplot as plt
import os

import threading
import queue
import time
from wxGUI import run_gui
from wxGUI import MyFrame

run_gui()

def decode_ieee754(data: bytes):
    if len(data) != 4:
        raise ValueError(
            "Buffer length must be 4 bytes for IEEE 754 single precision float"
        )
    return struct.unpack(">f", data)[0]

def plotting_callback():
    return


if __name__ == "__main__":
    # Pyrometer is controlled by a mix of manual serial commands and MODBUS commands
    pyro = photrix.pyrometer("COM1")
    # Should implement buffered reading, but that's for later

    temperature_bytes = bytearray()
    current_bytes = bytearray()
    electronics_temperature_bytes = bytearray()
    diode_temperature_bytes = bytearray()

    print("Starting stream read...")

    #--modified by Zhihan define data queue and threads
    data_queue = queue.Queue() #save PDcurrent reading
    data_queue_temp = queue.Queue() #save fitted temp value
    i=0
    time_elapse=[]
    Time=[]
    PDcurrents=[]
    Temps=[]
    while True:
        
        header_byte = pyro.get_unescaped_byte()
        if header_byte == b"\x80":
            pyro.get_unescaped_byte()
        elif header_byte == b"\x81":
            temperature_bytes = bytearray()
            for _ in range(4):
                temperature_bytes.extend(pyro.get_escaped_byte())
        elif header_byte == b"\x82":
            current_bytes = bytearray()
            for _ in range(4):
                current_bytes.extend(pyro.get_escaped_byte())
            
            #put in threads/socket (from Zhihan)
            PDcurrent_point=decode_ieee754(current_bytes)
            temp_point=MyFrame.get_fitting_function(PDcurrent_point) #convert to temperature using selected fitting function based on paddle materials
            time_point=time.time()
            Time.append(time_point)
            PDcurrents.append(PDcurrent_point)
            Temps.append(temp_point)
            if i==0:
                time_elapse[i]=0
            else:
                time_elapse.append(time_elapse[i-1]+Time[i]-Time[i-1])
            data_queue.put((time_elapse[i], PDcurrent_point))
            data_queue_temp.put((time_elapse[i], temp_point))
            i+=1
            
            def generate_plot():
                x_data, y_data = [], [] #PDcurrent
                x1_data,y1_data=[],[] #temp
                plt.ion()  # Enable interactive mode
                fig, ax = plt.subplots()
                line, = ax.scatter([], [])
                ax1=ax.twinx()
                line1,=ax1.scatter([],[])
                ax.set_xlabel('Time/s')
                ax1.set_.ylabel('Temperature/C')
                ax.set_.ylabel('photodiode current/A')
                ax.title('Photrix Pyromter fitted temperature')
                ax.grid(True)
    
                def on_close(event):
                    plt.close(fig)
                    exit()
                fig.canvas.mpl_connect('close_event', on_close)

                while True:
                    if not data_queue.empty() and not data_queue_temp.empty():
             # Get data from the queue
                       x,y = data_queue.get()
                       x1,y1 = data_queue_temp.get()
            # Update plot data
                       x_data.append(x)
                       y_data.append(y)
                       line.set_data(x_data, y_data)
                       x1_data.append(x1)
                       y1_data.append(y1)
                       line1.set_data(x1_data, y1_data)
            # Adjust plot limits
                       ax.relim()
                       ax.autoscale_view()
                       ax1.relim()
                       ax1.autoscale_view()
            # Update the plot
                       plt.draw()
                       plt.pause(0.01)  # Pause to allow plot to update
                       plt.show()
        def data_save(filepath):
            with open(filepath, 'w') as file:
    # Write the header
                file.write("Time\tPDcurrent/A\tFitted Temperature/C\n")  # Assuming tab-separated format
    
    # Write the data
                for item1, item2 , item3 in zip(Time, PDcurrents, Temps):
                    file.write(f"{item1}\t{item2}\t{item3}\n")  # Assuming tab-separated format

        '''elif header_byte == b"\x83":
            temperature_bytes = bytearray()
            current_bytes = bytearray()
            for _ in range(4):
                temperature_bytes.extend(pyro.get_escaped_byte())
            for _ in range(4):
                current_bytes.extend(pyro.get_escaped_byte())
        elif header_byte == b"\x84":
            electronics_temperature_bytes = bytearray()
            diode_temperature_bytes = bytearray()
            for _ in range(4):
                electronics_temperature_bytes.extend(pyro.get_escaped_byte())
            for _ in range(4):
                diode_temperature_bytes.extend(pyro.get_escaped_byte())

        output_string = ""
        if temperature_bytes != b"":
            output_string += f"Temperature (C): {decode_ieee754(temperature_bytes):+e} "
        if current_bytes != b"":
            output_string += f"Current (A): {decode_ieee754(current_bytes):+e} "
        if electronics_temperature_bytes != b"":
            output_string += f"Electronics Temp. (C): {decode_ieee754(electronics_temperature_bytes):+e} "
        if diode_temperature_bytes != b"":
            output_string += (
                f"Diode Temp. (C): {decode_ieee754(diode_temperature_bytes):+e}"
            )
        print(output_string)
'''