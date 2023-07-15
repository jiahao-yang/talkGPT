import pyttsx3

engine = pyttsx3.init("sapi5")
#voices = engine.getProperty("voices")
#engine.setProperty("voice", voices[0].id)
engine.setProperty("voice", "en")

voices = engine.getProperty('voices')
for voice in voices:
    print ('id = {} \nname = {} \n'.format(voice.id, voice.name))

#engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0') 
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-GB_HAZEL_11.0')

engine.say("The result of 1+1 is 2")

engine.runAndWait()