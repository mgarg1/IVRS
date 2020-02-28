# python -m virualenv proj/ --no-download -p python3
# sudo apt-get install libjpeg-dev zlib1g-dev
# pip install python-escpos --no-cache-dir

# https://python-escpos.readthedocs.io/en/latest/user/raspi.html

from escpos.printer import Usb

""" Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
p = Usb(0x04b8, 0x0202, 0, profile="TM-T88III")
p.text("Hello World\n")
p.image("logo.gif")
p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
p.cut()
