#!/bin/bash

/home/pi/IVRS/venv/bin/python /home/pi/IVRS/src/app.py &
/home/pi/IVRS/venv/bin/python /home/pi/IVRS/src/app_kilall.py &
/home/pi/IVRS/venv/bin/python /home/pi/IVRS/src/event_loop_telegram.py &

