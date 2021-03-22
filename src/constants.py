import os

DATE_FORMAT = '%d-%B-%Y'
BOOK_LIMIT = 20

WEEKDAYS_HINDI = ["Somvar","Mangalvar","Budhvar","Guruvar","Shukrvar","Shanivar","Ravivar"]

ROOTPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHONE_DB_FILE = os.path.join(ROOTPATH,'src','phoneDB.json')
HOLIDAY_DB_FILE = os.path.join(ROOTPATH,'src','holidayDB.txt') 