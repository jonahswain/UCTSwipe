# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# Main file

import RPI_LCD
import time
import gpiozero as GPIO
import UCT_AttendanceLogging
import RPI_CardReader
import uct_info

def main_attendance():
    # Main function
    
    piLCD = RPI_LCD.LCD(20, 21, 5, 6, 13, 19)
    piLCD.initialise()
    piLCD.write("Startup", "In progress")

    card_reader = RPI_CardReader.CardReader("/dev/ttyS0")
    card_reader.start()

    attendance_pi = UCT_AttendanceLogging.AttendancePi(card_reader, piLCD)
    attendance_pi.start()

if (__name__ == "__main__"):
    main_attendance()

