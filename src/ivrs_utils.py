import psutil
import sensitive
import requests

def killtree(pid, including_parent=True):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        print ("child", child)
        childStatus = child.status()
        if childStatus and childStatus != 'terminated':
            child.kill()

    if including_parent:
        parent.kill()

def sendMessageToTelegram(outMsg,recepient=sensitive.TELEGRAM_GROUP_CHATID):
    url = 'https://api.telegram.org/bot%s:%s/sendMessage' % (sensitive.TELEGRAM_BOT_ID,sensitive.TELEGRAM_AUTH_TOKEN)
    payload = '{"chat_id": "%s", "text": "%s", "disable_notification": true}' % (recepient,outMsg)
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
    return requests.post(url, data=payload, headers=headers)

def postMessageToPasteBin(outMsg):
    url = 'https://pastebin.com/api/api_post.php'
    payload = {"api_dev_key":sensitive.PASTEBIN_API_KEY,"api_paste_code":outMsg,"api_option":"paste", "api_paste_expire_date":"1D"}
    # curl -X POST -d 'api_dev_key=PASTEBIN_API_KEY' -d 'api_paste_code=test' -d 'api_option=paste' "https://pastebin.com/api/api_post.php"    
    # headers = {"Content-Type": "application/json; charset=utf8"}
    # r = requests.post(url,headers=headers, data=payload)
    return requests.post(url, data=payload)
    