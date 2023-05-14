import speech_recognition as sr

# create a recognizer instance
r = sr.Recognizer()

# create a microphone instance
mic = sr.Microphone(device_index=0)

# listen to the microphone and transcribe speech
with mic as source:
    print("Say something!")
    audio = r.listen(source)

text = r.recognize_google(audio, language="bg-BG")
print("You said:", text)
