import os
import time
import threading
import json
import requests
import speech_recognition as sr
import pyttsx3
import random
from dotenv import load_dotenv
from tkinter import Tk, Label, Entry, Button, StringVar, BOTH
from openai import OpenAI


# === Load environment variables ===
load_dotenv()
SONAR_API_KEY = os.getenv("SONAR_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


# === File paths ===
CHAT_LOG = "jarvis_chat_history.json"
PROFILE_FILE = "jarvis_profile.json"


# === File handling ===
def load_chat_history():
    return json.load(open(CHAT_LOG)) if os.path.exists(CHAT_LOG) else []


def save_chat_history(history):
    json.dump(history, open(CHAT_LOG, "w"), indent=2)


def load_user_profile():
    return json.load(open(PROFILE_FILE)) if os.path.exists(PROFILE_FILE) else {
        "name": "Sir",
        "about": "I don't have any information about you yet.",
        "dob": None
    }


def save_user_profile(profile):
    json.dump(profile, open(PROFILE_FILE, "w"), indent=2)


profile = load_user_profile()
user_name = profile.get("name", "Sir")
user_about = profile.get("about", "")
chat_history = load_chat_history()


# === Initialize Perplexity Sonar API client ===
client = OpenAI(
    api_key=SONAR_API_KEY,
    base_url="https://api.perplexity.ai"
)


# === Initialize TTS engine ===
tts_engine = pyttsx3.init()

# Configure TTS voice for deep, robotic-like male voice (Optimus Prime style approximation):
tts_engine.setProperty('rate', 110)  # slower pace for commanding tone
tts_engine.setProperty('volume', 1.0)

voices = tts_engine.getProperty('voices')
selected_voice = None

for voice in voices:
    name_lower = voice.name.lower()
    # Attempt to pick deep male voice by common names (Windows default voices, etc.)
    if any(male_id in name_lower for male_id in ["male", "david", "mark", "alex", "barry", "zira"]):
        selected_voice = voice.id
        break

if not selected_voice:
    # Fallback: first voice that doesn't say "female"
    for voice in voices:
        if "female" not in voice.name.lower():
            selected_voice = voice.id
            break

if selected_voice:
    tts_engine.setProperty('voice', selected_voice)
else:
    print("No suitable male voice found, using default.")


def speak(text):
    # Simulate natural pre-speaking pause (think time)
    time.sleep(random.uniform(0.4, 0.7))
    tts_engine.say(text)
    tts_engine.runAndWait()
    # Pause after speaking for naturalness
    time.sleep(random.uniform(0.3, 0.5))


def think_and_speak(text):
    # Sample “thinking” phrases for personality
    thinking_phrases = [
        "Let me see...",
        "Hmm...",
        "Okay...",
        "Just a moment...",
        "Understood."
    ]
    speak(random.choice(thinking_phrases))
    time.sleep(random.uniform(0.8, 1.3))
    speak(text)


# === Perplexity Sonar ask function with strict message alternation ===
def ask_sonar(prompt):
    try:
        messages = [{"role": "system", "content": "You are Jarvis, a helpful assistant."}]
        
        i, n = 0, len(chat_history)
        while i < n - 1:
            user_entry = chat_history[i]
            assistant_entry = chat_history[i+1]
            if user_entry.get("role") == "user" and assistant_entry.get("role") == "assistant":
                user_content = user_entry.get("parts", [""])[0]
                assistant_content = assistant_entry.get("parts", [""])[0]
                messages.append({"role": "user", "content": user_content})
                messages.append({"role": "assistant", "content": assistant_content})
                i += 2
            else:
                i += 1

        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="sonar-pro",
            messages=messages
        )

        reply = response.choices[0].message.content.strip()

        chat_history.append({"role": "user", "parts": [prompt]})
        chat_history.append({"role": "assistant", "parts": [reply]})
        save_chat_history(chat_history)

        think_and_speak(reply)
        return reply

    except Exception as e:
        err_msg = f"Sonar error: {e}"
        speak(err_msg)
        return err_msg


# === Weather info ===
def get_weather(city="Mumbai"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        res = requests.get(url)
        data = res.json()

        if data.get("cod") != 200:
            msg = f"Sorry, I couldn’t get the weather for {city}."
            speak(msg)
            return msg

        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        msg = f"The weather in {city} is {desc} with {temp} degrees Celsius, humidity at {humidity} percent, and wind speed of {wind} meters per second."
        speak(msg)
        return msg
    except Exception:
        msg = "Something went wrong while fetching the weather."
        speak(msg)
        return msg


# === Speech recognition ===
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
            query = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {query}")
            return query.lower()
        except:
            err_msg = "Sorry, I didn't catch that."
            print(f"JARVIS: {err_msg}")
            speak(err_msg)
            return ""


# === Wake word detection and command listen ===
def listen_for_wake_word_and_command(wake_word="jarvis"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Say '{wake_word}' to activate Jarvis...")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                phrase = recognizer.recognize_google(audio).lower()
                print(f"Detected phrase: {phrase}")
                if wake_word in phrase:
                    speak(f"Yes, {user_name}?")
                    print("🎙️ Listening for command...")
                    audio_command = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    command = recognizer.recognize_google(audio_command).lower()
                    print(f"🗣️ You said: {command}")
                    return command
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"Speech recognition error: {e}")
                continue


# === GUI dashboard ===
class JarvisDashboard:
    def __init__(self):
        self.root = Tk()
        self.root.title("JARVIS Console")
        self.root.geometry("600x200")
        self.output_text = StringVar()
        self.input_text = StringVar()

        Label(self.root, text="JARVIS Console", font=("Consolas", 16), fg="white", bg="black").pack(fill=BOTH)
        self.console = Label(self.root, textvariable=self.output_text, font=("Consolas", 12), bg="black", fg="lime", padx=20, pady=10)
        self.console.pack(fill=BOTH, expand=True)

        input_frame = Entry(self.root, textvariable=self.input_text, font=("Consolas", 12))
        input_frame.pack(fill=BOTH, padx=10, pady=5)
        Button(self.root, text="Send", command=self.on_send).pack()

        threading.Thread(target=self.root.mainloop, daemon=True).start()

    def update_console(self, text):
        self.output_text.set(text)

    def on_send(self):
        user_input = self.input_text.get().strip()
        self.input_text.set("")
        if user_input:
            process_command(user_input, self)


# === Process commands ===
def process_command(command, dashboard):
    global profile, user_name, user_about

    if not command:
        return

    if "my name is" in command:
        user_name = command.split("my name is")[-1].strip().capitalize()
        profile["name"] = user_name
        save_user_profile(profile)
        msg = f"Nice to meet you, {user_name}."
        print("JARVIS:", msg)
        dashboard.update_console(msg)
        speak(msg)

    elif "remember this" in command:
        msg = "Go ahead, I'm listening."
        print("JARVIS:", msg)
        dashboard.update_console(msg)
        speak(msg)
        info = listen_for_command()
        profile["about"] = info
        user_about = info
        save_user_profile(profile)
        msg = "Got it! I’ll remember that."
        print("JARVIS:", msg)
        dashboard.update_console(msg)
        speak(msg)

    elif "who am i" in command or "do you know me" in command:
        print("JARVIS:", user_about)
        dashboard.update_console(user_about)
        speak(user_about)

    elif "my birthday is" in command:
        dob = command.split("my birthday is")[-1].strip().capitalize()
        profile["dob"] = dob
        save_user_profile(profile)
        msg = f"I've saved your birthday as {dob}."
        print("JARVIS:", msg)
        dashboard.update_console(msg)
        speak(msg)

    elif "when is my birthday" in command:
        dob = profile.get("dob")
        if dob:
            parts = dob.split()
            if len(parts) >= 2:
                date, month = parts[0], parts[1]
                year = time.localtime().tm_year
                msg = f"Your birthday is on {date} {month} {year}."
            else:
                msg = f"You told me your birthday is {dob}."
        else:
            msg = "I don't know your birthday yet."
        print("JARVIS:", msg)
        dashboard.update_console(msg)
        speak(msg)

    elif "shutdown" in command or "exit" in command:
        msg = "Shutting down."
        print("JARVIS:", msg)
        dashboard.update_console(msg)
        speak(msg)
        dashboard.root.quit()

    elif "open notepad" in command:
        os.system("start notepad")
        msg = "Opening Notepad."
        print("JARVIS:", msg)
        dashboard.update_console(msg)
        speak(msg)

    elif "open calculator" in command:
        os.system("start calc")
        msg = "Opening Calculator."
        print("JARVIS:", msg)
        dashboard.update_console(msg)
        speak(msg)

    elif "weather" in command:
        city = "Mumbai"
        if "in" in command:
            city = command.split("in")[-1].strip()
        weather = get_weather(city)
        print("JARVIS:", weather)
        dashboard.update_console(weather)
        # TTS already handled in get_weather

    elif any(op in command for op in ["plus", "minus", "times", "divided"]):
        try:
            expr = command.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided", "/")
            result = eval(expr)
            msg = f"The answer is {result}"
        except Exception:
            msg = "I couldn't calculate that."
        print("JARVIS:", msg)
        dashboard.update_console(msg)
        speak(msg)

    else:
        reply = ask_sonar(command)
        print("JARVIS:", reply)
        dashboard.update_console(reply)
        # already spoken inside ask_sonar


# === Main loop with wake word activation (no spacebar) ===
def main():
    dashboard = JarvisDashboard()
    print(f"JARVIS: Online and waiting for your command, {user_name}.")
    speak(f"Hello {user_name}, I am online and ready.")

    while True:
        command = listen_for_wake_word_and_command()
        if command:
            process_command(command, dashboard)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
