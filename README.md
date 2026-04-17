# AstroLab

This isn't a "polished corporate" project. I built this because I’m a Computer Engineering freshman with a 10km commute. Most of this code was written on a crowded bus, holding a handrail with one hand and typing on my phone with the other.

I used **Firebase Studio** (web-based) and the **Unexpected Keyboard** app to get actual `Ctrl`, `Tab`, and `Arrow` keys on Android. If the code looks structured, it’s because I spent hours auditing what the AI suggested, fixing broken ANSI escape sequences, and fighting JSON mocks when my API quota ran out.

## Why I built this
I needed a way to study Astronomy and Physics during the gaps between classes or on the bus. 
- **NASA APOD:** Something new to learn every day.
- **CLI First:** No heavy web pages. Just the terminal.
- **Spaced Repetition:** Flashcards that actually work for my routine.

## Tech Stack
- **Python + Rich:** For the terminal interface (which is a pain to keep aligned).
- **Gemini 1.5 Flash:** For generating the quizzes and flashcards.
- **NASA API:** For real-world space data.
- **Smart Demo Mode:** I pre-cached data in `demo_cache.json` because I know what it's like to have no signal or no API credits.

## Installation
```bash
pip install astrolab-cli
```
Run it:
```bash
astrolab
```

## Current State
It works. It’s modular. It’s what I use to study. If you find a bug, it’s probably because the bus hit a pothole while I was committing the code.
