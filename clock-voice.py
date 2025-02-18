import datetime
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume

# Иницијализирај го моторот за текст-во-збор
engine = pyttsx3.init()

# Иницијализирај го препознавачот на говор
recognizer = sr.Recognizer()

def speak(text):
    print(f"Saying: {text}")  # За отстранување грешки: Печати што ќе се изговара
    engine.say(text)
    engine.runAndWait()

def set_all_app_volumes(volume_level, exclude_process):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name().lower() != exclude_process.lower():
            print(f"Setting volume for {session.Process.name()} to {volume_level * 100}%")
            volume.SetMasterVolume(volume_level, None)

def display_time(current_time):
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg='black')

    label = tk.Label(root, text=current_time, font=('Helvetica', 100), fg='white', bg='black')
    label.pack(expand=True)

    def close(event):
        root.destroy()

    root.bind('<Escape>', close)
    root.after(5000, root.destroy)  # Затвори го прозорецот по 5 секунди
    root.mainloop()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        print("Audio recorded.")  # За отстранување грешки: Печати кога ќе се сними говорот
    try:
        query = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("I couldn't understand you.")
    except sr.RequestError as e:
        print(f"Cannot process the speech; {e}")
    return None

while True:
    query = listen()
    if query:
        print(f"Recognized query: {query}")  # За отстранување грешки: Печати го препознаеното прашање
        if "what time is it" in query.lower():
            set_all_app_volumes(0.1, "python.exe")  # Намали го звукот на сите апликации освен Python
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            speak(f"The current time is {current_time}")
            display_time(current_time)  # Прикажи го времето на цел екран
            set_all_app_volumes(1.0, "python.exe")  # Врати го звукот на сите апликации освен Python на 100%
        else:
            print("The query did not match 'what time is it'")  # За отстранување грешки: Печати ако прашањето не одговара
