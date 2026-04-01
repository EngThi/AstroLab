# AstroLab 🚀
[![NASA API Powered](https://img.shields.io/badge/NASA-API_Powered-blue)](https://api.nasa.gov/)

Pivot for the Hack Club Sidequest Challenger. An astronomy/physics study tool that utilizes real NASA data (APOD endpoint) to generate interactive quizzes and flashcards using Google Gemini AI. The perfect tool for studying "between lectures"!

## Features

- `astrolab apod`: Shows the "Astronomy Picture of the Day" with a detailed explanation.
- `astrolab quiz`: Generates an interactive 5-question quiz based on the daily APOD using AI. Includes a **Deep Dive** mode to learn from your mistakes!
- `astrolab flashcard "<topic>"`: Creates a thematic flashcard based on space data and automatically saves it to your personal deck.
- `astrolab review`: **[NOVO]** Starts a review session with all the flashcards you have generated and saved.
- `astrolab stats`: Displays your study progress history with stylized bar charts in the terminal! Track your performance and accuracy across sessions.

## 💡 Quick Start (For Reviewers)

**AstroLab is now published on PyPI for a frictionless testing experience!**

1. Install the package globally via pip:
```bash
pip install astrolab-cli
```

2. **[OPTIONAL]** To use the fully dynamic AI generation, configure your credentials by creating a `.env` file in your working directory:
```bash
NASA_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```
*Note: If you don't configure an `.env`, the system will use a `DEMO_KEY` for NASA and safely fallback to our **Smart Demo Mode** for Gemini, pulling rich pre-generated responses from an internal cache.*

3. Explore space with our beautiful interactive menu by running:
```bash
astrolab
```

## Architecture and Tech Stack

- **NASA APOD API:** Provides the foundational space data.
- **Google Gemini API:** Generates and evaluates questions based on space context and creates Deep Dives.
- **Python / Rich:** CLI interface with beautiful visual components.
- **Storage:** Study history and Flashcard Deck persisted locally via JSON in `data/`.