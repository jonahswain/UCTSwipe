# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# LCD (Allows use of the ADM1602K-NSA-FBS/3.3V and similar 2x16 LCDs)

# Sidenote: The LCDs used at UCT are NOT ADM1602K-NSA-FBS/3.3V, they run on 5V. This caused me hours of headache wondering why my code wasn't working, when in fact I had the LCD connected to 3.3V so it wasn't powering on properly


# Imports
import time
import gpiozero as GPIO

class LCD(object):
    """A 2x16 LCD class"""

    # Commands
    ENABLE = 0x33 # Power up the LCD
    FOURBIT_MODE = 0x32 # Set the LCD to use only the higher order bus lines (D4-D7)
    TWOLINE_MODE = 0x28 # Set the LCD to two line mode (characters on both lines of display)
    DISPLAY_ENABLE = 0x0C # Displays data on the LCD (Also makes cursor invisible)
    DISPLAY_DISABLE = 0x08 # Blanks data from the LCD (But data is still stored)
    CURSOR_ENABLE = 0x01 # Displays the cursor (Send bitwise or-ed with DISPLAY_ENABLE)
    CURSOR_BLINKING = 0x03 # Enables cursor blinking (Send bitwise or-ed with DISPLAY_ENABLE and CURSOR_ENABLE)
    CLEAR_DISPLAY = 0x01 # Removes all data from the LCD
    CURSOR_HOME = 0x02 # Moves the cursor back to the first position on the first line
    CURSOR_LINETWO = 0xC0 # Moves the cursor to the first position of line two
    CURSOR_RIGHT = 0x14 # Moves the cursor one position to the right
    CURSOR_LEFT = 0x10 # Moves the cursor one position to the left

    def _delay_micros(microseconds):
        # Holds in a loop for a specified duration in microseconds (Note that this is very approximate in reality)
        end = time.time() + (microseconds/1000000.0)
        while time.time() < end:
            pass

    def _cycle_EN(self):
        # Cycles the EN line to trigger data reception on the LCD
        LCD._delay_micros(1)
        self._EN.on()
        LCD._delay_micros(1)
        self._EN.off()
        LCD._delay_micros(1)
        self._EN.on()
        LCD._delay_micros(1)

    def __init__(self, RS, EN,  D4, D5, D6, D7):
        # Declares an LCD on the specified GPIO pins
        self._RS = GPIO.OutputDevice(RS)
        self._EN = GPIO.OutputDevice(EN)
        self._D4 = GPIO.OutputDevice(D4)
        self._D5 = GPIO.OutputDevice(D5)
        self._D6 = GPIO.OutputDevice(D6)
        self._D7 = GPIO.OutputDevice(D7)
        self._EN.on()

    def initialise(self):
        # Performs LCD initialisation and clears the screen
        self._EN.on() # set EN high
        LCD._delay_micros(20000) # Wait 20ms for LCD to power up

        # Initialisation commands
        self.command(LCD.ENABLE) # Enable LCD controller
        self.command(LCD.FOURBIT_MODE) # Set to 4-bit mode
        self.command(LCD.TWOLINE_MODE) # Set 2-line mode
        self.command(LCD.CLEAR_DISPLAY) # Clear the LCD
        self.command(LCD.DISPLAY_ENABLE) # Enable the LCD

    def command(self, command):
        # Sends a command to the LCD
        self._RS.off() # Set RS low so data is interpreted as command

        # Send upper nibble
        if ((command & 0x80) > 0): self._D7.on()
        else: self._D7.off()
        if ((command & 0x40) > 0): self._D6.on()
        else: self._D6.off()
        if ((command & 0x20) > 0): self._D5.on()
        else: self._D5.off()
        if ((command & 0x10) > 0): self._D4.on()
        else: self._D4.off()

        self._cycle_EN()

        # Send lower nibble
        if ((command & 0x08) > 0): self._D7.on()
        else: self._D7.off()
        if ((command & 0x04) > 0): self._D6.on()
        else: self._D6.off()
        if ((command & 0x02) > 0): self._D5.on()
        else: self._D5.off()
        if ((command & 0x01) > 0): self._D4.on()
        else: self._D4.off()

        self._cycle_EN()

        if (command == LCD.CLEAR_DISPLAY or command == LCD.CURSOR_HOME): LCD._delay_micros(1530) # Wait 1.53 ms for command execution
        else: LCD._delay_micros(43) # Wait 43 us for command execution

    def place_character(self, character):
        # Places a character on the LCD at the current cursor position
        self._RS.on() # Set RS high so data is interpreted as character

        # Send upper nibble
        if ((character & 0x80) > 0): self._D7.on()
        else: self._D7.off()
        if ((character & 0x40) > 0): self._D6.on()
        else: self._D6.off()
        if ((character & 0x20) > 0): self._D5.on()
        else: self._D5.off()
        if ((character & 0x10) > 0): self._D4.on()
        else: self._D4.off()

        self._cycle_EN()

        # Send lower nibble
        if ((character & 0x08) > 0): self._D7.on()
        else: self._D7.off()
        if ((character & 0x04) > 0): self._D6.on()
        else: self._D6.off()
        if ((character & 0x02) > 0): self._D5.on()
        else: self._D5.off()
        if ((character & 0x01) > 0): self._D4.on()
        else: self._D4.off()

        self._cycle_EN()

        LCD._delay_micros(43) # Wait 43 us for command execution

    def set_cursor_position(self, row, column):
        # Moves the cursor to a specified position on the LCD
        column &= 0x1F # Drop column MSBs
        if (row == 1): # Add the row part to the column part
            column |= 0x80
        elif (row == 2):
            column |= 0xC0

        self.command(column) # Send the command

    def clear(self):
        # Clears the LCD
        self.command(LCD.CLEAR_DISPLAY)

    def place_string(self, string):
        # Places a string on the LCD, starting at the current cursor position
        for character in string:
            self.place_character(ord(character))

    def write(self, line1, line2):
        # Clears the LCD and writes lines 1 and 2

        #### DEBUG ####
        print("Writing to LCD:")
        print(line1)
        print(line2)
        print("================")
        #### END DEBUG ####
        self.command(LCD.CLEAR_DISPLAY)
        self.command(LCD.CURSOR_HOME)
        self.place_string(line1)
        self.command(LCD.CURSOR_LINETWO)
        self.place_string(line2)

    def __del__(self):
        # Deletes the current LCD instance and frees up all GPIO pins
        for gpio in {self._RS, self._EN, self._D4, self._D5, self._D6, self._D7}:
            gpio.close()
        del(self._RS)
        del(self._EN)
        del(self._D4)
        del(self._D5)
        del(self._D6)
        del(self._D7)
