# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# Card reader

# Imports
import threading
import serial

class CardReader(threading.Thread):
    """An RDM6300 card reader connected via serial"""

    def __init__(self, serial_port):
        # Open com port
        self.com = serial.Serial(serial_port,baudrate=9600,parity=serial.PARITY_ODD,stopbits=serial.STOPBITS_TWO,bytesize=serial.SEVENBITS)
        self.card_data = []

    def run(self):
        pass # Running part of thread (in background scan card reader serial port

    def card_data_available(self):
        pass # Return the number of card data in the array

    def get_card_data(self):
        pass # Return the first card data in the array