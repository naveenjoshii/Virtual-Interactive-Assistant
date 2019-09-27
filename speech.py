import speech_recognition as sr
from gtts import gTTS
import pyglet
import time,os

def tts(text,lang):
    file = gTTS(text=text,lang=lang)
    filename='abc'
    file.save(filename)
    music  = pyglet.media.load(filename,streaming=False)
    music.play()

# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os

# The text that you want to convert to audio
mytext = 'Easier than game engines. More interactive than video streaming. More creative than scanning. Immersive on both VR and web-phone. Create with any camera. Open source. Static build, so no hosting lock-in. Simple JSON markup. Extend with custom code. For starters'

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome
myobj.save("welcome.mp3")

# Playing the converted file
os.system("welcome.mp3")
