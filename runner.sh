#!/bin/bash

# /home/pi/IVRS/venv/bin/python /home/pi/IVRS/src/app.py &
# /home/pi/IVRS/venv/bin/python /home/pi/IVRS/src/app_kilall.py &
# /home/pi/IVRS/venv/bin/python /home/pi/IVRS/src/event_loop_telegram.py &


IVRS_DIR="/home/pi/Desktop/IVRS"
# start the core app
screen -S app_gsm -dm bash -c "sleep 5; source $IVRS_DIR/venv/bin/activate && python3 $IVRS_DIR/src/app_gsm.py"

# start the telegram event loop
screen -S telegram_loop -dm bash -c "source $IVRS_DIR/venv/bin/activate && python3 $IVRS_DIR/src/event_loop_telegram.py"
