# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# Card reader

# Imports
import threading
import serial
import time

class CardReader(threading.Thread):
    """An RDM6300 card reader connected via serial"""

    def __init__(self, serial_port):
        # Open com port
        threading.Thread.__init__(self)
        self.com = serial.Serial(serial_port,baudrate=9600,parity=serial.PARITY_ODD,stopbits=serial.STOPBITS_TWO,bytesize=serial.SEVENBITS)
        self.card_data = []

    def run(self):
        # Running part of thread (in background scan card reader serial port)
        card_data_length = 14
        while True:
            # Loop forever
            if (self.com.inWaiting() >= card_data_length):
                card_data_raw = self.com.read(card_data_length) # Retrieve the data from the serial buffer
                card_data_raw = card_data_raw.decode("utf-8") # Decode it into characters
                card_data_raw = int(card_data_raw[1:-3], 16) # Convert it into base 16
                self.card_data.append(card_data_raw) # Add it to the available data array
            time.sleep(0.1) # Sleep for 100ms, allowing other threads to execute

    def card_data_available(self):
        return len(self.card_data)

    def get_card_data(self):
        if (len(self.card_data > 0)):
            cdata = self.card_data[0]
            del self.card_data[0]
            return cdata
        else:
            return None

    def flush_serial(self):
        # Flush any serial data waiting
        self.com.read(self.com.inWaiting())