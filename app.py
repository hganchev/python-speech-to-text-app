import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import asyncio
import threading
import time

import speech_recognition as sr 


class MyApp(App):
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
        self.thread = threading.Thread(target=self.start_recording)
        self.thread.start()

        return boxLayout

    def start_recording(self):  
        recognizer = sr.Recognizer()       
        while True: 
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)
            self.labelStatus.text = "Listening..."
            if not audio:
                continue

            self.labelStatus.text = "Processing..."           
            try:
                text = recognizer.recognize_google(audio, language="bg-BG")
                self.labelTextFromSpeech.text = text
                print("You said:", text)
            except sr.UnknownValueError:
                print("Unable to recognize speech")
            except sr.RequestError as e:
                print(f"Error: {e}")
            time.sleep(0.02)

if __name__ == '__main__':
    MyApp().run()