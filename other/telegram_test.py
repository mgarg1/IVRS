import requests
import dateparser

TELEGRAM_BOT_ID = '1638267732'
TELEGRAM_AUTH_TOKEN = 'AAFVHLOeoIc65c8FKCtVhYbqDN0_T55_1rQ'
TELEGRAM_MOHIT_CHATID = '1682000090'

# def sendMessageToTelegram(outMsg,recepient=TELEGRAM_GROUP_CHATID):
#     url = 'https://api.telegram.org/bot%s:%s/sendMessage' % (TELEGRAM_BOT_ID,sensitive.TELEGRAM_AUTH_TOKEN)
#     payload = '{"chat_id": "%s", "text": "%s", "disable_notification": true}' % (recepient,outMsg)
#     headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
#     return requests.post(url, data=payload, headers=headers)

def getUpdatesFromTelegram():
    # curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates 
    url = 'https://api.telegram.org/bot%s:%s/getUpdates' % (TELEGRAM_BOT_ID,TELEGRAM_AUTH_TOKEN)
    # payload = '{"chat_id": "%s", "text": "%s", "disable_notification": true}' % (recepient,outMsg)
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
    return requests.post(url, headers=headers)

aa = getUpdatesFromTelegram()
print(aa.json()['result'][0])
#print(dir(aa))

#print(getUpdatesFromTelegram()['result'])
#print(dateparser.parse('12/Mar/20'))
