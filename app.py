import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

import asyncio
import threading
import time

import speech_recognition as sr 


class MyApp(App):
    def build(self):
        self.stop_listening = False

        Window.bind(on_request_close=self.exit_on_request)

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
    
    def exit_on_request(self, *args):    
        # stop listening
        self.stop_listening = True 
        # stop the thread
        self.thread.join()
        # stop the app
        App.get_running_app().stop()
        return True

    def start_recording(self):  
        # create and run the event loop with the start_listening coroutine until the app is closed
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.start_listening())
        loop.close()

    async def start_listening(self):
        self.recognizer = sr.Recognizer()       
        while not self.stop_listening: 
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=6)
            self.labelStatus.text = "Слушане..."
            if not audio:
                continue

            # when audio is recorded and trascripted if the text is "Хей Гери" start recording
            try:
                text = self.recognizer.recognize_google(audio, language="bg-BG")
                print("You said:", text)
                if text == "Хей Гери":
                    self.labelStatus.text = "Здравей Христо..."
                    await self.set_recording()
            except sr.UnknownValueError:
                print("Unable to recognize speech")
            except sr.RequestError as e:
                print(f"Error: {e}")
            
            time.sleep(0.02)

    async def set_recording(self):
        while not self.stop_listening:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=6)
            self.labelStatus.text = "Какво ще желаеш?..."
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

if __name__ == '__main__':
    MyApp().run()