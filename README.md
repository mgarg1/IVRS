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
- [ ] URI based holiday update
- [ ] Sending message to WhatsApp - https://llamalab.com/automate/community/flows/8315
- [ ] Callback functionality
- [ ] remove pastebin flow - instead pdf download

## Linux DTMF Setup
```bash
apt-get install multimon-ng
multimon-ng -t wav -a DTMF other/audiocheck.net_dtmf_112163_112196_11#9632_##9696.wav 
https://www.reddit.com/r/amateurradio/comments/f0wmux/could_use_some_help_with_multimonng_for_decoding/
https://cloudacm.com/?p=3197
sox -b 16 -e signed-integer -r 22k -c 1 -d -t wavpcm -| multimon-ng -a dtmf -
# record audio in python:
https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone

```
## Supported REST Commands
* http://<hostname:port>/phoneNum/9876543210
* http://<hostname:port>/kilall
* http://<hostname:port>/cmd/pub
* http://<hostname:port>/cmd/pub/17-March-2021

## Imp Links:
* https://components101.com/modules/mt8870-dtmf-decoder-module
* https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
* https://stackoverflow.com/a/7027113/1496826
* https://github.com/Drewsif/PiShrink
* https://readthedocs.org/projects/gtts/downloads/pdf/latest/
* DTMF generator - https://www.audiocheck.net/audiocheck_dtmf.php
* Usb Audio Card Setup - https://www.raspberrypi-spy.co.uk/2019/06/using-a-usb-audio-device-with-the-raspberry-pi/
* Singleton - https://pypi.org/project/singleton-decorator/
