import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

if not openrouter_api_key:
    raise ValueError("OPENROUTER API KEY NOT SET")


MAX_STEPS = 10  # safety limit so the loop can't run forever


def generate_headers():
    return {
        f"Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json",
    }


# -------------------------------------------------------
# YOUR PROMPT GOES HERE
# ReAct system prompt: model should interleave
# Thought: / Action: / Observation: until Finish[answer].
# Fill in the system_prompt string below.
# -------------------------------------------------------
SYSTEM_PROMPT = ""  # <-- your ReAct system prompt here


def call_model(messages: list) -> str:
    """Send the current conversation to the model and return the raw text reply."""
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


def parse_thought(text: str) -> str | None:
    """Extract the text after 'Thought:' on a line, if present."""
    for line in text.splitlines():
        if line.strip().startswith("Thought:"):
            return line.split("Thought:", 1)[1].strip()
    return None


def parse_action(text: str) -> tuple[str, str] | tuple[None, None]:
    """
    Extract action name and argument from a line like:
        Action: search[What is the capital of France]
    Returns (action_name, argument) or (None, None).
    """
    for line in text.splitlines():
        if line.strip().startswith("Action:"):
            action_text = line.split("Action:", 1)[1].strip()
            if "[" in action_text and action_text.endswith("]"):
                name = action_text[:action_text.index("[")].strip()
                arg = action_text[action_text.index("[") + 1:-1].strip()
                return name, arg
    return None, None


def execute_action(action_name: str, argument: str) -> str:
    """
    Dispatch an action and return an observation string.
    Stub implementations — replace with real tool logic.
    """
    action_name = action_name.lower()

    if action_name == "search":
        # TODO: plug in a real search (Wikipedia, SerpAPI, etc.)
        return f"[search stub] No result found for: {argument}"

    elif action_name == "lookup":
        # TODO: plug in a real lookup (e.g. within a retrieved document)
        return f"[lookup stub] No result found for: {argument}"

    elif action_name == "finish":
        # Finish is handled by the loop before reaching here
        return argument

    else:
        return f"Unknown action: {action_name}"


def react_loop(user_prompt: str) -> str:
    """
    Run the ReAct loop for a given user query.
    Returns the final answer from Finish[answer], or a timeout message.
    """
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

        thought = parse_thought(model_output)
        if thought:
            print(f"Thought: {thought}")

        action_name, argument = parse_action(model_output)

        if action_name is None:
            # Model didn't produce a valid Action line — add its output and
            # let it try again on the next step
            print("No action found in output. Continuing...\n")
            messages.append({"role": "assistant", "content": model_output})
            continue

        print(f"Action: {action_name}[{argument}]")

        # Finish ends the loop
        if action_name.lower() == "finish":
            print(f"\n{'='*60}")
            print(f"Final Answer: {argument}")
            print(f"{'='*60}\n")
            return argument

        # Run the action and get an observation
        observation = execute_action(action_name, argument)
        print(f"Observation: {observation}\n")

        # Add this turn to the conversation so the model can continue
        messages.append({"role": "assistant", "content": model_output})
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    print(f"Reached max steps ({MAX_STEPS}) without a Finish action.")
    return "No answer found within step limit."


react_loop("How far is the earth from the sun in miles?")
