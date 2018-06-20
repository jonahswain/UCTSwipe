# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# Main file

import RPI_LCD
import time
import gpiozero as GPIO

def testLCD():
    myLCD = RPI_LCD.LCD(20, 21, 5, 6, 13, 19)
    myLCD.initialise()
    myLCD.write("Testing LCD", "123456789")
