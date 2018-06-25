# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# Main file

#import RPI_LCD
import time
#import gpiozero as GPIO
import UCT_AttendanceLogging

def main():
    # Main function
    
    #piLCD = RPI_LCD.LCD(20, 21, 5, 6, 13, 19)
    #piLCD.initialise()
    #piLCD.write("Startup", "In progress")

    al = UCT_AttendanceLogging.AttendanceLog("TestSheet")
    al.log("SWNJON003")
    al.log("THLNIC003")
    al.log("PDXJUS001")
    al.push_to_gsheet()


if (__name__ == "__main__"):
    main()