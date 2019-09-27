from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import shutil
import numpy as np
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs

db = MongoClient().Attendance #connects to localhost by default
dic={}
count=1
fid=[]
fs1 = gridfs.GridFS(db)
name = ''
def capture(count):
	# Load the Haar cascades
	detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)
	total=0
	owd=os.getcwd()
	os.chdir('Images')
	os.makedirs(str(count).zfill(3))
	os.chdir(owd)
	name = input("enter your name")
	dic[count]=name
	print("images are being captured please wait...")
	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rects = detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
		for (x, y, w, h) in rects:
			 if len(rects)==0:
				 pass
			 else:
				 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				 p = os.path.sep.join(['Images',str(count).zfill(3),"{}.png".format(str(total).zfill(1))])
				 cv2.imwrite(p,img[y:y+h,x:x+w])
				 fid.append(fs1.put(open(p,'rb').read(),filename=name+str(list(dic.keys())[list(dic.values()).index(name)])))
				 total += 1
		cv2.imshow("Frame", frame)
		cv2.waitKey(1)
		if total==30:
			break
	cv2.destroyAllWindows()
	vs.stop()
	print("images successfully captured and stored")



def getimg():
	# retrieve what was just stored.
	total=1
	owd=os.getcwd()
	os.chdir('OutputImages')
	for i in range(len(fid)):
		fptr = fs1.get(fid[i])
		dat=fs1.find({"_id":fid[i]})
		for i in dat:
			label=''.join(filter(lambda x: not x.isdigit(), i.filename))
			lid=''.join(filter(lambda x: x.isdigit(), i.filename))
		outputdata = fptr.read()
		try:
			os.mkdir(label)
		except:
			pass
		p1 = label+"/"+str(label)+"-"+str(lid)+"-"+str(total)+".png"
		output= open(p1,"wb")
		output.write(outputdata)
		output.close()
		total+=1
	os.chdir(owd)
	print('images retrieved')
def maiin():
	n= int(input("How many persons you want to train"))
	if n != 0:
		res = True
	else:
		res= False
	count=1
	if res is True:
		while count<=n:
			capture(count)
			count+=1
		getimg()
	return res
#To retrive the images in database and store them in localsystem for training
