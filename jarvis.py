import pyttsx3
import webbrowser
import smtplib
import random
import urllib.request
import urllib.parse
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import re

import sys

engine = pyttsx3.init('sapi5')

#client = wolframalpha.Client('XLXUE2-AUUG43RE27')

voices = engine.getProperty('voices')
#print(voices)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    print('Computer: ' + audio)
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon!')

    if currentH >= 18 and currentH !=0:
        speak('Good Evening!')

greetMe()

speak('Hello Sir, I am your assistant')
speak('How may I help you?')


def myCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')

    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))

    return query


if __name__ == '__main__':

    while True:

        query = myCommand();
        query = query.lower()

        if 'open youtube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')
        elif 'play' in query:
            speak('okay')
            query_string = urllib.parse.urlencode({"search_query" : query.split()[1:len(query)-1]})
            html_cont = urllib.request.urlopen("http://www.youtube.com/results?"+query_string)
            search_res = re.findall(r'href=\"\/watch\?v=(.{11})', html_cont.read().decode())
            #print("http://www.youtube.com/watch?v=" + search_res[0])
            webbrowser.open_new("http://www.youtube.com/watch?v={}".format(search_res[0]))
        elif 'open google' in query:
            speak('okay')
            webbrowser.open('www.google.co.in')
        elif 'where is' in query:
            speak('okay')
            s = "".join(query.split()[2:len(query)-1])
            print(s)
            webbrowser.open('https://www.google.com/maps/place/'+s)

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')

        elif query in ["what\'s up",'how are you']:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))




        elif query in ['nothing','abort','stop','exit','bye','goodbye']:
            speak('That\'s a nice talk with you ')
            speak('Bye Sir, have a good day.')
            sys.exit()

        elif query in ['hello','hi','hello']:
            speak('Hello Sir')


        else:
            query = query
            speak('Searching...')
            try:
                results = wikipedia.summary(query, sentences=2)
                speak('Got it.')
                #speak('WIKIPEDIA says - ')
                speak(results)
                '''try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak('WOLFRAM-ALPHA says - ')
                    speak('Got it.')
                    speak(results)

                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it.')
                    speak('WIKIPEDIA says - ')
                    speak(results)'''

            except:
                webbrowser.open('https://www.google.co.in/search?ei=EZXCXMHXFavEz7sP-LSL8Ag&q='+query)

        speak('Next Command! Sir!')
