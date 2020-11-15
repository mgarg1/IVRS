"""
install gTTS module, turn the internet on and run this file in your own machine.
Don't forget to like it!
version : 1.0
author : Shibaayan
Suggestion for improvement and modofication quite appreciated.

"""

#importing gTTS module for text to speech
from gtts import gTTS
#importing os
import os

#introductions for user
print("Now this text to speech conversion is available in Indian languages!")

while True:
    #introduction for user
    print("\nEnter the language first in which you want to run this 'text to speech' program\nHere are the options for you!\n")
    print("use '1' for hindi\nuse '2' for arbic\nuse '3' for bengali\nuse '4' for tamil\nuse '5' for UK-English\nuse '6' for US-English\nuse '0' to close")
    print("ALWAYS WRITE YOUR TEXT ACCORDING TO YOUR LANGUAGE PHONETICS\n")

    #available gTTS-language-codes taken
    options = ["hi","ar","bn","ta","en-uk","en-us"]

    #taking the preference
    pref = int(input("Now please enter your preference : "))
    
    #taking the language for gTTS text-to-speech operation
    if pref<=5:
        language = options[pref-1]
    if pref==0:
        exit(0)
    
    #main input by user for text-to-speech operation
    mytext = input("Enter a text : ")
     
    #creating an object for gTTS text-to-speech operation
    myobj = gTTS(text=mytext, lang=language, slow=False)

    #saving as a audio_file and txt_file inside a directory
    def save_file():
        #entering the general file name
        #this file_input will be used to create a directory and the input text file and output audiofile inside the directory                        
        file_input = input("Enter a file name  : ")
        audio_file = (file_input+".mp4")
        
        #creating the directory
        os.mkdir(file_input) 
        
        #getting into the directory
        os.chdir(os.getcwd()+'/'+file_input)
        
        #saving the audio_file '<file_input>.mp4' into the directory
        myobj.save(audio_file)
        
        #running the audio_file '<file_input>.mp4'                    //was not working in ubuntu! still you will get the files
        os.system(audio_file)
        
        #opening,writing and closing the text file '<file_input>.txt'
        txt_file = open(file_input+".txt","w")
        txt_file.write(mytext)
        txt_file.close()
        exit(0)
    
    #just taking a preference
    a = input("\nSave and then collect the files from directory\nDo you want to save as a audio file(y/n) : ")
    
    #if input is 'y' or 'Y' process runs to save the file
    if a == 'y' or a == 'Y':
        save_file()
    else:
        a = input("Press 0 to close : ")
        exit(0)
    if pref==0:
        exit(0)