import os

DATE_FORMAT = '%d-%B-%Y'
BOOK_LIMIT = 30
START_TOKEN_NUM = 11

WEEKDAYS_HINDI = ["Somvar","Mangalvar","Budhvar","Guruvar","Shukrvar","Shanivar","Ravivar"]

ROOTPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHONE_DB_FILE = os.path.join(ROOTPATH,'src','phoneDB.json')
HOLIDAY_DB_FILE = os.path.join(ROOTPATH,'src','holidayDB.txt')
ARCHIVE_DB_FILE = os.path.join(ROOTPATH,'src','archiveDB.txt')