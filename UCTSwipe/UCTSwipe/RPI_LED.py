# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# LED control

# Imports
import threading
import time
import gpiozero

class RGB_LED(threading.Thread):
    """An RGB LED"""

    # Command structure: [LED ('r'/'g'/'b'), state ('on'/'off'), time (seconds)]

    def __init__(self, red_pin, green_pin, blue_pin):

        threading.Thread.__init__(self)

        self._R = gpiozero.OutputDevice(red_pin)
        self._G = gpiozero.OutputDevice(green_pin)
        self._B = gpiozero.OutputDevice(blue_pin)

        self._commands = []

    def run(self):
        while(True): # Loop forever
            if (len(self._commands) > 0):
                self.execute_command(self._commands[0])
                del self._commands[0]
            time.sleep(0.1)

    def execute_command(self, command):
        if (command[0] == 'r'):
            if (command[1] == 'on'): self._R.on()
            elif (command[1] == 'off'): self._R.off()
        elif (command[0] == 'g'):
            if (command[1] == 'on'): self._G.on()
            elif (command[1] == 'off'): self._G.off()
        elif (command[0] == 'b'):
            if (command[1] == 'on'): self._B.on()
            elif (command[1] == 'off'): self._B.off()
        if (command[2] <= 0.1):
            return
        else:
            time.sleep(command[2] - 0.1)

    def queue_command(self, colour, state, time):
        self._commands.append([colour, state, time])

    def on(self, colour):
        self.queue_command(colour, 'on', 0)

    def off(self, colour):
        self.queue_command(colour, 'off', 0)

    def blink(self, colour, period, repetitions=1):
        for i in range(0, repetitions):
            self.queue_command(colour, 'on', period/2)
            self.queue_command(colour, 'off', period/2)
