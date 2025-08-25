# JARVIS: Voice-activated Intelligent Assistant



***

## 🧠 Introduction

Meet **JARVIS**—your personal assistant powered by Python, OpenAI, Perplexity Sonar, and real-time voice interaction. Inspired by the vision of intelligent, conversational AIs, this project blends speech recognition, text-to-speech (TTS), local command execution, weather, memory, and a user-friendly GUI to create a true desktop companion.

***

## ✨ Features At a Glance

| Feature                                 | Description                                                                               |
|------------------------------------------|-------------------------------------------------------------------------------------------|
| 🎙️ Wake-word Listening                  | Say “jarvis” to activate—no keyboard required!                                            |
| 💬 Natural Conversations                | Responds with LLM-based answers, keeps history context for multi-turn dialogue.           |
| 🗣️ Deep-voice TTS                       | Replies out loud in a rich, robotic voice (approximates ‘Optimus Prime’ style).           |
| 📝 Memory & Personal Profile             | Remembers your name, birthday, important facts; learns as you interact.                   |
| 🌦️ Weather Reports                      | Real-time weather via OpenWeatherMap.                                                     |
| 🧮 Math Solver                           | Handles simple verbal math operations (“five plus four divided by two”).                  |
| 🖥️ Local Program Launch                  | Opens Calculator/Notepad on your command.                                                 |
| 🖼️ GUI Dashboard                        | View interaction history and converse using graphical interface for convenience.           |
| 🗂️ Conversation Logging                  | Chat history is stored and leveraged for better context and recall.                       |

***


*Modern Tkinter dashboard for easy monitoring and input.*

***

## 📋 Table of Contents

- [Introduction](#introduction)
- [Features](#features-at-a-glance)
- [Demo Images](#demo-images)
- [How It Works](#how-it-works)
- [Setup](#setup)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

***

## 📷 Demo Images

<img width="1388" height="455" alt="image" src="https://github.com/user-attachments/assets/aee5798b-0234-41c7-9d5c-d1fa28cfb54c" />

***

## 🛠️ How It Works

- **Startup:** JARVIS greets you with a deep robotic voice and waits for your “jarvis” wake word.
- **Speech Recognition:** Listens for your command, transcribes it using Google speech recognition.
- **Profile & Memory:** Stores your name, birthday, and info; recalls them on request with “who am I” or “when is my birthday.”
- **Weather Fetching:** Instantly fetches and reads local weather from OpenWeather API.
- **Conversations:** Thanks to Perplexity Sonar and OpenAI, JARVIS answers intelligent questions, jokes, and summaries.
- **GUI Dashboard:** View and send messages via Tkinter, review output and histories, and interact by typing.

***

## 🧑‍💻 Setup

1. **Clone the repo and install requirements:**
   ```bash
   git clone https://github.com/yourname/jarvis-desktop-assistant.git
   cd jarvis-desktop-assistant
   pip install -r requirements.txt
   ```

2. **Add your API keys to `.env`:**
   ```
   SONAR_API_KEY=your_openai_or_perplexity_key
   OPENWEATHER_API_KEY=your_openweathermap_key
   ```

3. **(Optional) Add images/GIFs in `images/` for your README.**

***

## 🚦 Usage

- **Start GUI and Assistant:**
   ```bash
   python jarvis_main.py
   ```
- **Say “jarvis”, then your command (e.g., “weather in Mumbai”, “open calculator”, “my name is Tony”)**

- **Interact with GUI:** Type or click “Send” in GUI window.

***

## 🏗️ Code Structure Overview

Your project is modular and extensible:
- **Main App:** Handles launching the dashboard, voice loop, and event orchestration.
- **Speech & TTS:** Uses `pyttsx3` for offline TTS and configures deep male voice for signature output.
- **Perplexity/OpenAI LLM:** Contextual, smart responses for “general knowledge” and natural conversation.
- **Weather & Memory:** Responds to “weather,” “birthday,” “remember this,” or “who am I.”
- **GUI:** Tkinter-powered, shows chat logs, allows typed commands and updates.

***

## 🎨 Customization

- Switch TTS voice in the code for personality change.
- Add more commands in `process_command` for new actions (e.g., play music, send emails).
- Change and expand your GUI to include images, stats, or more controls.

***

## 🤝 Contributing

Want to extend JARVIS? Pull requests welcome!
- Fork, clone, and work in feature branches.
- Submit code with screenshots/GIFs showing your new features.
- Open issues for bugs, enhancements, or feedback.

***

## 📜 License

Released under the MIT License for maximum freedom and collaboration.

***

## ❤️ Final Thoughts

JARVIS isn’t just a codebase—it’s your own smart agent. Every feature, from wake-word to memory, makes the experience more immersive. Add your flair, share your usage GIFs, and make it truly personalized!

*“I am here, always listening and ready to assist. Just say the word.”*
