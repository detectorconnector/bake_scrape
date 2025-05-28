import requests

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
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'mistral',
                'prompt': prompt,
                'stream': False
            }
        )

        reply = response.json().get('response', '')
        parts = reply.split('\n')

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
