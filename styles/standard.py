import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

if not openrouter_api_key:
    raise ValueError("OPENROUTER API KEY NOT SET")


# -------------------------------------------------------
# YOUR PROMPT GOES HERE
# Standard prompting: model answers directly from its
# own knowledge, no tools or reasoning steps.
# -------------------------------------------------------
SYSTEM_PROMPT = """
    You are a standard prompt, you will answer the users query based on your own knowledge.

    Rules:
    - You are NOT allowed to use external tools to answer the users query
    - You are NOT allowed to reason your way to an answer to answer the users query
    - State how you got to know the answer for the users query (state the source you used from model knowledge)
    - If you are NOT sure how to answers a users query because you DO NOT have the most up to date data, just try your best and answer.
    - DO NOT say you don't have the most up to date information. Just make your best GUESS and answer!
    - Do NOT ask the user to check external sources to better answer the question. 
    Example:
    users query: Who is Nvidia CEO?

    Jensen Huang




"""  # <-- your system prompt here


def generate_headers():
    return {
        f"Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json",
    }


def call_model(user_prompt: str) -> str:
    send = json.dumps({
        "model": "nvidia/nemotron-3-nano-30b-a3b:free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "reasoning": {"enabled": False}
    })

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=generate_headers(),
        data=send
    )

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Request failed: {response.status_code} {response.text}")


def standard_prompt(user_prompt: str) -> str:
    print(f"\n{'='*60}")
    print(f"Query: {user_prompt}")
    print(f"{'='*60}\n")

    answer = call_model(user_prompt)

    print(f"Answer:\n{answer}")
    print(f"\n{'='*60}\n")

    return answer


prompt = input("Enter your prompt! ")
standard_prompt(prompt)
