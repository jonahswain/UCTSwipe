# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# Attendance logging (using Google Sheets)

# Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime, date, time

class AttendanceLog(object):
    """An attendance log (local and remote logging of student numbers)"""

    # Saves student numbers in a local text file and pushes them to a google sheet

    def __init__(self, sheet_name, worksheet_name):
        # Creates an attendance logger and opens/creates a corresponding GSheet
        # Authorization
        oauth2_scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        oauth2_credentials = ServiceAccountCredentials.from_json_keyfile_name('UCTSwipe_gscredential.json', oauth2_scope)

        # Connect to Google Sheets and open the sheet
        self.mode = 'online'
        try:
            self.gspread_client = gspread.authorize(oauth2_credentials)
        except:
            # Error handling here
            self.on_error("Unable to authorize GSpread credentials")
            self.mode = 'offline'
            
        else:
            try:
                self.gsheet = self.gspread_client.open(sheet_name)
            except:
                # Error handling here
                self.on_error("Could not open sheet: " + sheet_name)
                self.mode = 'offline'
                

        # Create the log
        self.attendance_log = []
        self.log_gsheet_index = 0

        # Open or create the worksheet
        if (self.mode == 'online'):
            try:
                worksheet_list_raw = self.gsheet.worksheets()
                worksheet_list = []
                for ws in worksheet_list_raw:
                    worksheet_list.append(ws.title)
                if (worksheet_name in worksheet_list):
                    self.worksheet = self.gsheet.worksheet(worksheet_name)
                else:
                    self.worksheet = self.gsheet.add_worksheet(title = worksheet_name, rows=1000, cols=1)
            except:
                self.on_error("Could not open/create worksheet " + worksheet_name)

        # Create the file log
        dt_now = datetime.now()
        dt_now_str = dt_now.strftime("%Y.%m.%d_%H.%M")
        filename = "attendance_logs\\" + dt_now_str + "_" + sheet_name + "_" + worksheet_name + ".atlog"
        self.file_log = open(filename, 'w')

    def log(self, uct_id):
        # Adds a student number to the log
        self.attendance_log.append(uct_id)
        self.file_log.write(uct_id + "\n")

    def push_to_gsheet(self):
        # Pushes pending changes to Google Sheets
        if (self.mode == 'online'):
            while(self.log_gsheet_index < len(self.attendance_log)):
                try:
                    self.worksheet.append_row([self.attendance_log[self.log_gsheet_index]])
                except:
                    self.on_error("Could not add " + self.attendance_log[self.log_gsheet_index] + " to sheet")
                self.log_gsheet_index += 1

    def on_error(self, error):
        # Error handling goes here
        # Potentially print to LCD in future
        print("Error:", error)

    def __del__(self):
        # Cleans up
        self.file_log.close()
        try:
            del self.attendance_log
            del self.gsheet
            del self.gspread_client
        except:
            self.on_error("Could not delete GSheet attributes")