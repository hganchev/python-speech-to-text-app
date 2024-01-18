# pip install pydub
# pip install ffmpeg-downloader
# ffdl install --add-path

import speech_recognition as sr

# FILEPATH: /e:/MyProjects/Projects/GitHub/python-speech-to-text-app/fileTranscription.py
AUDIO_FILE = "./audio/audio4.m4a"
AUDIO_FILE_WAV = "./audio/audio4.wav"

# Load the audio file
from pydub import AudioSegment
audio = AudioSegment.from_file(AUDIO_FILE, format='m4a')

# check audio file time
print(audio.duration_seconds / 60)

# check audio file volume
print(audio.dBFS)

# boost volume
audio = audio + (abs(audio.dBFS) - 10)
print(audio.dBFS)
    

# # export modified audio file
# audio.export(out_f=AUDIO_FILE_WAV,
#                 format="wav",
#                 bitrate="192k",
#                 parameters=["-ac", "1", "-ar", "16000"])

# # Perform speech recognition  
# r = sr.Recognizer()
# with sr.AudioFile(AUDIO_FILE_WAV) as source:
#     # Read the entire audio file
#     audio = r.record(source)

# try:
#     transcription = r.recognize_google(audio, language="bg-BG")
# except sr.UnknownValueError:
#     pass
# # Print the transcription
# print(transcription)

# Create a recognizer object for all chunks
r = sr.Recognizer()

# Split the audio file into chunks accirding to the duration of the audio file and export them as wav files
arrChunks = []
for i in range(int(audio.duration_seconds / 60)):
    chunk = audio[i*60*1000:(i+1)*60*1000]
    arrChunks.append(chunk)

for i, chunk in enumerate(arrChunks):
    chunk.export(f"./audio/audio{i}.wav", format="wav", bitrate="192k", parameters=["-ac", "1", "-ar", "16000"])

    # Perform speech recognition on each chunk
    with sr.AudioFile(f"./audio/audio{i}.wav") as source:
        # Read the entire audio file
        audio = r.record(source)
    try:
        transcription = r.recognize_google(audio, language="bg-BG")
    except sr.UnknownValueError:
        pass

    # Print the transcription
    print(transcription)
