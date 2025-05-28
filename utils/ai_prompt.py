import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_outreach(text):
    prompt = f"""
Given this business content:

{text}

Generate:
1. Two personalized business ideas for the prospect.
2. Three smart questions to ask in a meeting.
3. A short cold email or LinkedIn opener.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
        parts = reply.split("\n")

        return {
            "ideas": "\n".join([p for p in parts if p.startswith("1.") or p.startswith("2.")]),
            "questions": "\n".join([p for p in parts if "?" in p]),
            "opener": "\n".join([p for p in parts if "email" in p.lower() or "LinkedIn" in p])
        }
    except Exception as e:
        return {
            "ideas": "Error generating ideas.",
            "questions": str(e),
            "opener": ""
        }
