# Instructions for setting up the Raspberry Pi (For use with the UCTSwipe project)  
0. Install the latest version of Raspbian lite (Stretch at the time of writing) on an SD card  
1. ** Pre-boot procedure **  
   1.1. Create an empty/blank file called ssh in the boot partition of the SD card (to enable SSH server)  
   1.2. Append 'ip=10.255.255.254:::255.255.255.252:rpi:eth0:off' to 'cmdline.txt' in the boot partition  
2. ** First boot procedure **  
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
     
3. ** Eduroam WiFi configuration **  
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
4. ** Required packages **  
   - Do the following commands first:  
     - sudo apt-get update  
     - sudo apt-get upgrade  
   - Install the following packages (sudo apt-get install)  
     - python3.4  
     - python3.4-dev  
     - pip  
     - git  
     - freetds-dev  
5. ** Python environment **  
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
6. ** GPIO serial **  
   6.1. Enable software serial by adding 'enable_uart=1' to /boot/cmdline.txt  
   6.2. Disable console output on serial by removing 'console=serial0,115200' from /boot/cmdline.txt  
7. ** UCTSwipe installation **  
   7.1. Unzip the file UCTSwipe.zip (provided to UCT directly, contains everything) into /home/pi/UCTSwipe
   7.2. Cont.d
