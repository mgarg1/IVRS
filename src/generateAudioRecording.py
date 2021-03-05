# -*- coding: utf-8 -*-
from gtts import gTTS
import os
from dateToNum import key2file,key2fileWithoutMap,audioRecordingsPath,audioRecordingshindiNumbersPath
import datetime

#converts 6789 -> '६७८९'
def getHindiNumberString(num):
    if type(num) !=  int:
        print('Error in getHindiNumberString - not an int')
        return ''

    num_map = ['०','१','२','३','४','५','६','७','८','९']
    hindi_num = ''
    if num == 0:
        hindi_num = num_map[0]
   
    while num != 0:
        hindi_num = num_map[num % 10] + hindi_num
        num = int(num/10)
    
    # print(hindi_num)
    return hindi_num

def getHindiDate(date,month,year=None):
    month_map  =  ['','जनवरी','फरवरी','मार्च','अप्रैल','मई','जून','जुलाई','अगस्त','सेप्टैंबर','अक्टूबर','नवम्बर','दिसम्बर']
    day_hindi = getHindiNumberString(date)
    day_hindi = day_hindi + ' ' + month_map[month]
    if year:
        day_hindi = day_hindi + ' ' + getHindiNumberString(year)
    
    return day_hindi

def generate_gtts_file(text_string,filename):
    try:
        audioObj = gTTS(text=text_string, lang='hi', slow=False)
    except:
        print('exeption occurred')

    audio_file = (filename+".mp4")    
    #saving the audio_file '<file_input>.mp4' into the directory
    audioObj.save(os.path.join(audioRecordingshindiNumbersPath,audio_file))
    # os.system(audio_file)

def generateHindiAudioFromDate(dateTimeObj,includeYear=False):
    day = int(dateTimeObj.strftime('%d'))
    mon = int(dateTimeObj.strftime('%m'))
    yer = None
    dateFormat = '%d_%m'
    if includeYear:
        yer = int(dateTimeObj.strftime('%Y'))
        dateFormat = '%d_%m_%Y'

    hindi_date = getHindiDate(day,mon,yer)
    filename = dateTimeObj.strftime(dateFormat)
    generate_gtts_file(hindi_date,filename)

def generateOnlyYears(numOfYears):
    for i in range(0,numOfYears):
        hindiYear = getHindiNumberString(2020+i)
        generate_gtts_file(hindiYear,str(2020+i))


def generateAudioForNextDays(startDate,days):
    for i in range(0,days):
        newDate = startDate + datetime.timedelta(days=i)
        generateHindiAudioFromDate(newDate)

def generateOtherAudioFiles():
    # audioObj = gTTS(text='के लिए', lang='hi', slow=False)
    # audioObj.save(key2file('keliye'))

    # count_map = ['०','१','२','३','४','५','६','७','८','९']
    # for i in range(0,10):
    #     audioObj = gTTS(text=(str(count_map[i]) + ' दबाएं'), lang='hi', slow=False) 
    #     audioObj.save(key2fileWithoutMap(str(i)+'_dabayein.mp4'))

    # audioObj = gTTS(text='मयूरी हॉस्पिटल में आपका स्वागत है . अपॉइंटमेंट बुक करने के लिए एक दबाएं . किसी हॉस्पिटल कर्मचारी से बात करने के लिए दो दबाएं', lang='hi', slow=False) 
    # audioObj.save(key2file('welcomeState1'))

    audioObj = gTTS(text='आगे उपलब्ध आठ तारीखों में से एक का चुनाव करें', lang='hi', slow=False) 
    audioObj.save(key2file('bookInstr'))

    # audioObj = gTTS(text='आपने चुना है', lang='hi', slow=False) 
    # audioObj.save(key2file('confirmState1'))

    # audioObj = gTTS(text='कन्फर्म करने के लिए एक दबाएं . फिरसे चुनाव करने के लिए दो दबाएं', lang='hi', slow=False) 
    # audioObj.save(key2file('confirmState2'))

    # audioObj = gTTS(text='मयूरी हॉस्पिटल में आपका स्वागत है . आपका अपॉइंटमेंट, पहले से ही बुक है दिनांक', lang='hi', slow=False) 
    # audioObj.save(key2file('alreadyState1'))

    # audioObj = gTTS(text='इसे बदलने के लिए, एक दबाएं , इसे कैंसिल करने के लिए, दो दबाएं', lang='hi', slow=False) 
    # audioObj.save(key2file('alreadyState2'))

    # audioObj = gTTS(text='आपका अपॉइंटमेंट बुक हो चुका है . हमें कॉल करने के लिए धन्यवाद', lang='hi', slow=False) 
    # audioObj.save(key2file('booked'))

    # audioObj = gTTS(text='हमें कॉल करने के लिए धन्यवाद ... हमारे प्रतिनिधि जल्द ही आपको कॉलबैक करेंगे', lang='hi', slow=False) 
    # audioObj.save(key2file('callback'))

    # audioObj = gTTS(text='आपका अपॉइंटमेंट कैंसिल हो चुका है . हमें कॉल करने के लिए धन्यवाद', lang='hi', slow=False) 
    # audioObj.save(key2file('cancelled'))
     
    # audioObj = gTTS(text='आपने कोई विकल्प नहीं चुना है ... कृपया पुनः प्रयास करें', lang='hi')
    # audioObj.save(key2file('retry'))

    # audioObj = gTTS(text='आपने कोई विकल्प नहीं चुना है ...हमें कॉल करने के लिए धन्यवाद', lang='hi')
    # audioObj.save(key2file('timeout'))

def main():
    # # Leap Year to cover all recordings
    # startDate = datetime.datetime(2000, 1, 1, 0, 0)
    # generateAudioForNextDays(datetime.datetime.now(),366)
    # generateOnlyYears(10)
    generateOtherAudioFiles()

main()
