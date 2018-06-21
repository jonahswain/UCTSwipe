# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# Main file

import RPI_LCD
import time
import gpiozero as GPIO

def main():
    # Main function
    piLCD = RPI_LCD.LCD(20, 21, 5, 6, 13, 19)
    piLCD.initialise()
    piLCD.write("Startup", "In progress")


if (__name__ == "__main__"):
    main()