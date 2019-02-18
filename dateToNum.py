def numToWords(num,join=True):
    '''words = {} convert an integer number into words'''
    units = ['','one','two','three','four','five','six','seven','eight','nine']
    teens = ['','eleven','twelve','thirteen','fourteen','fifteen','sixteen', \
             'seventeen','eighteen','nineteen']
    tens = ['','ten','twenty','thirty','forty','fifty','sixty','seventy', \
            'eighty','ninety']
    thousands = ['','thousand','million','billion','trillion','quadrillion', \
                 'quintillion','sextillion','septillion','octillion', \
                 'nonillion','decillion','undecillion','duodecillion', \
                 'tredecillion','quattuordecillion','sexdecillion', \
                 'septendecillion','octodecillion','novemdecillion', \
                 'vigintillion']
    words = []
    if num==0: words.append('zero')
    else:
        numStr = '%d'%num
        numStrLen = len(numStr)
        groups = int((numStrLen+2)/3)
        numStr = numStr.zfill(groups*3)
        for i in range(0,groups*3,3):
            h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
            g = int(groups-(i/3+1))
            if h>=1:
                words.append(units[h])
                words.append('hundred')
            if t>1:
                words.append(tens[t])
                if u>=1: words.append(units[u])
            elif t==1:
                if u>=1: words.append(teens[u])
                else: words.append(tens[t])
            else:
                if u>=1: words.append(units[u])
            if (g>=1) and ((h+t+u)>0): words.append(thousands[g])
    if join: return ' '.join(words)
    return words

#example usages:
# print numToWords(0)
# print numToWords(11)
# print numToWords(110)
# print numToWords(1001000025)
# print numToWords(123456789012)

import os

def getFileFromNum(wordToConvert):
    dirname = './hindinumbers/'
    return dirname + wordToConvert + '_hindi.mp3'



def playWord(filename):
    cmdToRun = 'nvlc  %s  --play-and-exit --no-osd' % (filename)
    print(filename)
    if os.path.isfile(filename):
        print ("File exist")
        os.system(cmdToRun)
    else:
        print ("word File not exist")

def date2audioFiles(bookDate):
    from datetime import datetime
    datetime_obj = datetime.strptime(bookDate,'%d-%B-%Y')

    #print(numToWords(13))
    day = numToWords(int(datetime_obj.day),False)
    month = datetime_obj.strftime('%B')
    year = numToWords(int(datetime_obj.year),False)

    dateFileList = day + [month] + year
    dateFileList = [getFileFromNum(x) for x in dateFileList]
    #dateFileList = map(getFileFromNum,dateFileList)
    return dateFileList

aa = date2audioFiles('12-April-2019')
print(aa)


