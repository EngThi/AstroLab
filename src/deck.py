import json
import os
import random
from rich.console import Console
from rich.panel import Panel

console = Console()
DECK_FILE = "data/deck.json"

class DeckManager:
    """Gerencia a coleção de flashcards salvos."""

    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data", exist_ok=True)
            
        if not os.path.exists(DECK_FILE):
            with open(DECK_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save_card(self, topic: str, front: str, back: str):
        """Salva um flashcard gerado no deck pessoal."""
        try:
            with open(DECK_FILE, "r", encoding="utf-8") as f:
                deck = json.load(f)
        except json.JSONDecodeError:
            deck = []

        # Evita duplicatas exatas
        if not any(card.get('front') == front for card in deck):
            deck.append({
                "topic": topic,
                "front": front,
                "back": back
            })
            with open(DECK_FILE, "w", encoding="utf-8") as f:
                json.dump(deck, f, indent=4, ensure_ascii=False)

    def review_deck(self):
        """Inicia uma sessão de revisão dos flashcards salvos."""
        try:
            with open(DECK_FILE, "r", encoding="utf-8") as f:
                deck = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            console.print("[bold red]Erro ao ler o deck.[/bold red]")
            return

        if not deck:
            console.print("[bold yellow]Seu deck está vazio! Gere alguns flashcards primeiro usando a opção 3 do menu.[/bold yellow]")
            return

        console.print(f"\n[bold green]--- 📚 INICIANDO REVISÃO ({len(deck)} cards) ---[/bold green]\n")
        
        # Embaralha os cards para a revisão
        random.shuffle(deck)

        for i, card in enumerate(deck, 1):
            console.print(f"[bold cyan]Card {i}/{len(deck)} | Tema: {card.get('topic', 'N/A')}[/bold cyan]")
            
            front_panel = Panel(card.get("front", ""), title="[bold blue]Frente (Pergunta)[/bold blue]", expand=False)
            console.print(front_panel)
            
            input("\nPressione ENTER para revelar a resposta...")
            
            back_panel = Panel(card.get("back", ""), title="[bold green]Verso (Resposta)[/bold green]", expand=False)
            console.print(back_panel)
            
            if i < len(deck):
                cont = input("\nPressione ENTER para o próximo card ou 'q' para sair da revisão...").strip().lower()
                if cont == 'q':
                    break
            console.print("\n")
            
        console.print("[bold yellow]--- Fim da Revisão! ---[/bold yellow]\n")

deck_manager = DeckManager()
