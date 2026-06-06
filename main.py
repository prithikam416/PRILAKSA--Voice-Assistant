import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Typically index 0 is male (David) and index 1 is female (Zira) on Windows
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)

def speak(audio):
    """Function to make Prilaksa speak"""
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    """Function to greet the user based on the time of day"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
        
    speak("I am Prilaksa. How can I help you today?")

def take_command():
    """Function to take microphone input and return string output"""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
    except Exception as e:
        print("\n[Warning] Could not access the microphone. Please check if it's connected and unblocked.")
        # Fallback to text input if microphone fails
        query = input("Please type your command instead: ")
        return query.lower()

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()

        if query == "none":
            continue

        # Logic for executing basic tasks
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak("Sorry, I could not find anything on Wikipedia.")
                print("Wikipedia Error:", e)

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")    
            speak(f"The time is {strTime}")
            print(f"The time is {strTime}")

        elif 'stop' in query or 'exit' in query or 'quit' in query or 'bye' in query:
            speak("Goodbye! Have a great day.")
            break
        
        else:
            speak("I am not sure how to do that yet. Try asking me to open Google, open YouTube, or check the time.")
