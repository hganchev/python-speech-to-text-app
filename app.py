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
    def on_stop(self):
        self.stopThread = True
        print("Stopping thread...")
        return True
    
    def build(self):
        # initialize variables
        self.startRecording = True
        self.stopThread = False

        # create a Box Layout
        boxLayout = BoxLayout(orientation="vertical")

        # create a button with text "Record" and bind it to the record() method
        buttonRecord = Button(text="Record", on_press=self.on_record_press)

        # create a label for status display
        self.labelStatus = Label(text="Ready for recording...", font_size=24)

        # create a label for displaying the text from speech
        self.labelTextFromSpeech = Label(text="Press the button to record", font_size=36)

        boxLayout.add_widget(buttonRecord)
        boxLayout.add_widget(self.labelStatus)
        boxLayout.add_widget(self.labelTextFromSpeech)

        # start a new thread that will listen to the microphone and transcribe speech
        self.thread = threading.Thread(target=self.start_recording)
        self.thread.start()

        return boxLayout
    
    # record press method that records the speech and displays it in the labelText
    def on_record_press(self, instance):
        self.startRecording = not self.startRecording
        print("Recording started" if self.startRecording else "Recording stopped")


    def start_recording(self):  
        recognizer = sr.Recognizer()
        while not self.stopThread:
            if self.startRecording:
                self.labelStatus.text = "Recording..."
                print("Recording...")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)

                try:
                    text = recognizer.recognize_google(audio, language="bg-BG")
                    self.labelTextFromSpeech.text = text
                    print("You said:", text)
                except sr.UnknownValueError:
                    print("Unable to recognize speech")
                except sr.RequestError as e:
                    print(f"Error: {e}")
            else:
                self.labelStatus.text = "Press Record for recording..."
            time.sleep(0.1)

if __name__ == '__main__':
    MyApp().run()