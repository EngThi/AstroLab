# AstroLab (ex-Study-Lab-Core) 🚀
[![NASA API Powered](https://img.shields.io/badge/NASA-API_Powered-blue)](https://api.nasa.gov/)

Pivot para o desafio Sidequest Challenger. Ferramenta de estudo de astronomia/física que utiliza dados reais da NASA (APOD) e gera perguntas (Flashcards e Quizzes) interativas usando o Google Gemini. O estudo perfeito "entre as aulas"!

## Funcionalidades

- `python main.py apod`: Mostra a "Astronomy Picture of the Day" com explicação.
- `python main.py quiz`: Gera um quiz interativo de 5 perguntas sobre o APOD do dia usando IA. Inclui o modo **Deep Dive** para aprender com os seus erros!
- `python main.py flashcard "<tema>"`: Cria um flashcard temático baseado nos dados do espaço e salva automaticamente no seu deck pessoal.
- `python main.py review`: **[NOVO]** Inicia uma sessão de revisão com todos os flashcards que você gerou e salvou.
- `python main.py stats`: Exibe o seu histórico de progresso de estudo com gráficos de barras estilizados no terminal! Acompanhe sua evolução e acertos em cada sessão.

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

3. Explore o espaço (agora com menu interativo!):
```bash
python main.py
```

## Arquitetura e Tech Stack

- **NASA APOD API:** Fornece os dados base do dia.
- **Google Gemini API:** Gera e avalia perguntas com base no contexto espacial e cria Deep Dives.
- **Python / Rich:** Interface CLI rica em recursos visuais.
- **Armazenamento:** Histórico e Deck de Flashcards persistidos localmente via JSON em `data/`.