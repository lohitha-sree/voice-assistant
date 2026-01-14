import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import sys

engine = pyttsx3.init()
engine.setProperty('rate', 150)

recognizer = sr.Recognizer()

EXIT_COMMANDS = ["exit", "quit", "goodbye", "stop listening", "bye"]

# ---------------- SPEAK ----------------
def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN ----------------
def listen():
    """Listen to microphone input and return recognized text."""
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)
            command = recognizer.recognize_google(audio).lower()
            print(f"🗣 You said: {command}")
            return command
        except sr.WaitTimeoutError:
            speak("I am waiting. Please say something.")
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Speech service is currently unavailable.")
            return ""

# ---------------- TIME & DATE ----------------
def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%B %d, %Y")

# ---------------- WEB SEARCH ----------------
def search_web(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Searching the web for {query}")

# ---------------- MAIN ASSISTANT ----------------
def start_assistant():
    speak(
        "Hello! I am your voice assistant. "
        "You can ask me the time, date, or say search followed by your query. "
        "To stop me, say goodbye or stop listening."
    )

    while True:
        command = listen()

        if not command:
            continue

        # EXIT COMMAND
        if any(word in command for word in EXIT_COMMANDS):
            speak("Goodbye! I am stopping now. Have a nice day.")
            print("👋 Assistant stopped.")
            sys.exit()

        # TIME
        elif "time" in command:
            speak(f"The current time is {get_time()}")

        # DATE
        elif "date" in command:
            speak(f"Today's date is {get_date()}")

        # SEARCH
        elif "search" in command:
            query = command.replace("search", "").strip()
            if query:
                search_web(query)
            else:
                speak("Please tell me what you want to search for.")

        # HELP
        elif "help" in command:
            speak(
                "You can say time, date, search something, "
                "or say goodbye to exit."
            )

        # UNKNOWN
        else:
            speak(
                "I can help with time, date, or web search. "
                "Say help to know more, or goodbye to exit."
            )

# ---------------- RUN ----------------
if __name__ == "__main__":
    start_assistant()