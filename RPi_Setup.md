# Instructions for setting up the Raspberry Pi (For use with the UCTSwipe project)  
0. Install the latest version of Raspbian lite (Stretch at the time of writing) on an SD card  
1. **Pre-boot procedure**  
   1.1. Create an empty/blank file called ssh in the boot partition of the SD card (to enable SSH server)  
   1.2. Append 'ip=10.255.255.254:::255.255.255.252:rpi:eth0:off' to 'cmdline.txt' in the boot partition  
2. **First boot procedure**  
   2.1. Connect to your Pi  
        2.1.1. Connect an ethernet cable between your PC/Laptop and your Pi  
        2.1.2. Set a static IP address for your PC/Laptop (IP: 10.255.255.253 Subnet: 255.255.255.252 (/30))  
        2.1.3. SSH in to the Pi (ssh pi@10.255.255.254)  
   2.2. Change the Pi's password (using the command passwd)  
   2.3. Set a permanent static IP address for the Pi  
        Append the following to /etc/dhcpcd.conf  
        # Static IP profile for eth0  
        profile static_eth0  
        static ip_address=10.255.255.254/30  
        static routers=  
        static domain_name_servers=    
        # Ethernet interface configuration  
        interface eth0  
        fallback static_eth0  
   2.4. Remove 'ip=10.255.255.254:::255.255.255.252:rpi:eth0:off' from /boot/cmdline.txt  
     
3. **Eduroam WiFi configuration**  
   Skip this step if not using eduroam for WiFi
   3.1. Append the following to /etc/dhcpcd.conf  
        # Wireless configuration  
        interface wlan0  
   3.2. Append the following to /etc/wpa_supplicant/wpa_supplicant.conf  
        network={  
        ssid="eduroam"  
        scan_ssid=0  
        key_mgmt=WPA-EAP  
        pairwise=CCMP TKIP  
        group=CCMP TKIP  
        eap=PEAP  
        identity="STUDENTNUMBER@wf.uct.ac.za"  
        password="UCTPASSWORD"  
        phase2="auth=MSCHAPv2"  
        }  
4. **Required packages**  
   - Do the following commands first:  
     - sudo apt-get update  
     - sudo apt-get upgrade  
   - Install the following packages (sudo apt-get install)  
     - python3.4  
     - python3.4-dev  
     - python-pip  
     - python3-pip  
     - git  
     - freetds-dev  
5. **Python environment**  
   5.1. Install pipenv (pip install pipenv)  
   5.2. Create a folder for UCTSwipe (These instructions assume the folder is /home/pi/UCTSwipe) (mkdir UCTSwipe)  
   5.3. Make the folder your working directory (cd /home/pi/UCTSwipe)  
   5.4. Create a python virtual environment (python version 3.4) in the directory with pipenv (pipenv --python 3.4)  
   5.5. Install the following python dependencies into the environment with pipenv (pipenv install)  
        - RPi.GPIO  
        - RPIO (probably optional)  
        - pigpio (probably optional)  
        - gpiozero  
        - gspread  
        - oauth2client  
        - pyserial  
        - pymssql  
6. **GPIO serial**  
   6.1. Enable software serial by adding the line 'enable_uart=1' to /boot/config.txt  
   6.2. Disable console output on serial by removing 'console=serial0,115200' from /boot/cmdline.txt  
7. **GPIO connections**  
   All RPi GPIO pins in BCM numbering  
   - GPIO 20 -> LCD RS  
   - GPIO 21 -> LCD EN  
   - GPIO 5 -> LCD D4  
   - GPIO 6 -> LCD D5  
   - GPIO 13 -> LCD D6  
   - GPIO 19 -> LCD D7  
   - GPIO 14 (TX) -> RDM6300 RX  
   - GPIO 15 (RX) -> RDM6300 TX  
   - GPIO 17 -> RGB LED Red  
   - GPIO 27 -> RGB LED Green  
   - GPIO 22 -> RGB LED Blue  
   - GPIO 8 -> Shutdown/off button  
   - GPIO 23 -> Toggle switch (1)  
   - GPIO 24 -> Toggle switch (2)  
   - GPIO 25 -> Toggle switch (4)  
   - LCD V0 -> a 10k contrast adjust potentiometer  
   - LCD RW -> ground  
   - LCD A -> +5V  
   - LCD K -> ground  
8. **UCTSwipe installation**  
   8.1. Unzip the file UCTSwipe.zip (provided to UCT directly, contains everything) into /home/pi/UCTSwipe  
   8.2. Make the file autorun.sh executable (sudo chmod +x autorun.sh)  
   8.3. Add a cron job (using crontab -e) to run the file autorun.sh on startup (@reboot /home/pi/UCTSwipe/autorun.sh)  
9. **Using UCTSwipe**  
   (( Just use it, it's that simple, seriously ))  
   9.1. Adding access to lecturers/TAs  
        9.1.1. The lecturer/TA must create a google sheet, named as their staff/student number  
               Staff numbers must include the leading zero, and student numbers must be in upper case  
        9.1.2. The lecturer/TA may create an acccess list by creating a worksheet in their google sheets called "AccessList" to control access to the venue/tutorial  
        9.1.3. Up to 7 additional access lists may be created (for multiple labs) by creating worksheets called "AccessList_1" through "AccessList_7" - the naming convention must be followed exactly in order for it to function correctly  
        9.1.4. The lecturer/TA must then share the google sheet (with edit permissions) to the email address of the PI (this is provided to UCT directly, to avoid abuse of the system)  
   9.2. Checking attendance  
        The device creates a google sheets worksheet in the lecturer/TA -'s google sheet (shared with the device in step 8.1) titled Attendance_date_time where date and time correspond to the date and time when the device was initialised. The contents of the worksheet contains 3 columns with the student number, authorisation (if configured with an access list in step 8.1), and time scanned of each scanned card. Do whatever you want with the provided information.  
   9.3. Checking attendance (if the device shuts down unexpectedly)  
        In the event the PI shuts down unexpectedly, without first pushing pending changes to google sheets, a plaintext file log is saved on the device in the attendance_logs folder.  
