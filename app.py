# pip install kivy --upgrade --pre
# pip install SpeechRecognition
# pip install PyAudio
# pip install gtts
# pip install playsound==1.2.2
import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

import asyncio
import threading
import time

import speech_recognition as sr 
from gtts import gTTS
from playsound import playsound

from enum import Enum

class Catalog(Enum):
    pokupki = 665


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stopThread = False
        self.recognizer = sr.Recognizer()

    def build(self):
        # create a Box Layout
        boxLayout = BoxLayout(orientation="vertical")

        # create a label for status display
        self.labelStatus = Label(text="Кажете нещо...", font_size=24)

        # create a label for displaying the text from speech
        self.labelTextFromSpeech = Label(text="Текст тука ...", font_size=36)

        boxLayout.add_widget(self.labelStatus)
        boxLayout.add_widget(self.labelTextFromSpeech)

        # start a new thread that will listen to the microphone and transcribe speech
        threading.Thread(target=self.start_recording).start()

        return boxLayout
    
    def on_stop(self):
        # stop listening when the app closes
        self.stopThread = True
        return True

    def start_recording(self):  
        asyncio.run(self.start_listening())
        asyncio.run(self.set_recording())

    async def start_listening(self):
        while not self.stopThread:            
            try:
                # for mic in sr.Microphone.list_microphone_names():
                #     print(mic)
                with sr.Microphone() as source:
                    # self.recognizer.adjust_for_ambient_noise(source=source)
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                continue

            if not audio:
                continue

            # when audio is recorded and trascripted if the text is "Хей Гери" start recording
            try:
                text = self.recognizer.recognize_google(audio, language="bg-BG")
                print("You said:", text.lower())
                if text.lower() == "хей гери":
                    self.speech("Здравей Христо, с какво мога да ти помогна?")
                    break
            except sr.UnknownValueError:
                print("Unable to recognize speech")
                self.speech("Не мога да разбера")
            except sr.RequestError as e:
                print(f"Error: {e}")
            
            time.sleep(0.1)

    async def set_recording(self):
        while not self.stopThread:          
            try:
                with sr.Microphone() as source:
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                continue        
            if not audio:
                continue
            # when audio is recorded and trascripted if the text is "Спри" stop recording
            try:
                text = self.recognizer.recognize_google(audio, language="bg-BG")
                print("You said:", text.lower())
                if text.lower() == "довиждане" or text.lower() == "чао":
                    self.speech("Довиждане...")
                    break
                else:
                    self.labelTextFromSpeech.text = text
            except sr.UnknownValueError:
                print("не мога да разбера")
                self.speech("Не мога да разбера")
            except sr.RequestError as e:
                print(f"Error: {e}")
            time.sleep(0.02)

    def speech(self, text : str):
        self.labelStatus.text = text
        speech = gTTS(text=text, lang="bg")
        speech.save("text.mp3")
        playsound("text.mp3")
        os.remove("text.mp3")

def main():
    MyApp().run()

if __name__ == '__main__':
    main()