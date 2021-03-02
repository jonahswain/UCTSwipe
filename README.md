# UCTSwipe
Student access card reader/logger

This project is intended as a class attendance logger for the University of Cape Town. In conjunction with the relevant hardware, it reads 125kHz RFID student cards, and logs the student's details to a Google sheet. The project available here on Github is incomplete, as certain components are omitted for security reasons. It should be readily adaptable to work with other RFID card systems/databases if needed.

This project was prepared by Jonah Swain in fulfillment of the vacation work experience requirements for EEE1000X for the University of Cape Town.

## Hardware requirements
- A Raspberry Pi with WiFi (I used a model 3B)
- An RDM6300 RFID card reader module
- A ADM1602K-NSA-FBS 2-line LCD display
- An RGB LED
- Some switches (I used some spare chunky panel mount ones)
- A power bank to power the Pi (if you want it to be portable)

## Set-up, configuration, and usage
Consult `RPi_Setup.md` for information on how to set up the Pi and the project, and use the attendance logger.