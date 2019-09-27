import nltk
import numpy as np
import random
import string
import speech_recognition as sr
from gtts import gTTS
import pyglet
import time,os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
lang='en'
flag=0
def tts(text,lang):
    file = gTTS(text=text,lang=lang)
    filename='abc'
    file.save(filename)
    music  = pyglet.media.load(filename,streaming=False)
    music.play()
    time.sleep(music.duration)
    os.remove(filename)
#tts('I will answer your queries about GVP. If you want to exit, type Bye!',lang)
#print("GVPBOT: I will answer your queries about GVP. If you want to exit, type Bye!")
def spt(flag):

    text=''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        lang='en'
        if(flag is 0):
            tts('How can i help you ?',lang)
            audio = r.listen(source)
        elif(flag>0 and flag <4):
            tts('speak now',lang)
            audio = r.listen(source)
        elif(flag is 4 or flag is 5):
            tts('Do you want to continue ?',lang)
            audio = r.listen(source)
        else:
            audio = r.listen(source)
        # tts('wait a moment',lang)
    try:
        text = r.recognize_google(audio)
        if(text=='yes' and (flag is 4 or flag is 5)):
            return text
        elif(text=='no'and (flag is 4 or flag is 5)):
            return text

        print('YOU :'+text)
    except Exception as e:
        print(e)
    return text
# Create a new trainer for the chatbot
#trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
#trainer.train("chatterbot.corpus.english")
tts('Hi,I am GVP BOT ,',lang)

while True:
    s = str(spt(flag))
    b=str(chatbot.get_response(s))
    if(b=='no'):
        break
    print("GVP BOT: "+b)
    tts(b,lang)
    print(flag)
    flag=flag+1


# Get a response to an input statement
f=open('gayatri.txt','r',errors = 'ignore')
raw=f.read()
raw=raw.lower()# converts to lowercase
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences
word_tokens = nltk.word_tokenize(raw)# converts to list of word
lemmer = nltk.stem.WordNetLemmatizer()
#WordNet is a semantically-oriented dictionary of English included in NLTK.
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "whats up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):

    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response
flag=True
while(flag==True):
    user_response = spt()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            tts("Bot: You are welcome..",lang)
        else:
            if(greeting(user_response)!=None):
                t = greeting(user_response)
                tts(t,lang)
                print("Bot: "+t)
                #print("ROBO: "+greeting(user_response))
            else:
                #print("ROBO: ",end="")
                g = response(user_response)
                tts(g,lang)
                print("Bot: "+g)
                sent_tokens.remove(user_response)
    else:
        flag=False
        tts('Bye! take care..',lang)
        print("ROBO: Bye! take care..")
