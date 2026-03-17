from groq import Groq

from config.libs.envroinments import env

client = Groq(api_key=env.GROQ_API_KEY)


def generate_ai_response(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro no Groq: {str(e)}"
