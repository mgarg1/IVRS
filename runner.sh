#!/bin/bash

# /home/pi/IVRS/venv/bin/python /home/pi/IVRS/src/app.py &
# /home/pi/IVRS/venv/bin/python /home/pi/IVRS/src/app_kilall.py &
# /home/pi/IVRS/venv/bin/python /home/pi/IVRS/src/event_loop_telegram.py &

sudo systemctl disable serial-getty@USB0.service

# start the core app
./app_runner.sh

# start the telegram event loop
./telegram_runner.sh
