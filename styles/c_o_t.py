import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

if not openrouter_api_key:
    raise ValueError("OPENROUTER API KEY NOT SET")




def generate_headers():
    return {
        f"Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json",
    }


def make_request(user_prompt: str):
    # -------------------------------------------------------
    # YOUR PROMPT GOES HERE
    # Chain-of-Thought: model should reason step-by-step,
    # but take no external actions. Fill in the system prompt.
    # -------------------------------------------------------
    system_prompt = ""  # <-- your CoT system prompt here

    send = json.dumps({
        "model": "nvidia/nemotron-3-nano-30b-a3b:free",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "reasoning": {"enabled": False}
    })

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=generate_headers(),
        data=send
    )

    if response.status_code == 200:
        response = response.json()
        return response['choices'][0]['message']
    else:
        raise Exception(f"Request failed: {response.status_code} {response.text}")


result = make_request("How far is the earth from the sun in miles?")
print(result)
