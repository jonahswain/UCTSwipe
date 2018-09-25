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
    
    log_file_name = "CardLog.txt" # File to log scanned card tag data to
    logging_enabled = True # Change to False to disable card tag data logging

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
                card_data_raw = card_data_raw[1:-3] # Chop the unneeded bytes off
                if (len(self.card_data) >= 1):
                    if (card_data_raw != self.card_data[-1]):
                        self.card_data.append(card_data_raw) # Add it to the available data array
                        if (CardReader.logging_enabled): # Log
                            log_file = open(CardReader.log_file_name, mode = 'a')
                            log_file.write(str(card_data_raw) + "\n")
                            log_file.close()
                else:
                    self.card_data.append(card_data_raw) # Add it to the available data array
                    if (CardReader.logging_enabled): # Log
                        log_file = open(CardReader.log_file_name, mode = 'a')
                        log_file.write(str(card_data_raw) + "\n")
                        log_file.close()

            time.sleep(0.1) # Sleep for 100ms, allowing other threads to execute

    def card_data_available(self):
        return len(self.card_data)

    def get_card_data(self):
        if (len(self.card_data) > 0):
            cdata = self.card_data[0]
            del self.card_data[0]
            return cdata
        else:
            return None

    def flush_serial(self):
        # Flush any serial data waiting
        self.com.read(self.com.inWaiting())

    def flush_card_data(self):
        # Flush any card data in the buffer/array
        while (len(self.card_data) > 0):
            del self.card_data[0]


    def __del__(self):
        self.com.close() # Close com port