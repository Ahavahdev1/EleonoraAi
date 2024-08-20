import os
from groq import Groq
from duckduckgo_search import DDGS
from datetime import date

class GroqDuckDuckGoBot:
    def __init__(self, model_name="llama3-8b-8192"):
        self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = model_name

    def chat(self, message, history=[]):
        today = date.today()
        message = f"Lembre-se que você está conectado à internet e tem acesso a informações em tempo real. Use seus recursos para fornecer respostas precisas e relevantes para o usuário, considerando a data de hoje, {today.strftime('%d de %B de %Y')}. {message}"

        messages = [{ "role": "user", "content": message }] + history
        chat_completion = self.groq_client.chat.completions.create(
            messages=messages,
            model=self.model_name,
        )
        response = chat_completion.choices[0].message.content

        if "search" in response:
            parts = response.split("search: ")
            if len(parts) >= 2:
                search_term = parts[1].strip()
                search_results = self.perform_search(search_term)
                if search_results:
                    response += f"\n\n**Resultados da Busca:**\n"
                    for result in search_results:
                        response += f"- {result['href']} - {result['title']}\n"
        else:
            search_results = self.perform_search(message)
            if search_results:
                response += f"\n\n**Resultados da Busca:**\n"
                for result in search_results:
                    response += f"- {result['href']} - {result['title']}\n"
        return response

    def perform_search(self, query):
        with DDGS() as ddgs:
            results = ddgs.text(query)
            return results

os.environ["GROQ_API_KEY"] = "Groq_api_key_here"

bot = GroqDuckDuckGoBot()

while True:
    user_input = input("Você: ")
    if user_input.lower() == "sair":
        break
    response = bot.chat(user_input)
    print("Bot:", response)
