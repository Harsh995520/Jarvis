import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
import os
from gtts import gTTS
import tkinter as tk
from tkinter import messagebox
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set properties for male voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 for male, 1 for female
engine.setProperty('rate', 150)  # Speed of speech



def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}\n")
        
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except Exception as e:
            print("Sorry, I did not understand that. Could you please repeat?")
            return "None"
        return command.lower()

def speak(text):
        engine.say(text)
        engine.runAndWait()


def handle_command(command):
    if 'wikipedia' in command:
        speak("Searching Wikipedia...")
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif 'play video' in command:
        speak("Playing video")
        play_video(command)
    elif 'the time' in command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
    elif 'exit' in command or 'stop' in command:
        speak("Goodbye!")
        root.quit()
    else:
        speak("I am sorry, I don't understand that command.")


def start_listening():
    command = listen()
    if command != "None":
        handle_command(command)

def greet_user():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your Jarvis. How can I help you today?")

root = tk.Tk()
root.title("Jarvis")
root.geometry("400x200")

greet_user()


label = tk.Label(root, text="Press the button and speak a command", font=("Helvetica", 16))
label.pack(pady=20)

listen_button = tk.Button(root, text="Listen", command=start_listening, font=("Helvetica", 14), bg="blue", fg="white")
listen_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Helvetica", 14), bg="red", fg="white")
exit_button.pack(pady=10)

root.mainloop()
