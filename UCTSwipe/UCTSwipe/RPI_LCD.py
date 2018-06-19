# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# LCD
# Module to allow use of common 2x16 LCDs (ADM1602K-NSA-FBS/3.3V LCD) in 4-bit mode

# Imports
import gpiozero
import time

class LCD(object):
    """LCD class"""

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


    def __sleep_micros(microseconds):
        """Sleeps for a specified number of microseconds"""
        time.sleep(microseconds/1000000)

    def __cycle_EN(self):
        """Cycles the EN line (for data/commands to be sent)"""
        LCD.__sleep_micros(5) # Wait before cycling
        self.EN.on() # Ensure EN is high
        LCD.__sleep_micros(5) # Wait before cycling
        self.EN.off() # Set EN low
        LCD.__sleep_micros(10) # Wait
        self.EN.on() # Set EN high

    def __init__(self, pin_RS, pin_EN, pin_D4, pin_D5, pin_D6, pin_D7):
        """Initialises (declares) an LCD on the specified GPIO pin numbers (4-bit mode)"""
        self.RS = gpiozero.OutputDevice(pin_RS)
        self.EN = gpiozero.OutputDevice(pin_EN)
        self.data_lines = []
        self.data_lines.append(gpiozero.OutputDevice(pin_D4))
        self.data_lines.append(gpiozero.OutputDevice(pin_D5))
        self.data_lines.append(gpiozero.OutputDevice(pin_D6))
        self.data_lines.append(gpiozero.OutputDevice(pin_D7))

    def initialise(self):
        """Initialises the LCD display (performs initial configuration and clears the display)"""
        self.EN.on() # set EN high
        LCD.__sleep_micros(20000) # Wait 20ms

        # Initialisation commands
        self.send_command(LCD.ENABLE) # Enable LCD controller
        self.send_command(LCD.FOURBIT_MODE) # Set to 4-bit mode
        self.send_command(LCD.TWOLINE_MODE) # Set 2-line mode
        self.send_command(LCD.DISPLAY_DISABLE) # Enable the LCD
        self.send_command(LCD.CLEAR_DISPLAY) # Clear the LCD


    def clear(self):
        """Clears the LCD"""
        send_command(LCD.CLEAR_DISPLAY) # Clear the LCD

    def send_command(self, command):
        """Sends a command to the LCD"""

        self.RS.off() # Set RS low so data is interpreted as a command

        # Send 1st nibble of command
        if (command & 0x80): self.data_lines[0].on() # Set corresponding data line to value of command
        else: self.data_lines[0].off()
        if (command & 0x40): self.data_lines[1].on() # Set corresponding data line to value of command
        else: self.data_lines[0].off()
        if (command & 0x20): self.data_lines[2].on() # Set corresponding data line to value of command
        else: self.data_lines[0].off()
        if (command & 0x10): self.data_lines[3].on() # Set corresponding data line to value of command
        else: self.data_lines[0].off()
        self.__cycle_EN() # Cycle EN line

        # Send 2nd nibble of command
        if (command & 0x08): self.data_lines[0].on() # Set corresponding data line to value of command
        else: self.data_lines[0].off()
        if (command & 0x04): self.data_lines[1].on() # Set corresponding data line to value of command
        else: self.data_lines[0].off()
        if (command & 0x02): self.data_lines[2].on() # Set corresponding data line to value of command
        else: self.data_lines[0].off()
        if (command & 0x01): self.data_lines[3].on() # Set corresponding data line to value of command
        else: self.data_lines[0].off()
        self.__cycle_EN() # Cycle EN line

        if (command == LCD.CLEAR_DISPLAY or command == LCD.CURSOR_HOME): LCD.__sleep_micros(1530) # Wait 1.53 ms for command execution
        else: LCD.__sleep_micros(43) # Wait 43 us for command execution

    def set_cursor_position(self, line, character):
        """Moves the cursor to a specified location"""
        
        character &= 0x1F # Drop character MSBs
        if (line == 1): # Add the line part to the character part
            character |= 0x80
        elif (line == 2):
            character |= 0xC0

        self.send_command(character) # Send the command

    def place_character(self, character):
        """Places a character on the LCD at the current cursor position"""
        self.RS.on() # Set RS high so data is interpreted as a character

        # Send 1st nibble of character
        if (character & 0x80): self.data_lines[0].on() # Set corresponding data line to value of character
        else: self.data_lines[0].off()
        if (character & 0x40): self.data_lines[1].on() # Set corresponding data line to value of character
        else: self.data_lines[0].off()
        if (character & 0x20): self.data_lines[2].on() # Set corresponding data line to value of character
        else: self.data_lines[0].off()
        if (character & 0x10): self.data_lines[3].on() # Set corresponding data line to value of character
        else: self.data_lines[0].off()
        self.__cycle_EN() # Cycle EN line

        # Send 2nd nibble of character
        if (character & 0x08): self.data_lines[0].on() # Set corresponding data line to value of character
        else: self.data_lines[0].off()
        if (character & 0x04): self.data_lines[1].on() # Set corresponding data line to value of character
        else: self.data_lines[0].off()
        if (character & 0x02): self.data_lines[2].on() # Set corresponding data line to value of character
        else: self.data_lines[0].off()
        if (character & 0x01): self.data_lines[3].on() # Set corresponding data line to value of character
        else: self.data_lines[0].off()
        self.__cycle_EN() # Cycle EN line

        LCD.__sleep_micros(43) # Wait 43 us for character placement

    def write_string(self, string):
        """Places a string on the LCD, starting at the current cursor position"""
        for i in range(len(string)):
            self.place_character(int(string[i]))

    def write_lcd(self, line1, line2):
        """Clears the LCD and writes strings to both lines"""
        self.send_command(LCD.CLEAR_DISPLAY) # Clear the LCD
        self.send_command(LCD.CURSOR_HOME) # Home the cursor
        for i in range(len(line1)): # Write line 1
            self.place_character(int(line1[i]))
        self.send_command(LCD.CURSOR_LINETWO) # Move cursor to line 2
        for i in range(len(line2)): # Write line 2
            self.place_character(int(line2[i]))

    def __del__(self):
        """Deconstructor"""
        for pin in self.data_lines:
            pin.close()
            del pin
        del self.data_lines
        self.RS.close()
        self.EN.close()
        del self.RS
        del self.EN
