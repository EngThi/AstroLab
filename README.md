# Study-Lab-Core: Space Pivot 🚀
[![NASA API Powered](https://img.shields.io/badge/NASA-API_Powered-blue)](https://api.nasa.gov/)

Pivot para o desafio Sidequest Challenger. Ferramenta de estudo de astronomia/física que utiliza dados reais da NASA (APOD) e gera perguntas (Flashcards e Quizzes) interativas usando o Google Gemini.

## Funcionalidades

- `python main.py apod`: Mostra a "Astronomy Picture of the Day" com explicação.
- `python main.py quiz`: Gera um quiz interativo de 5 perguntas sobre o APOD do dia usando IA.
- `python main.py flashcard "<tema>"`: Cria um flashcard temático baseado nos dados do espaço.

## Quick Start

1. Clone o repositório e instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as credenciais:
```bash
cp .env.example .env
# Edite o arquivo .env e coloque as chaves (NASA_API_KEY e GEMINI_API_KEY)
```

3. Explore o espaço:
```bash
python main.py apod
```

## Arquitetura e Tech Stack

- **NASA APOD API:** Fornece os dados base do dia.
- **Google Gemini API:** Gera e avalia perguntas com base no contexto espacial.
- **Python / Rich:** Interface CLI rica em recursos visuais.