# Devlog: Space Pivot - Sidequest Challenger 🚀

**Data:** 12 de Fevereiro de 2026

## O que foi feito?
Pivotei o Study Lab para um tema espacial com o objetivo de participar da Sidequest Challenger!

## Justificativa do pivot
"Estudo para Engenharia de Computação e percebo que aprender física teórica é entediante. Decidi usar dados reais da NASA — a API deles é gratuita e dá acesso a fotos, dados planetários e eventos astronômicos. Cada sessão de estudo usa dados do dia atual."

## Implementações (O que "Shipamos")
1. **Integração NASA API:** O script agora se conecta ao endpoint APOD para buscar a foto e o contexto astronômico do dia.
2. **Integração Google Gemini:** Implementamos um gerador de Quizzes e Flashcards que usa a descrição da NASA como *ground truth* para criar perguntas educacionais de múltipla escolha.
3. **CLI Interativa:** Construímos uma interface com `Rich` no terminal.
    - `python main.py apod`: Exibe os dados do dia.
    - `python main.py quiz`: Inicia um quiz gerado na hora pela IA.
    - `python main.py flashcard "tema"`: Gera flashcards de estudo na hora.
4. **Qualidade e Testes:** Criamos uma suíte com 5 testes usando `pytest` e `pytest-mock` para garantir que o cliente da NASA retorna os campos corretos e o Gemini gera o fallback caso necessário.
5. **CI/CD:** Adicionado GitHub Action (`ci.yml`) para rodar os testes automaticamente.

**Nota de Teste:** Testei hoje com o tema 'black holes' e as perguntas que a IA gerou baseadas no texto da NASA foram surpreendentemente boas e desafiadoras! Tudo pronto para o deploy e submissão.
