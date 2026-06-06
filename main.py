import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import google.generativeai as genai

# ==========================================
# SETUP YOUR GEMINI API KEY HERE
# Get a free key from: https://aistudio.google.com/
# ==========================================
API_KEY = "YOUR_GEMINI_API_KEY_HERE"

genai.configure(api_key=API_KEY)
ai_enabled = True
if API_KEY == "YOUR_GEMINI_API_KEY_HERE":
    ai_enabled = False

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)

def speak(audio):
    """Function to make Prilaksa speak"""
    engine.say(audio)
    engine.runAndWait()

def ask_ai(prompt):
    """Ask Google Gemini for a conversational response"""
    if not ai_enabled:
        return "Please set your Gemini API key in main dot py to use my smart brain."
    try:
        # Use gemini-1.5-flash for fast responses
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Instruct the model to be concise since it's a voice assistant
        response = model.generate_content(f"You are a helpful voice assistant named Prilaksha. Answer this query conversationally but briefly in 1 to 2 sentences: {prompt}")
        return response.text.replace('*', '') # Remove markdown asterisks so they aren't spoken aloud
    except Exception as e:
        print(f"AI Error: {e}")
        return "I'm having trouble connecting to my brain right now. Check your internet or API key."

def take_command():
    """Function to take microphone input and return string output"""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\nListening for wake word ('Prilaksha')...")
            r.pause_threshold = 1
            # We don't want a strict timeout here since it should listen continuously
            audio = r.listen(source, phrase_time_limit=10)
    except Exception as e:
        print("\n[Warning] Could not access the microphone.")
        query = input("\nType your command (e.g. 'prilaksha what is the capital of France'): ")
        return query.lower()

    try:
        query = r.recognize_google(audio, language='en-in')
        return query.lower()

    except Exception as e:
        return "none"

if __name__ == "__main__":
    print("\n--- Prilaksha Voice Assistant is Online ---")
    speak("I am online. Just say 'Prilaksha' followed by your command.")
    
    while True:
        query = take_command()

        if query == "none":
            continue
            
        print(f"Heard: {query}")

        # Wake word detection
        if 'prilaksha' in query or 'prilaksa' in query:
            # Extract the actual command
            command = query.replace("prilaksha", "").replace("prilaksa", "").strip()
            
            if command == "":
                speak("Yes? How can I help you?")
                command = take_command() # Listen for the next part
            
            if command == "none":
                continue

            print(f"Command processing: {command}")

            # Basic Hardcoded Tasks
            if 'wikipedia' in command:
                speak('Searching Wikipedia...')
                command = command.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(command, sentences=2)
                    print(results)
                    speak(results)
                except Exception as e:
                    speak("Sorry, I could not find anything on Wikipedia.")

            elif 'open youtube' in command:
                speak("Opening YouTube")
                webbrowser.open("https://youtube.com")

            elif 'open google' in command:
                speak("Opening Google")
                webbrowser.open("https://google.com")

            elif 'time' in command:
                strTime = datetime.datetime.now().strftime("%I:%M %p")    
                speak(f"The time is {strTime}")
                print(f"The time is {strTime}")

            elif 'stop' in command or 'exit' in command or 'quit' in command or 'bye' in command:
                speak("Goodbye! Have a great day.")
                break
            
            else:
                # If it's not a basic command, ask the AI Brain!
                speak("Let me think...")
                answer = ask_ai(command)
                print(f"\nAI says: {answer}\n")
                speak(answer)
