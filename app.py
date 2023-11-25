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


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stopThread = False
        self.recognizer = sr.Recognizer()

    def build(self):
        # create a Box Layout
        boxLayout = BoxLayout(orientation="vertical")

        # create a label for status display
        self.labelStatus = Label(text="Ready for recording...", font_size=24)

        # create a label for displaying the text from speech
        self.labelTextFromSpeech = Label(text="Text Here ...", font_size=36)

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
            self.labelStatus.text = "Слушане..."
            try:
                with sr.Microphone() as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=6)
            except sr.WaitTimeoutError:
                continue

            if not audio:
                continue

            # when audio is recorded and trascripted if the text is "Хей Гери" start recording
            try:
                text = self.recognizer.recognize_google(audio, language="bg-BG")
                print("You said:", text)
                if text == "Хей Гери":
                    self.labelStatus.text = "Здравей Христо..."
                    break
            except sr.UnknownValueError:
                print("Unable to recognize speech")
            except sr.RequestError as e:
                print(f"Error: {e}")
            
            time.sleep(0.02)

    async def set_recording(self):
        while not self.stopThread:
            self.labelStatus.text = "Какво ще желаеш?..."
            try:
                with sr.Microphone() as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=6)
            except sr.WaitTimeoutError:
                continue        
            if not audio:
                continue
            # when audio is recorded and trascripted if the text is "Спри" stop recording
            try:
                text = self.recognizer.recognize_google(audio, language="bg-BG")
                print("You said:", text)
                if text == "спри":
                    self.labelStatus.text = "Довиждане..."
                    break
                else:
                    self.labelTextFromSpeech.text = text
            except sr.UnknownValueError:
                print("Unable to recognize speech")
            except sr.RequestError as e:
                print(f"Error: {e}")
            time.sleep(0.02)

def main():
    MyApp().run()

if __name__ == '__main__':
    main()