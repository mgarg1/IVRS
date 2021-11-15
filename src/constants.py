import os

DATE_FORMAT = '%d-%B-%Y'
BOOK_LIMIT = 25
START_TOKEN_NUM = 16

WEEKDAYS_HINDI = ["Somvar","Mangalvar","Budhvar","Guruvar","Shukrvar","Shanivar","Ravivar"]

ROOTPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHONE_DB_FILE = os.path.join(ROOTPATH,'src','phoneDB.json')
HOLIDAY_DB_FILE = os.path.join(ROOTPATH,'src','holidayDB.txt')
ARCHIVE_DB_FILE = os.path.join(ROOTPATH,'src','archiveDB.txt')

ENTER_PHONE_NUM, CONFIRM_DATE, CONFIRMATION, SEL_DATE, ALREADY_REGISTERED   = range(5)