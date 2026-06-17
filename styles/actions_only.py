import requests
import json
import re
from dotenv import load_dotenv
from ddgs import DDGS
import os

load_dotenv()

openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

if not openrouter_api_key:
    raise ValueError("OPENROUTER API KEY NOT SET")


MAX_STEPS = 10  # safety limit so the loop can't run forever

# -------------------------------------------------------
# YOUR PROMPT GOES HERE
# Actions-only: model answers using only Action: calls,
# no Thought step. Tools: search[entity], lookup[string], Finish[answer]
# -------------------------------------------------------
SYSTEM_PROMPT = """
    You are an action only agent. For every query given by a users prompt, you are only allowed to make actions, by using the following tools:
    - search tool which returns up to 3 result snippets
    - lookup tool which allows you to find a word or phrase in a sentence, similar to ctrl + f tool
    - finish tool when you have an answer and are done
    You are not allowed to hallucinate or just guess answers to users prompts. you MUST use the following tools discussed above.


    These are the available tools:
    
    search[query] -> search the web. write short, clear, factual search queries (2-8 words max)
    lookup[phrase] ->  Search for a specific word or phrase inside previous observations (like Ctrl+F).
    finish[answer] -> use this when you have enough information to answer the users prompt. write the final answer clearly

    Rules:
    - Output **only one action per response**.
    - After I give you the Observation, think again and output the next single action.
    - Only output in this format:

    Action X: toolname[argument]

    - Do not output multiple actions at once.
    - Do not add extra text or explanations.
    
    here is an example:

    Question: How far is Earth from the Moon?

    Action 1: search[Earth to Moon distance miles]
    Action 2: lookup[miles]
    Action 3: finish[238,855 miles]

    Now solve the user's question using only actions.


    In your response you will include the actions you took along with the tool and how the tool was used. Follow the example i've given.




"""
  # <-- your actions-only system prompt here

# stores the last search result so lookup[] can scan it
_last_search_result = ""


def generate_headers():
    return {
        f"Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json",
    }


# --- Tools ---

def search(query: str) -> str:
    """DuckDuckGo search — returns up to 5 result snippets."""
    global _last_search_result
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            if not results:
                return "No results found."
            formatted = []
            for r in results:
                formatted.append(f"Title: {r.get('title', '')}\nSnippet: {r.get('body', '')[:300]}")
            _last_search_result = "\n\n".join(formatted)
            return _last_search_result
    except Exception as e:
        return f"Search failed: {str(e)}"


def lookup(term: str) -> str:
    """Scan the last search result for a sentence containing the term."""
    if not _last_search_result:
        return "No previous search to look up from."
    for sentence in _last_search_result.split("."):
        if term.lower() in sentence.lower():
            return sentence.strip()
    return f"'{term}' not found in the last search result."


def execute_action(action_name: str, argument: str) -> str:
    action_name = action_name.lower()
    if action_name == "search":
        return search(argument)
    elif action_name == "lookup":
        return lookup(argument)
    elif action_name == "finish":
        return argument  # handled by the loop before reaching here
    else:
        return f"Unknown action: {action_name}"


# --- Parsing ---

KNOWN_TOOLS = {"search", "lookup", "finish"}

def parse_all_actions(text: str) -> list[tuple[str, str]]:
    """
    Extract all actions from model output in order. Handles:
        Action 1: search[query]      — numbered with prefix
        Action 1: search [query]     — space before bracket
        search[query]                — bare tool call, no prefix
    Returns a list of (action_name, argument) tuples.
    """
    actions = []
    for line in text.splitlines():
        stripped = line.strip()

        # strip "Action X:" prefix if present
        if re.match(r'Action\s*\d*\s*:', stripped, re.IGNORECASE):
            stripped = re.split(r'Action\s*\d*\s*:', stripped, maxsplit=1)[1].strip()

        # match toolname[argument] or toolname [argument]
        match = re.match(r'(\w+)\s*\[(.+)\]', stripped)
        if match and match.group(1).lower() in KNOWN_TOOLS:
            actions.append((match.group(1), match.group(2).strip()))

    return actions


# --- Main loop ---

def call_model(messages: list) -> str:
    send = json.dumps({
        "model": "nvidia/nemotron-3-nano-30b-a3b:free",
        "messages": messages,
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


def actions_loop(user_prompt: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    print(f"\n{'='*60}")
    print(f"Query: {user_prompt}")
    print(f"{'='*60}\n")

    for step in range(1, MAX_STEPS + 1):
        print(f"--- Step {step} ---")

        model_output = call_model(messages)
        print(f"Model output:\n{model_output}\n")

        actions = parse_all_actions(model_output)

        if not actions:
            print("No actions found in output. Continuing...\n")
            messages.append({"role": "assistant", "content": model_output})
            continue

        # execute all actions from this response in order
        observations = []
        final_answer = None
        for action_name, argument in actions:
            print(f"Action: {action_name}[{argument}]")

            if action_name.lower() == "finish":
                final_answer = argument
                break

            observation = execute_action(action_name, argument)
            print(f"Observation: {observation}\n")
            observations.append(f"Observation ({action_name}): {observation}")

        if final_answer is not None:
            print(f"\n{'='*60}")
            print(f"Final Answer: {final_answer}")
            print(f"{'='*60}\n")
            return final_answer

        messages.append({"role": "assistant", "content": model_output})
        messages.append({"role": "user", "content": "\n".join(observations)})

    print(f"Reached max steps ({MAX_STEPS}) without a Finish action.")
    return "No answer found within step limit."



prompt = input("Enter your prompt! ")
actions_loop(prompt)
