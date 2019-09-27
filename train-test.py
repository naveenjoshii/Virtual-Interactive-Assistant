import cv2
import os
import sys
from time import sleep
from imutils.video import VideoStream
import imutils
import numpy as np
import time
import datetime
import speech as sp
from pymongo import MongoClient
import pyttsx3
import webbrowser
import datacreation
import smtplib
import random
import urllib.request
import urllib.parse
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
from multiprocessing import Process
import os
import re

import sys
engine = pyttsx3.init()

#client = wolframalpha.Client('XLXUE2-AUUG43RE27')

voices = engine.getProperty('voices')
#print(voices)
engine.setProperty('voice', voices[0].id)
def sing():
	time_delays = [0.1, 0.1, 0.1, 0.5, 0.2, 0.1, 0.1]
	song_lyrics = "thesong"

	print("Let's sing a song...")
	for song_char, char_delay in zip(song_lyrics, time_delays):
		sleep(char_delay)
		speak(song_char)

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

def detect_face (img):
	 try:
		 gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
	 except:
		 gray = img
	 face_cas = cv2.CascadeClassifier ('haarcascade_frontalface_default.xml')
	 faces = face_cas.detectMultiScale (gray, scaleFactor=1.3, minNeighbors=4)
	 if (len (faces) == 0):
		 return gray
	 else:
		 x,y,w,h = faces[0]
	 return gray[y:y+h,x:x+w]
def vid():
	detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	print("starting video stream...")
	vs = VideoStream(src=0).start()
	#time.sleep(1.0)
	total=0
	while True:
		 frame = vs.read()
		 #frame = imutils.resize(frame, width=400)
		 img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		 rects = detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
		 for (x, y, w, h) in rects:
			 if len(rects)==0:
				 pass
			 else:
				 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	cv2.imshow("Frame", frame)
'''def runInParallel(*fns):
	proc = []
	for fn in fns:
		p = Process(target=fn)
		p.start()
		proc.append(p)
	for p in proc:
		p.join()'''
def prepare_training_data(data_folder_path):
	 dirs = os.listdir(data_folder_path)
	 faces = [] #images
	 ids = [] # ids
	 labels = [] # names
	 dic={}
	 for emp_name in dirs:
		 emp_dir_path = data_folder_path + "/" + emp_name
		 emp_images_names = os.listdir(emp_dir_path)
		 for image_name in emp_images_names[:-1]:
			 lid = image_name.split("-")[1]
			 label = image_name.split("-")[0]
			 image_path = emp_dir_path + "/" + image_name
			 image = cv2.imread(image_path)
			 cv2.imshow("Training on image...", image)
			 cv2.waitKey(100)
			 image = np.array(image, dtype=np.uint8)
			 face = detect_face(image)

			 if not face is None:
				 faces.append(face)
			 labels.append(label)
			 ids.append(int(lid))
			 dic[int(lid)]=label

			 cv2.waitKey(1)
			 cv2.destroyAllWindows()
	 return faces,ids,dic

def predict(test_img):
	img = test_img.copy()
	face = detect_face(img)
	lid = face_recognizer.predict(face)
	return lid
'''def insert_new(img,total):
	p = os.path.sep.join(["pics","Guest","{}.png".format("Guest"+str(total).zfill(1))])
	cv2.imwrite(p,img)
	guest_col.insert_one({"name":"Guest"+str(total),"time":str(datetime.datetime.now())})
	'''
def myCommand():
	# r = sr.Recognizer()
	# with sr.Microphone() as source:
	# 	r.adjust_for_ambient_noise(source)
	# 	print("Listening...")
	# 	r.pause_threshold =  2
	# 	audio = r.listen(source)
	# try:
	# 	query = r.recognize_google(audio, language='en-in')
	# 	print('User: ' + query + '\n')
	#
	# except sr.UnknownValueError:
	# 	speak('Sorry sir! I didn\'t get that! Try typing the command!')
	# 	query = str(input('Command: '))
	query = str(input('Command: '))
	return query
def initializeQuery(name):
		speak('Hello '+name +' How May i help you?')
		while True:
			b=0

			query = myCommand()
			query = query.lower()

			if 'open youtube' in query:
				speak('roger that')
				webbrowser.open('www.youtube.com')
			elif 'sing' in query:
				sing()
			elif 'play' in query:
				speak('roger that')
				query_string = urllib.parse.urlencode({"search_query" : query.split()[1:len(query)-1]})
				html_cont = urllib.request.urlopen("http://www.youtube.com/results?"+query_string)
				search_res = re.findall(r'href=\"\/watch\?v=(.{11})', html_cont.read().decode())
				webbrowser.open_new("http://www.youtube.com/watch?v={}".format(search_res[0]))
			elif 'open google' in query:
				speak('roger that')
				webbrowser.open('www.google.co.in')
			elif 'where is' in query:
				speak('roger that')
				s = "".join(query.split()[2:len(query)-1])
				print(s)
				webbrowser.open('https://www.google.com/maps/place/'+s)

			elif 'open gmail' in query:
				speak('roger that')
				webbrowser.open('www.gmail.com')

			elif query in ["what\'s up",'how are you']:
				stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
				speak(random.choice(stMsgs))
				print(random.choice(stMsgs))

			elif query in ['nothing','abort','stop','exit','bye','goodbye']:
				speak('That\'s a nice talk with you ')
				speak('Bye Sir, have a good day.')
				b=1

			elif query in ['hola','hi','hello','hey']:
				speak('Hello')

			else:
				try:
					query = query
					speak('Searching...')
					results = wikipedia.summary(query,sentences=2)
					speak('Got it.')
                    #speak('WIKIPEDIA says - ')
					speak(results)
				except:
					webbrowser.open('https://www.google.co.in/search?ei=EZXCXMHXFavEz7sP-LSL8Ag&q='+query)
			if b==1:
				break
			speak('Next Command! Sir!')

def recognizing():
	detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	print("starting video stream...")
	vs = VideoStream(src=0).start()
	#time.sleep(1.0)
	total=0
	s=''
	f=0
	waiting=1;
	while True:
		 frame = vs.read()
		 #frame = imutils.resize(frame, width=400)
		 img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		 rects = detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

		 for (x, y, w, h) in rects:
			 if len(rects)==0:
				 pass
			 else:
				 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				 lid,cfd = predict(img[y:y+h,x:x+w])
				 print(lid)
				 if cfd > 75 and s!=dic[lid]:
					 print(dic[lid])
					 s=dic[lid]
					 #runInParallel(initializeQuery(dic[lid]),vid)
					 initializeQuery(dic[lid])
				 else:
					 waiting=waiting+1
				 if waiting ==100 or waiting ==200:
					 speak('Do You want any help ? '+s)
					 print('Do You want any help ? '+s)
					 q = myCommand()
					 q=q.lower()
					 if 'yes' in q:
						 initializeQuery(dic[lid])
						 s=''
						 waiting=1
					 else:
						 f=f+1
						 speak('okay fine')
						 print('okay fine')
						 if f==2:
							 break
					 #sp.tts("Hello "+dic[lid],lang)
		 cv2.imshow("Frame",frame)
		 k=cv2.waitKey(100) & 0xFF
		 if ord('q')==k:
			 break
	cv2.destroyAllWindows()
	print("video streaming stopped")
	vs.stop()


db = MongoClient().Attendance
col = db.rollcall
guest_col = db.Guest
greetMe()
speak('I am your assistant ')
print('I am your assistant ')

count = datacreation.maiin()

if count is True:
	print("Preparing data...")
	faces,ids,dic = prepare_training_data("D:/GVP-Assistant/Assistant-v1/OutputImages")
	print("Data prepared")
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()#create our LBPH face recognizer
	'''for above line to work install the dependency as follows:pip install opencv-contrib-python'''
	print("training on data")
	face_recognizer.train(faces, np.array(ids))
	print("training succesfully finished")
	recognizing()
	'''start the video stream to recignize and mark attendance'''
