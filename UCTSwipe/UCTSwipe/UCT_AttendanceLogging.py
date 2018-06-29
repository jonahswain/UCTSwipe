# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# Attendance logging (using Google Sheets)

# Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import datetime
import threading
import gpiozero
import RPI_CardReader
import RPI_LCD
import RPI_LED
import uct_info

class AttendanceLog(threading.Thread):
    """An attendance/access log (Local and remote logging of (allowed) student numbers)"""

    ATTENDANCE_LOG_FILE_PATH = "attendance_logs/"

    def sheet_exists(sheet):
        # Check if a sheet exists
        oa2scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        oa2creds = ServiceAccountCredentials.from_json_keyfile_name('UCTSwipe_gscredential.json', oa2scope)

        try:
            gsclient = gspread.authorize(oa2creds)
        except:
            return False
        else:
            try:
                gs = gsclient.open(sheet)
            except:
                return False
            else:
                return True

    def _on_error(self, error):
        # Error handling method
        # Potentially use GPIO/LEDs or LCD to show errors in future

        print("Error:", error)

    def __init__(self, sheet_name, access_sheet_number = 0):

        threading.Thread.__init__(self)

        # RGB LED
        self.g_led = gpiozero.LED(27)
        self.r_led = gpiozero.LED(17)

        # OAuth2 Authorization credentials
        oauth2_scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        oauth2_credentials = ServiceAccountCredentials.from_json_keyfile_name('UCTSwipe_gscredential.json', oauth2_scope)

        # Worksheet log name
        dt_now = datetime.datetime.now()
        dt_now_str = dt_now.strftime("%Y.%m.%d_%H.%M")
        self.worksheet_name = "Attendance_" + dt_now_str

        # Access list worksheet name
        self.access_sheet_name = "AccessList"
        if (access_sheet_number != 0):
            self.access_sheet_name = self.access_sheet_name + "_" + str(access_sheet_number)

        # Log in and open sheet
        self.status = 'online'
        try:
            self.gspread_client = gspread.authorize(oauth2_credentials)
        except:
            # Error handling here
            self.on_error("Unable to authorize GSpread credentials")
            self.status = 'offline'

        else:
            try:
                self.gsheet = self.gspread_client.open(sheet_name)
            except:
                # Error handling here
                self.on_error("Could not open sheet: " + sheet_name)
                self.mode = 'offline'

        if (self.status == 'online'):
            # Setup mode and worksheet
            try:
                worksheet_list_raw = self.gsheet.worksheets()
                self.gsheet_worksheet_list = []
                for ws in worksheet_list_raw:
                    self.gsheet_worksheet_list.append(ws.title)
            except:
                self._on_error("Unable to fetch worksheet list")
            else:
                if (self.access_sheet_name in self.gsheet_worksheet_list): # Try to get access worksheet
                    try:
                        self.access_sheet = self.gsheet.worksheet(self.access_sheet_name)
                    except:
                        self._on_error("Unable to open access list: " + self.access_sheet_name)
                        self.mode = 'attendance'
                    else:
                        self.mode = 'access'
                else:
                    self.mode = 'attendance'

            try: # Try to create log worksheet
                self.worksheet = self.gsheet.add_worksheet(title = self.worksheet_name, rows = 1000, cols = 3)
                self.worksheet.append_row(["Student ID", "Access authorization", "Time scanned"])
            except:
                self._on_error("Could not create log worksheet: " + self.worksheet_name)
                self.status = 'offline'

        # Pull access list from GSheets
        if (self.status == 'online' and self.mode == 'access'):
            self.access_list = self.access_sheet.col_values(1)

        self.attendance_list = []
        self.gsheet_index = 0

        # File log
        self.attendance_file_name = AttendanceLog.ATTENDANCE_LOG_FILE_PATH + sheet_name + "_" + self.worksheet_name + ".atlog"


    def run(self):
        # Thread
        self.sleep_cnt = 0
        while(True):
            self.sleep_cnt += 1
            if (self.sleep_cnt >= 12):
                self.sleep_cnt = 0
                self.update_acces_list()
            self.push_to_gsheet()
            time.sleep(300) # sleep for 5 minutes

    def log(self, uct_id):
        # Logs a student number

        time_now = datetime.datetime.now()
        time_now_str = time_now.strftime("%H:%M")

        access = ""
        if (self.mode == 'access'):
            if (uct_id in self.access_list):
                access = "Allowed"
            else:
                access = "Not allowed"
        self.attendance_list.append([uct_id, access, time_now_str])

        # Add to file log
        attendance_list_file = open(self.attendance_file_name, mode = 'a')
        attendance_list_file.write(uct_id + ", " + access + ", " + time_now_str + "\n")
        attendance_list_file.close()

        # On log actions
        self.on_log(uct_id)
        if (access == "Allowed"):
            self.on_access_successful(uct_id)
        if (access == "Not allowed"):
            self.on_access_unsuccessful(uct_id)

    def push_to_gsheet(self):
       # Pushes any pending student numbers to the GSheet log
       if (self.status == 'online'):
            while(self.gsheet_index < len(self.attendance_list)):
                try:
                    self.worksheet.append_row(self.attendance_list[self.gsheet_index])
                except:
                    self._on_error("Error adding " + self.attendance_list[self.gsheet_index][0] + " to attendance worksheet")
                self.gsheet_index += 1

    def update_acces_list(self):
        # Updates the access list (can be called periodically to keep the list up-to-date)
        if (self.status == 'online' and self.mode == 'access'):
            self.access_list = self.access_sheet.col_values(1)

    def on_log(self, uct_id):
        # Actions to take when a uct_id is logged
        if (self.mode == 'access'):
            self.g_led.blink(0.5, 0.5, 3)

    def on_access_successful(self, uct_id):
        # Actions to take when access mode is in effect and access is successful
        self.g_led.blink(0.5, 0.5, 3)

    def on_access_unsuccessful(self, uct_id):
        # Actions to take when access mode is in effect and access is unsuccessful
        self.g_led.blink(0.5, 0.5, 3)

    def __del__(self):
       self.attendance_list_file.close()

class AttendancePi(threading.Thread):
    """A Raspberry Pi based attendance logger which runs nicely in the background"""

    def __init__(self, card_reader, lcd):
        # Set up basic values
        threading.Thread.__init__(self)
        self.card_reader = card_reader
        self.lcd = lcd

    def get_id_from_tag(tag):
        uct_data = uct_info.get_info_from_tag(tag)
        if (len(uct_data) > 0):
            return uct_data['uct_id']
        else:
            return None

    def run(self):
        self.lcd.write("-Attendance Log-", "Student-made :)") # Display welcome message
        time.sleep(1)
        self.lcd.write("Scan staff card", "to initialise")
        while(True):
            if (self.card_reader.card_data_available() > 0): # Wait until a card is scanned
                self.staff_id = AttendancePi.get_id_from_tag(self.card_reader.get_card_data())
                if (self.staff_id):
                    if (AttendanceLog.sheet_exists(self.staff_id)): # Check if a sheet for that person exists
                        self.lcd.write("Staff ID:", self.staff_id)
                        self.card_reader.flush_card_data() # Flush any card data
                        break
                    else:
                        self.lcd.write("Not authorised", "")
                        time.sleep(1)
                    self.lcd.write("Scan staff card", "to initialise")
                else:
                    self.lcd.write("Card not", "recognised")
                    time.sleep(1)
                    self.lcd.write("Scan staff card", "to initialise")
                self.card_reader.flush_card_data() # De-bounce
            time.sleep(0.2)
        # Staff card has now been scanned, prepare for everything else
        
        # TODO: Add access sheet number selection

        self.attendance_log = AttendanceLog(self.staff_id)
        self.attendance_log.start()

        if (self.attendance_log.status == 'offline'):
            self.lcd.write("Offline mode", "Saving to file")
            time.sleep(5)

        self.lcd.write("Scan card for", "attendance")

        while(True):
            if(self.card_reader.card_data_available() > 0):
                student_id = AttendancePi.get_id_from_tag(self.card_reader.get_card_data())
                if (student_id):
                    self.lcd.write("Scanned:", student_id)
                    self.attendance_log.log(student_id)
                    time.sleep(1)
                    self.lcd.write("Scan card for", "attendance")
                    self.card_reader.flush_card_data() # De-bounce
                else:
                    self.lcd.write("Card not", "recognised")
                    time.sleep(1)
                    self.lcd.write("Scan card for", "attendance")
                self.card_reader.flush_card_data() # De-bounce
            time.sleep(0.2)

    def __del__(self):
        self.attendance_log.push_to_gsheet()