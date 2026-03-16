from openai import OpenAI
from config.libs.envroinments import env

# O cliente permanece o mesmo
client = OpenAI(api_key=env.OPENAI_API_KEY)

def generate_gpt_response(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            # 1. Troque para o 4o-mini apenas para testar se a resposta volta
            model="gpt-5-nano", 
            messages=[
                # 2. Dê um contexto mais claro
                {"role": "system", "content": "Você é um especialista em MMA e finanças."},
                {"role": "user", "content": prompt}
            ],
            # 3. Volte para max_tokens se usar o 4o-mini, ou mantenha se for gpt-5
            max_completion_tokens=500,
        )
        
        print(f"DEBUG: Finish Reason: {completion.choices[0].finish_reason}")
        
        content = completion.choices[0].message.content
        return content.strip() if content else "API retornou vazio (None)"
        
    except Exception as e:
        return f"Erro na API: {str(e)}"

if __name__ == "__main__":
    # Teste com uma pergunta bem direta
    print("Enviando pergunta para o GPT-5 Nano...")
    resposta = generate_gpt_response("me fale sobre o charles do bronx")
    
    print("-" * 30)
    print(f"RESPOSTA DA IA:\n {resposta}")
    print("-" * 30)