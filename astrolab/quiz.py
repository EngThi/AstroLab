from astrolab.nasa_client import nasa_client
from astrolab.gemini_client import gemini_client
from astrolab.session import session_manager
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

class QuizGenerator:
    """Generator and executor of NASA data-based quizzes."""
    
    def run_daily_quiz(self, is_random: bool = False):
        """Fetches the APOD and generates an interactive 5-question quiz."""
        status_msg = "Fetching a random space event for your quiz..." if is_random else "Fetching today's NASA APOD data to use as study context for your quiz..."
        
        with console.status(f"[bold cyan]{status_msg}"):
            try:
                apod_data = nasa_client.get_apod(random=is_random)
            except Exception as e:
                console.print(f"[bold red]Error fetching NASA data: {e}[/bold red]")
                return
                
        title = apod_data.get("title", "Unknown")
        explanation = apod_data.get("explanation", "")
        
        console.print(Panel(f"[italic]{explanation}[/italic]", title=f"Context: {title}"))
        
        with console.status("[bold magenta]Generating 5 questions based on the text above..."):
            questions = gemini_client.generate_quiz(explanation, num_questions=5)
            
        if not questions:
            console.print("[bold red]Failed to generate the quiz.[/bold red]")
            return
            
        self._execute_quiz(questions, title)

    def _execute_quiz(self, questions: list, topic_title: str):
        score = 0
        wrong_answers = []
        console.print("\n[bold green]--- STARTING SPACE QUIZ ---[/bold green]\n")
        
        for i, q in enumerate(questions, 1):
            console.print(f"[bold cyan]Question {i}:[/bold cyan] {q.get('question')}")
            for opt in q.get('options', []):
                console.print(f"  {opt}")
                
            user_answer = Prompt.ask("\nYour answer (e.g., A, B, C, D)").strip().upper()
            
            # Extract just the letter of the correct answer (e.g., "A) text" -> "A")
            correct_answer = q.get('answer', '')
            correct_letter = correct_answer[0].upper() if correct_answer else ''
            
            if user_answer == correct_letter:
                console.print("[bold green]Correct![/bold green]")
                score += 1
            else:
                console.print(f"[bold red]Incorrect.[/bold red] The correct answer was: {correct_answer}")
                wrong_answers.append(q)
                
            console.print(f"[italic]Explanation: {q.get('explanation')}[/italic]\n")
            
        console.print(f"[bold yellow]--- End of Quiz! Your score: {score}/{len(questions)} ---[/bold yellow]\n")
        
        # Save result to session history
        session_manager.save_session(topic_title, score, len(questions))
        console.print(f"[dim]Session saved to history. Use 'astrolab stats' to view your progress.[/dim]")
        
        if wrong_answers and Confirm.ask("\n[bold cyan]You missed some questions. Do you want a Deep Dive explanation for your mistakes?[/bold cyan]"):
            with console.status("[bold magenta]Analyzing your mistakes and generating an educational Deep Dive..."):
                deep_dive_text = gemini_client.generate_deep_dive(wrong_answers)
            console.print(Panel(deep_dive_text, title="[bold blue]Deep Dive: Focused Review[/bold blue]", border_style="blue"))


