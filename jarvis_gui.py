import os
import time
import threading
import json
import requests
import speech_recognition as sr
from tkinter import *
from dotenv import load_dotenv
from openai import OpenAI
import keyboard

# === Load API Keys ===
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# === Memory Files ===
CHAT_LOG = "jarvis_chat_history.json"
PROFILE_FILE = "jarvis_profile.json"

# === Load & Save ===
def load_chat_history():
    return json.load(open(CHAT_LOG)) if os.path.exists(CHAT_LOG) else []

def save_chat_history(history):
    json.dump(history, open(CHAT_LOG, "w"), indent=2)

def load_user_profile():
    return json.load(open(PROFILE_FILE)) if os.path.exists(PROFILE_FILE) else {
        "name": "Sir",
        "about": "I don't know you yet.",
        "dob": None
    }

def save_user_profile(profile):
    json.dump(profile, open(PROFILE_FILE, "w"), indent=2)

profile = load_user_profile()
user_name = profile["name"]
chat_history = load_chat_history()

# === GROQ Model via OpenAI SDK ===
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def ask_groq(prompt):
    try:
        messages = [{"role": "system", "content": "You are Jarvis, a helpful assistant."}]
        for entry in chat_history:
            role = entry.get("role")
            content = entry.get("parts", [""])[0]
            if role in ["user", "assistant"]:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages
        )
        reply = response.choices[0].message.content.strip()
        chat_history.append({"role": "user", "parts": [prompt]})
        chat_history.append({"role": "assistant", "parts": [reply]})
        save_chat_history(chat_history)
        return reply
    except Exception as e:
        return f"GROQ error: {e}"

def get_weather(city="Mumbai"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        res = requests.get(url)
        data = res.json()
        if data["cod"] != 200:
            return f"Sorry, I couldn’t get the weather for {city}."
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        return f"The weather in {city} is {desc} with {temp}°C, {humidity}% humidity, wind at {wind} m/s."
    except:
        return "Error fetching weather."

def listen_for_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            query = r.recognize_google(audio)
            return query.lower()
        except:
            return "Sorry, I didn't catch that."

# === GUI App ===
class JarvisApp:
    def __init__(self):
        self.profile = profile
        self.root = Tk()
        self.root.title("JARVIS - Virtual Assistant")
        self.root.geometry("700x500")
        self.root.configure(bg="black")

        self.chat_box = Text(self.root, bg="black", fg="white", font=("Consolas", 12), wrap=WORD)
        self.chat_box.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.input_entry = Entry(self.root, font=("Consolas", 12))
        self.input_entry.pack(fill=X, padx=10, pady=(0, 5))
        self.input_entry.bind("<Return>", lambda event: self.send_text())

        button_frame = Frame(self.root, bg="black")
        button_frame.pack(fill=X, padx=10)

        Button(button_frame, text="Send", command=self.send_text).pack(side=LEFT, padx=5)
        Button(button_frame, text="🎤 Mic", command=self.send_voice).pack(side=LEFT)

        self.status_label = Label(self.root, text="Status: Idle", bg="black", fg="gray", font=("Consolas", 10))
        self.status_label.pack(fill=X)

        self.is_awake = True
        self.last_space_time = 0
        self.setup_keyboard_listener()

    def setup_keyboard_listener(self):
        def on_space(event):
            current_time = time.time()
            if current_time - self.last_space_time < 0.5:
                self.is_awake = not self.is_awake
                state = "Awake" if self.is_awake else "Sleeping"
                self.update_status(f"{state} (Toggled by SPACE)")
                self.display("JARVIS", f"I am now {state.lower()}, {self.profile['name']}.")
            self.last_space_time = current_time

        keyboard.on_press_key("space", on_space)

    def display(self, sender, message):
        self.chat_box.insert(END, f"{sender}: {message}\n")
        self.chat_box.see(END)

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")

    def send_text(self):
        query = self.input_entry.get().strip()
        self.input_entry.delete(0, END)
        if query:
            self.process_command(query)

    def send_voice(self):
        if not self.is_awake:
            self.display("JARVIS", "I'm sleeping. Press SPACE twice to wake me.")
            return

        self.update_status("Listening...")
        self.display("You (🎤)", "...")
        threading.Thread(target=self._process_voice, daemon=True).start()

    def _process_voice(self):
        voice_cmd = listen_for_voice()
        self.chat_box.delete("end-2l", "end-1l")  # Remove placeholder
        self.display("You (🎤)", voice_cmd)
        self.process_command(voice_cmd)

    def process_command(self, command):
        self.display("You", command)
        self.update_status("Thinking...")

        if "weather" in command:
            city = "Mumbai"
            if "in" in command:
                city = command.split("in")[-1].strip()
            response = get_weather(city)

        elif "my name is" in command:
            name = command.split("my name is")[-1].strip().capitalize()
            self.profile["name"] = name
            save_user_profile(self.profile)
            response = f"Nice to meet you, {name}!"

        elif "my birthday is" in command:
            dob = command.split("my birthday is")[-1].strip()
            self.profile["dob"] = dob
            save_user_profile(self.profile)
            response = f"I've saved your birthday as {dob}."

        elif "when is my birthday" in command:
            dob = self.profile.get("dob", None)
            response = f"Your birthday is {dob}." if dob else "You haven't told me your birthday yet."

        elif "shutdown" in command or "exit" in command:
            self.root.quit()
            return

        else:
            response = ask_groq(command)

        self.display("JARVIS", response)
        self.update_status("Idle")

if __name__ == "__main__":
    app = JarvisApp()
    app.root.mainloop()
