#!/bin/bash

IVRS_DIR="/home/pi/Desktop/IVRS"
APP_NAME="app_gsm"

#command to find the screen id of the existing app_gsm screen session
screenList=`screen -ls $APP_NAME | grep $APP_NAME | cut -d'.' -f1`

if [ ! -z "$screenList" ]
then
      echo "$APP_NAME is alive. Killing It"
      screen -S "$APP_NAME" -X at "#" stuff '^C'      
else
      echo "no existing session starting $APP_NAME"
fi

screen -S "$APP_NAME" -dm bash -c "sleep 2m; source $IVRS_DIR/venv/bin/activate && python3 $IVRS_DIR/src/app_gsm.py"
