#Sends prompts to LLaMa container
import requests

LLAMA_URL = "http://llama:8080/completion"

def generate(prompt: str):
    payload = {
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.2
    }

    response = requests.post(LLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["content"]
