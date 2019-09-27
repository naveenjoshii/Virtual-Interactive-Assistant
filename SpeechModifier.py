import numpy as np
import pyttsx3
import speech_recognition as sr
#Create an object as shown below −
engine = pyttsx3.init('sapi5')
def speak(audio):
	print('Computer: ' + audio)
	engine.say(audio)
	engine.runAndWait()
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Listening...")
    #r.dynamic_energy_threshold
    r.energy_threshold = 300
    r.pause_threshold = 0.8
    audio = r.listen(source)
try:
    query = r.recognize_google(audio, language='en-in')
    print('User: ' + query + '\n')
    speak(query)

except sr.UnknownValueError:
    speak('Sorry sir! I didn\'t get that! Try typing the command!')
    query = str(input('Command: '))
#Please Say Something:
#You said:
