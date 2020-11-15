# """
# install gTTS module, turn the internet on and run this file in your own machine.
# Don't forget to like it!
# version : 1.0
# author : Shibaayan
# Suggestion for improvement and modofication quite appreciated.

# """

#importing gTTS module for text to speech
from gtts import gTTS
#importing os
import os


# #saving as a audio_file and txt_file inside a directory
# def save_file(audio_binary,file_input='audio1'):
#     #entering the general file name
#     #this file_input will be used to create a directory and the input text file and output audiofile inside the directory                        
#     # file_input = input("Enter a file name  : ")
#     audio_file = (file_input+".mp4")
    
#     #creating the directory
#     # os.mkdir(file_input) 
    
#     #getting into the directory
#     # os.chdir(os.getcwd()+'/'+file_input)
    
#     #saving the audio_file '<file_input>.mp4' into the directory
#     audio_binary.save(audio_file)
    
#     #running the audio_file '<file_input>.mp4'                    //was not working in ubuntu! still you will get the files
#     os.system(audio_file)
    
#     #opening,writing and closing the text file '<file_input>.txt'
#     # txt_file = open(file_input+".txt","w+")
#     # txt_file.write(mytext)
#     # txt_file.close()
#     # exit(0)

# def save_file(audio_binary,file_input='audio1'):
#     audio_file = (file_input+".mp4")    
#     #saving the audio_file '<file_input>.mp4' into the directory
#     audio_binary.save(audio_file)

# myobj = gTTS(text='२ जनवरी २०२०', lang='hi', slow=False)
# save_file(myobj)


import datetime
import os

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
    audioObj.save(audio_file)
    # os.system(audio_file)

def main():
    x = datetime.datetime.now()
    for i in range(0,31):
        newDate = x + datetime.timedelta(days=i)
        generateHindiAudioFromDate(newDate)

# main()

audioObj = gTTS(text='के लिए', lang='hi', slow=False) 
audioObj.save('keliye.mp4')

# count_map = ['०','१','२','३','४','५','६','७','८','९']
# for i in range(0,10):
#     audioObj = gTTS(text=(str(count_map[i]) + ' दबाएं'), lang='hi', slow=False) 
#     audioObj.save(str(i)+'_hindi.mp4')

# audioObj = gTTS(text='मयूरी हॉस्पिटल में आपका स्वागत है . अपॉइंटमेंट बुक करने के लिए एक दबाएं . किसी हॉस्पिटल कर्मचारी से बात करने के लिए दो दबाएं', lang='hi', slow=False) 
# audioObj.save('welcomeStateMsg.mp4')

# audioObj = gTTS(text='आपने चुना है', lang='hi', slow=False) 
# audioObj.save('confirmState1.mp4')

# audioObj = gTTS(text='कन्फर्म करने के लिए एक दबाएं . फिरसे चुनाव करने के लिए दो दबाएं', lang='hi', slow=False) 
# audioObj.save('confirmState2.mp4')

audioObj = gTTS(text='आपका अपॉइंटमेंट पहले से ही बुक है दिनांक', lang='hi', slow=False) 
audioObj.save('alreadyState1.mp4')

audioObj = gTTS(text='के लिए  ,  इसे  बदलने के लिए, एक दबाएं , इस कॉल को यही बंद करने के लिए, दो दबाएं', lang='hi', slow=False) 
audioObj.save('alreadyState2.mp4')
 