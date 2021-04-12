# IVRS
* This project is about implementing the IVRS system using the raspberry pi and a phone and a DTMF decoder
  * tinydb -  for database
  * gtts - for generating the audio
  * flask - for a webserver to initiate the flow with caller ID, and respond with http response of the user confirmation 

##  SiteMap
###  src/

## Circuit Diagram
![Circuit Diagram](other/images/IVRS.png)

## TODO - Enhancement
- [ ] Automate - keep checking if call is active
- [ ] Sending message to WhatsApp - https://llamalab.com/automate/community/flows/8315
- [ ] Callback functionality
- [ ] remove pastebin flow - instead pdf download
- [ ] accept date in multiple format
- [ ] add holiday from REST API
- [ ] start the linux flask app automatically 
```bash
lxterminal --working-directory="/home/pi/IVRS" -e "bash -c \"source /home/pi/IVRS/venv/bin/activate;python src/app.py \""
```
- [ ] cold period (not to accept any reservation) - can be used for cleanup
- [ ] backup automate app flows
- [ ] remove DTMF encoder hardware

## TODO - BUGS
- [ ] while removing the stale entries from the DB make a backup to central server
- [ ] when making a holiday - send sms to all members that your reservation is cancelled pls book again for another appointment

## Linux DTMF Experiment
```bash
apt-get install multimon-ng
multimon-ng -t wav -a DTMF other/audiocheck.net_dtmf_112163_112196_11#9632_##9696.wav 
https://www.reddit.com/r/amateurradio/comments/f0wmux/could_use_some_help_with_multimonng_for_decoding/
https://cloudacm.com/?p=3197
https://www.thegeekstuff.com/2009/05/sound-exchange-sox-15-examples-to-manipulate-audio-files/
sox -b 16 -e signed-integer -r 22k -c 1 -d -t wavpcm -| multimon-ng -c -a dtmf -
# record audio in python:
https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone

#recording from the mic
export AUDIODEV=hw:1
rec -r 8000 -c 1 record_voice.wav # it shows the visualisation of the sound wave

#sox command to record audio and dump in a wav file
sox -b 16 -e signed-integer -c 1 -d -t wavpcm tt.wav

#multimon-ng legends:
-a  = add demodulator (e.g. DTMF)
-t  = input file type
-c  = Remove all demodulators (must be added with -a <demod>).
```

## Telegram API connect
```bash
# https://wk0.medium.com/send-and-receive-messages-with-the-telegram-api-17de9102ab78#:~:text=You%20can%20find%20it%20here,bot%20and%20an%20API%20token.
# https://gist.github.com/dideler/85de4d64f66c1966788c1b2304b9caf1
# https://www.freecodecamp.org/news/telegram-push-notifications-58477e71b2c2/

# **** V.V. IMP **** Just to be sure you have update send a 'hi' message first
curl https://api.telegram.org/bot{botID}:{API_key}/getUpdates
# obtain chat Id from the output of prev command
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{"chat_id": "{chatId from prev step}", "text": "This is a test from curl", "disable_notification": true}' \
     https://api.telegram.org/bot{botID}:{API_key}/sendMessage
```
## Supported REST Commands
* http://<hostname:port>/phoneNum/9876543210
* http://<hostname:port>/kilall
* http://<hostname:port>/cmd/PUB
* http://<hostname:port>/cmd/PUB/17-March-2021
* http://<hostname:port>/cmd/HOL
* http://<hostname:port>/cmd/HOL/09-March-2021
* http://<hostname:port>/cmd/REM
* http://<hostname:port>/cmd/REM/09-March-2021

## Imp Links:
* https://components101.com/modules/mt8870-dtmf-decoder-module
* https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
* https://stackoverflow.com/a/7027113/1496826
* https://github.com/Drewsif/PiShrink
* https://readthedocs.org/projects/gtts/downloads/pdf/latest/
* DTMF generator - https://www.audiocheck.net/audiocheck_dtmf.php
* Usb Audio Card Setup - https://www.raspberrypi-spy.co.uk/2019/06/using-a-usb-audio-device-with-the-raspberry-pi/
* Singleton - https://pypi.org/project/singleton-decorator/
