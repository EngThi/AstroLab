import os
import json
import random
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class GeminiClient:
    """Cliente para a API do Google Gemini com fallback inteligente para Demonstração."""
    
    def __init__(self):
        # Utiliza o modelo gemini-1.5-flash para tarefas rápidas de texto
        if GEMINI_API_KEY:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            
        self._load_demo_cache()

    def _load_demo_cache(self):
        """Carrega dados em cache para demonstração offline."""
        try:
            with open("data/demo_cache.json", "r", encoding="utf-8") as f:
                self.demo_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.demo_data = {"quizzes": [], "deep_dives": [], "flashcards": {}}

    def _generate_json(self, prompt: str) -> dict:
        """Helper para garantir que a resposta seja um JSON válido."""
        if not self.model:
            raise ValueError("GEMINI_API_KEY não configurada.")
            
        full_prompt = f"{prompt}\n\nResponda APENAS com um objeto JSON válido, sem formatação markdown ou texto extra."
        
        response = self.model.generate_content(full_prompt)
        text = response.text.strip()
        
        # Remove possíveis blocos de código markdown que o modelo pode retornar
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Fallback em caso de erro na geração
            return {"error": "Falha ao decodificar JSON do Gemini", "raw_text": text}

    def generate_quiz(self, context_text: str, num_questions: int = 5) -> list:
        """Gera um quiz com base no texto fornecido."""
        if not self.model:
            return self._fallback_quiz()

        prompt = f"""
        Baseado no texto a seguir sobre astronomia, crie um quiz com {num_questions} perguntas de múltipla escolha.
        O nível deve ser para estudantes universitários (desafiador mas focado nos conceitos do texto).
        
        TEXTO:
        {context_text}
        
        O JSON de saída deve ser estritamente uma lista de objetos com este formato:
        [
            {{
                "question": "texto da pergunta",
                "options": ["A) op1", "B) op2", "C) op3", "D) op4"],
                "answer": "A) op1",  // DEVE ser exatamente igual a uma das strings na lista de opções
                "explanation": "Por que esta é a resposta correta baseado no texto"
            }}
        ]
        """
        try:
            result = self._generate_json(prompt)
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "quiz" in result: # Lida com pequenas variações estruturais
                return result["quiz"]
            return self._fallback_quiz()
        except Exception as e:
            print(f"Erro ao gerar quiz: {e}")
            return self._fallback_quiz()

    def generate_flashcard(self, topic: str, context_text: str) -> dict:
        """Gera o conteúdo de um flashcard."""
        if not self.model:
            return self._fallback_flashcard(topic)

        prompt = f"""
        Baseado no texto da NASA sobre o tema '{topic}', crie o conteúdo para um flashcard de estudo.
        
        TEXTO:
        {context_text}
        
        O JSON de saída deve ser um objeto com este formato:
        {{
            "front": "Uma pergunta direta ou conceito chave sobre {topic}",
            "back": "A resposta detalhada, direta e fácil de memorizar"
        }}
        """
        try:
            result = self._generate_json(prompt)
            if "front" in result and "back" in result:
                return result
            return self._fallback_flashcard(topic)
        except Exception:
            return self._fallback_flashcard(topic)

    def generate_deep_dive(self, wrong_answers: list) -> str:
        """Gera uma explicação aprofundada baseada nos erros."""
        if not self.model:
            return self.demo_data.get("deep_dives", ["Desculpe, modo offline. Verifique a documentação para habilitar a IA."])[0]
            
        erros_formatados = ""
        for i, q in enumerate(wrong_answers, 1):
            erros_formatados += f"Erro {i}:\n"
            erros_formatados += f"Pergunta: {q.get('question')}\n"
            erros_formatados += f"Resposta Correta: {q.get('answer')}\n\n"

        prompt = f"""
        Você é um professor universitário de astrofísica apaixonado por ensinar. 
        Um aluno acabou de fazer um quiz sobre astronomia e errou as seguintes questões:

        {erros_formatados}

        Por favor, crie um guia de estudo curto e aprofundado (Deep Dive) focado APENAS nestes conceitos.
        Sua resposta não precisa ser um JSON. Pode usar Markdown livremente.
        - Explique a intuição física por trás de cada erro.
        - Use analogias do dia a dia para ajudar na memorização.
        - Seja encorajador.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Ocorreu um erro ao gerar o Deep Dive: {e}"

    def _fallback_quiz(self) -> list:
        """Retorna um quiz fixo rico do cache caso a API falhe."""
        quizzes = self.demo_data.get("quizzes", [])
        if quizzes:
            return random.choice(quizzes)
        return []
        
    def _fallback_flashcard(self, topic: str) -> dict:
        """Retorna um flashcard do cache de demonstração."""
        cards = self.demo_data.get("flashcards", {})
        # Tenta achar um card que bata com o tema, senão pega o default
        topic_lower = topic.lower()
        if topic_lower in cards:
            return cards[topic_lower]
        return cards.get("default", {"front": "Modo Offline", "back": "Adicione GEMINI_API_KEY no .env"})

gemini_client = GeminiClient()
