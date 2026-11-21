import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# WHERE to send it (the restaurant counter)
url = "https://api.openai.com/v1/responses"

# WHO is asking (our membership card)
headers = {
    "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY"),
    "Content-Type": "application/json",
}

# WHAT we want (the order slip)
order_slip = {
    "model": os.getenv("OPENAI_MODEL"),
    "instructions": "You are a customer support assistant. Summarise this email in one line.",
    "input": "Paisa kat gaya but order nahi aaya",
}

print("=== WHAT WE SEND (the order slip) ===")
print(json.dumps(order_slip, indent=4))

response = requests.post(url, headers=headers, json=order_slip, timeout=60)

print("\n=== WHAT COMES BACK (status code", response.status_code, ") ===")
print(json.dumps(response.json(), indent=4))
