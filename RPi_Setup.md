# Instructions for setting up the Raspberry Pi
0. Install the latest version of Raspbian (full/lite) on to your SD card
1. **Pre-boot procedure**  
   1.1. Create an empty file called ssh in the boot partition (to enable SSH server)  
   1.2. Append 'ip=10.255.255.253::10.255.255.254:255.255.255.248:rpi:eth0:off' to 'cmdline.txt' in the boot partition  
2. **First boot procedure**  
   2.1. Connect an ethernet cable between your computer and the Pi  
   2.2. Set your computers IP address to 10.255.255.252, and subnet mask to 255.255.255.248 (/29)  
   2.3. SSH into the Pi (IP address: 10.255.255.253)  
   2.4. Change the Pi's password (using passwd)  
   2.5. Set a permanent static IP for the Pi's ethernet  
    Append the following to /etc/network/interfaces  
    auto eth0  
    iface eth0 inet static  
        address 10.255.255.253  
        netmask 255.255.255.248  
        post-up route del default dev $IFACE  
   2.6. Remove 'ip=10.255.255.253::10.255.255.254:255.255.255.248:rpi:eth0:off' from 'cmdline.txt' in the boot partition (/boot/cmdline.txt)  
3. **Eduroam WiFi configuration** (Skip this step if not using eduroam)  
   3.1. Append the following to /etc/network/interfaces  
    auto wlan0  
    allow-hotplug wlan0  
    iface wlan0 inet dhcp  
        post-up sudo route add default wlan0  
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf  
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
4. **Dependencies**  
   4.1. Get the following packages from apt  
      - pip (Python library installer)  
      - git (Assuming you want to clone this project from github)  
   4.2. Get the following python libraries from pip  
      - gpiozero (RPi GPIO library)  
      - gspread (Google sheets library)  
      - oauth2client (For connecting to Google sheets)  
