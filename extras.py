elif 'email' in query:
    speak('Who is the recipient? ')
    recipient = myCommand()

    if 'me' in recipient:
        try:
            speak('What should I say? ')
            content = myCommand()

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login("kondetinaveen1113@gmail.com", 'naveenjoshi123')
            server.sendmail('Your_Username', "Recipient_Username", content)
            server.close()
            speak('Email sent!')

        except:
            speak('Sorry Sir! I am unable to send your message at this moment!')
elif 'play music' in query:
    music_folder = 'C:/Users/ashok/Pictures/videos'
    music1='3_(Telugu)_-_Yedhalo_Oka_Mounam_Video___Dhanush,_Shruti___Anirudh'
    music2='Charlie_Puth_-_We_Don_t_Talk_Anymore_(feat._Selena_Gomez)_[Official_Video]'
    music = [music1, music2]
    random_music = music_folder + random.choice(music) + '.mp4'
    os.system(random_music)

    speak('Okay, here is your music! Enjoy!')
