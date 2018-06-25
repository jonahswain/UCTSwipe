# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# Attendance logging (using Google Sheets)

# Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime, date, time
import threading


class AttendanceLog():
    """An attendance/access log (Local and remote logging of (allowed) student numbers)"""

    ATTENDANCE_LOG_FILE_PATH = "attendance_logs\\"

    def _on_error(self, error):
        # Error handling method
        # Potentially use GPIO/LEDs or LCD to show errors in future

        print("Error:", error)

    def __init__(self, sheet_name, access_sheet_number = 0):

        # OAuth2 Authorization credentials
        oauth2_scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        oauth2_credentials = ServiceAccountCredentials.from_json_keyfile_name('UCTSwipe_gscredential.json', oauth2_scope)

        # Worksheet log name
        dt_now = datetime.now()
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
                self.worksheet = self.gsheet.add_worksheet(title = self.worksheet_name, rows = 1000, cols = 2)
            except:
                self._on_error("Could not create log worksheet: " + self.worksheet_name)
                self.status = 'offline'

        # Pull access list from GSheets
        if (self.status == 'online' and self.mode == 'access'):
            self.access_list = self.access_sheet.col_values(1)

        self.attendance_list = []
        self.gsheet_index = 0

        # Create access log file
        attendance_file_name = AttendanceLog.ATTENDANCE_LOG_FILE_PATH + sheet_name + "_" + self.worksheet_name + ".atlog"
        self.attendance_list_file = open(attendance_file_name, mode = 'w')

    def log(self, uct_id):
        # Logs a student number
        access = ""
        if (self.mode == 'access'):
            if (uct_id in self.access_list):
                access = "Allowed"
            else:
                access = "Not allowed"
        self.attendance_list.append([uct_id, access])
        self.attendance_list_file.write(uct_id + ", " + access + "\n")
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
        pass

    def on_access_successful(self, uct_id):
        # Actions to take when access mode is in effect and access is successful
        pass

    def on_access_unsuccessful(self, uct_id):
        # Actions to take when access mode is in effect and access is unsuccessful
        pass

    def __del__(self):
       self.attendance_list_file.close()