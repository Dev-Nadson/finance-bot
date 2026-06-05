from openai import OpenAI

from config.libs.envroinments import env

client = OpenAI(api_key=env.OPENAI_API_KEY)


def generate_gpt_response(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em finanças."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )

        content = completion.choices[0].message.content
        return content.strip() if content else "API retornou vazio (None)"

    except Exception as e:
        return f"Erro na API: {str(e)}"
