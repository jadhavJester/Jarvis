# Jarvis
This is the first gen code i wrote for my personal voice assistant and as i have made newer versions of my desk companion, i am open sourcing my first gen code of jarvis
This Python project implements an advanced voice-activated JARVIS assistant featuring speech recognition, natural language conversation, weather queries, and user personalization with a simple GUI dashboard.

Voice Activation & Conversation: Listens for a wake word (“jarvis”), transcribes speech to text, and maintains context-aware dialogue using Perplexity’s Sonar (LLM) API for intelligent responses.

Text-to-Speech (TTS): Replies are spoken aloud in a deep, commanding voice by configuring available system voices with pyttsx3.

Personalization: Remembers and updates user profile details including name, about/bio, and birthday.

Chat History: Persists conversations via JSON files, enabling context-aware, multi-turn conversations.

Weather Integration: Gets and voices real-time weather information using the OpenWeather API.

GUI Console: Provides a Tkinter-based dashboard for visual interaction and manual input.

Basic Local Commands: Supports personal notes, remembering facts, retrieving birthdays, and launching desktop applications (like Notepad or Calculator).

Natural Speaking Style: Adds pauses and “thinking” phrases before answering for a friendly and believable user experience.

This assistant demonstrates a blend of modern LLM conversation, real-time voice input/output, and practical automation—all accessible via voice or GUI.
