# -*- coding: utf-8 -*-
from gtts import gTTS
import os
from dateToNum import key2file,key2fileWithoutMap,audioRecordingsPath,audioRecordingshindiNumbersPath
import datetime

def getHindiDate(date,month,year):
    date_map = ['०','१','२','३','४','५','६','७','८','९',
    '१०','११','१२','१३','१४','१५','१६','१७','१८','१९',
    '२०','२१','२२','२३','२४','२५','२६','२७','२८','२९',
    '३०','३१']

    month_map  =  ['','जनवरी','फरवरी','मार्च','अप्रैल','मई','जून','जुलाई','अगस्त','सेप्टैंबर','अक्टूबर','नवम्बर','दिसम्बर']

    year_map = ['२०२०','२०२१','२०२२','२०२३']

    day_hindi = str(date_map[date])
    day_hindi = day_hindi + ' ' + str(month_map[month])
    day_hindi = day_hindi + ' ' + str(year_map[year])
    return day_hindi

def generateHindiAudioFromDate(dateTimeObj):
    day = int(dateTimeObj.strftime('%d'))
    mon = int(dateTimeObj.strftime('%m'))
    yer = int(dateTimeObj.strftime('%Y')) - 2020

    hindi_date = getHindiDate(day,mon,yer)
    try:
        audioObj = gTTS(text=hindi_date, lang='hi', slow=False)
    except:
        print('exeption occured')
    filename = dateTimeObj.strftime('%d_%m_%Y')
    audio_file = (filename+".mp4")    
    #saving the audio_file '<file_input>.mp4' into the directory
    audioObj.save(os.path.join(audioRecordingshindiNumbersPath,audio_file))
    # os.system(audio_file)

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
    #     audioObj.save(str(i)+'_hindi.mp4')

    # audioObj = gTTS(text='मयूरी हॉस्पिटल में आपका स्वागत है . अपॉइंटमेंट बुक करने के लिए एक दबाएं . किसी हॉस्पिटल कर्मचारी से बात करने के लिए दो दबाएं', lang='hi', slow=False) 
    # audioObj.save(key2file('welcomeState1'))

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
    generateAudioForNextDays(datetime.datetime.now(),31)
    #generateOtherAudioFiles()


main()
