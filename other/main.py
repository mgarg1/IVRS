# python -m virualenv proj/ --no-download -p python3
# sudo apt-get install libjpeg-dev zlib1g-dev
# pip install python-escpos --no-cache-dir

# https://python-escpos.readthedocs.io/en/latest/user/raspi.html

from escpos.printer import Usb
from datetime import datetime


def setupPrinter():
	return Usb(0x0456, 0x0808, 0, 0x81, 0x03)

def printDate(printerObj):
	printerObj.set(font='a', height=1, width=1, align='center')
	now = datetime.now() # current date and time
	now_time = now.strftime("%d-%b-%Y         %H:%M:%S")
	printerObj.text(now_time)

def printToken(p,tokenCount):
	p.control("LF")
	printDate(p)	
	
	p.set(font='a', height=3, width=3, align='center')
	p.image("sleet3.png",impl="bitImageColumn")
	p.text(tokenCount)
	p.text("\n\n")
	p.image("footer.png",impl="bitImageColumn")
	p.text("\n\n\n\n")
	
p = setupPrinter()
printToken(p,'23')