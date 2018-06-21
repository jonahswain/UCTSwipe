# UCTSwipe
# Student access card reader/logger
# Author: Jonah Swain (SWNJON003)
# Attendance logging (using Google Sheets)

# Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class AttendanceLog(object):
    """An attendance log (local and remote logging of student numbers)"""

    # Saves student numbers in a local text file and pushes them to a google sheet

    def __init__(self, staff_id):
        # Creates an attendance logger and opens/creates a corresponding GSheet
        pass