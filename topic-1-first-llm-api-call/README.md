# Topic 1: Your First LLM API Call

**Theme: From Python Code to Large Language Models**
**By Rahul Chaubey**

---

## Table of Contents

- [Part A: The Problem](#part-a-the-problem)
  - A1. A day at the ShopEase support desk
  - A2. Fix 1: write keyword rules
  - A3. Fix 2: use ChatGPT in the browser
- [Part B: How does a program talk to an LLM?](#part-b-how-does-a-program-talk-to-an-llm)
  - B1. Where does ChatGPT actually run?
  - B2. What is an API? The restaurant
  - B3. Why do programs speak JSON?
  - B4. The order slip: what we send
  - B5. The food and the bill: what comes back
  - B6. Three restaurants, same dish
- [Part C: The Toolkit](#part-c-the-toolkit)
- [Part D: The Lab](#part-d-the-lab)
  - Files we create and how they connect
  - Step 0 to Step 8
- [Part E: Production Thinking](#part-e-production-thinking)
- [Interview Questions](#interview-questions)

**Learning outcomes.** By the end you can explain how a Python program talks to an LLM, read the request and response JSON, measure input and output tokens, calculate the cost of every call, compare two models on cost and quality, and keep your API key safe.

---

## Part A: The Problem

### A1. A day at the ShopEase support desk

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **A1 ShopEase Support Desk**

Have you ever emailed Amazon, Flipkart or Swiggy support and waited two days for a reply? Here is why.

Meet Priya. She works at the support desk of ShopEase, an e-commerce company. Every morning she finds 500 new customer emails.

```
Email 1: I ordered a laptop five days ago. Tracking still says not dispatched.
Email 2: I ordered a laptop bag but received a mobile cover. I want a refund.
Email 3: My bank account was charged but the order page says payment failed.
```

For every email Priya must read it, understand the problem, decide the category (Refund, Delivery, Payment) and send it to the right team.

| Item | Value |
| ---- | ----- |
| Emails per day | 500 |
| Time per email | 3 minutes |
| Total | 1,500 minutes = 25 hours of reading, every day |

One Priya is not enough. Three Priyas still only read all day. Customers wait.

**Concept: The Problem Statement**
Read every customer email, understand what the customer wants, and summarise it in one line, automatically, for 500 emails a day.

### A2. Fix 1: write keyword rules

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **A2 Fix 1 Write Rules**

A programmer's first idea is keyword rules:

| If the email contains | Category |
| --------------------- | -------- |
| refund | Refund |
| delivery | Delivery |
| payment | Payment |

It works on the three easy emails. Now try these:

| Customer email | Rules say | Correct |
| -------------- | --------- | ------- |
| My money has been deducted, but I cannot see my order. | Unknown | Payment |
| I do NOT want a refund, I want a replacement. | Refund | Replacement |
| Paisa kat gaya but order nahi aaya | Unknown | Payment |
| 5 days!!! Still waiting. Worst service ever. | Unknown | Delivery |

Add more rules? Customers write in endless ways: new words, Hinglish, spelling mistakes, negation. 500 rules later, the 501st email still breaks it.

**Concept: Rules match WORDS. Customers write MEANING.** We need something that understands meaning.

### A3. Fix 2: use ChatGPT in the browser

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **A3 Fix 2 Use ChatGPT**

Paste "Paisa kat gaya but order nahi aaya" into ChatGPT and it answers correctly: payment deducted, order not created. It understands.

But is the problem solved? Priya now copy-pastes 500 emails into ChatGPT and 500 answers back into the ticket system. Nobody is there at 2 AM. Nobody knows what it costs.

```
TODAY:   Email -> Priya copy-paste -> ChatGPT website -> Priya copy-paste -> Ticket system
WE WANT: Email -> OUR PROGRAM -> AI model -> OUR PROGRAM -> Ticket system
```

**Concept: The INTELLIGENCE problem is solved. The AUTOMATION problem is not.** We need our own program to talk to the AI directly, with no website and no human in the middle.

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **A Summary**

---

## Part B: How does a program talk to an LLM?

### B1. Where does ChatGPT actually run?

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **B1 Where Does ChatGPT Run**

When you type in ChatGPT, the answer is not created on your laptop. The model is huge and runs in OpenAI's data centres on thousands of GPUs. Your browser sends your message over the internet and the answer travels back.

**Concept: the ChatGPT website is ALSO just a program talking to the model.** We will build our own program that talks to the same model directly.

### B2. What is an API? The restaurant

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **B2 API The Waiter**

| Restaurant | Our system |
| ---------- | ---------- |
| You, the customer | Our program |
| The waiter | The API |
| The kitchen and chef | The AI model |
| The menu | API documentation |
| The bill | Token usage |

You never walk into the kitchen. You order in a fixed way, and the food and the bill come back. You already use APIs every day: PhonePe talks to your bank through an API, Uber shows Google Maps through an API, Swiggy takes payment through Razorpay's API.

**Concept: API = Application Programming Interface.** A fixed, agreed way for one program to ask another program for something.

### B3. Why do programs speak JSON?

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **B3 Why JSON**

A waiter understands "2 paneer butter masala, less spicy, and 1 naan please". A computer does not know which word is the item and which is the quantity. Programs fill a form instead:

```json
{
    "item": "Paneer Butter Masala",
    "quantity": 2,
    "spice": "less"
}
```

| Symbol | Meaning |
| ------ | ------- |
| `{ }` | one complete form |
| `"item"` | the label, called a key |
| `"Paneer Butter Masala"` | the value |
| `2` | a number, no quotes |
| `[ ]` | a list of things |

**Concept: why JSON?** Both sides know exactly where each piece of data is, every programming language can read it, and humans can read it too.

Try it: open ChatGPT in Chrome, press F12, open the Network tab and send a message. Your message travels inside JSON.

### B4. The order slip: what we send

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **B4 The Order Slip Request**

Every LLM request has three parts:

| Part | Example | Restaurant |
| ---- | ------- | ---------- |
| Endpoint | `https://api.openai.com/v1/responses` | which restaurant and counter |
| API key | `Authorization: Bearer sk-...` | your membership card, who pays |
| JSON body | model, instructions, input | the order slip |

```json
{
    "model": "gpt-5.4",
    "instructions": "You are a customer support assistant. Summarise this email in one line.",
    "input": "Paisa kat gaya but order nahi aaya"
}
```

`model` is which chef, `instructions` are the house rules (the system message), `input` is the actual order (the user message).

**Concept: the API key is your ATM PIN.** Anyone who has it can order on your bill. Never share it, never put it in code, never push it to GitHub.

### B5. The food and the bill: what comes back

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **B5 Food and Bill Response**

The answer also comes back as JSON. Two parts matter: the generated text (the food) and `usage` (the bill).

**What is a token?** The model reads text in small pieces. `unbelievable` becomes `un + believ + able`. About 1 token is 3/4 of an English word. Hindi and Hinglish usually use more tokens for the same meaning.

**Concept: the taxi meter.** You pay per token in both directions: input tokens (what you send) and output tokens (what the model writes). Output usually costs more per token.

```
cost = input tokens / 1,000,000 x input price + output tokens / 1,000,000 x output price
```

Example from our real run with gpt-5.4 ($2.50 input, $15.00 output per million tokens): 35 input and 17 output tokens cost about $0.00034. Tiny for one email. At 10,000 emails a day it becomes a budget line.

**Context window = plate size.** A model can only read a limited number of tokens at once. Send only what is needed.

### B6. Three restaurants, same dish

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **B6 Three Restaurants**

| | OpenAI (GPT) | Anthropic (Claude) | Google (Gemini) |
| - | ------------ | ------------------ | --------------- |
| House rules go in | instructions | system | system_instruction |
| Answer is in | output_text | content[0].text | text |
| Bill is in | usage.input_tokens | usage.input_tokens | usage_metadata.prompt_token_count |

Same idea everywhere, different order forms. Companies use more than one for price, quality, backup, or because a customer allows only one. In this lab we use OpenAI.

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **B Summary**

---

## Part C: The Toolkit

Every tool exists because of a problem.

| Tool | The problem it solves | Analogy | Diagram page |
| ---- | --------------------- | ------- | ------------ |
| Laptop + VS Code | A place to write code (editor) and run it (terminal) | your desk | C1 Where Our Program Lives |
| Python | The language we write instructions in | the language of the recipe | C2 Python |
| SDK (openai library) | Writing the raw request by hand every time is slow | ready-made masala | C3 SDK Library |
| pip + requirements.txt | Everyone must install the same libraries | Play Store + shopping list | C4 pip and requirements |
| venv | Two projects need different library versions | separate tiffin boxes | C5 venv |
| .env + python-dotenv | The key must not live inside the code | a locker | C6 env Locker |
| git + .gitignore | Save and share code, never the secrets | do-not-pack list | C7 git and gitignore |

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **C Summary Toolkit**

---

## Part D: The Lab

### Files we create and how they connect

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **D0 Files We Create**

```
requirements.txt (shopping list) -> pip installs the tools
.env (locker: key, model, prices) ----+
emails.json (10 customer emails) -----+--> summariser.py --> results.csv
raw_call.py: Step 1 only, by hand     |    (the main file)   (final report)
.gitignore: never upload .env, venv, results.csv
```

Only one file really grows: `summariser.py`. After every step it runs.

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **D1 One File Grows**

### Step 0: Set up the project

Open VS Code, then Terminal, New Terminal. These commands are for Git Bash on Windows.

```bash
mkdir shopease-summariser
cd shopease-summariser
python --version
python -m venv venv
source venv/Scripts/activate
```

On PowerShell use `venv\Scripts\Activate.ps1`, on Mac use `source venv/bin/activate`. You should now see `(venv)` in the terminal: our private tiffin box is open.

### Step 0.1: Install the tools

```bash
cat > requirements.txt <<'EOF'
openai
python-dotenv
requests
EOF
pip install -r requirements.txt
```

`openai` is the ready-made order app, `python-dotenv` opens the locker, `requests` sends the order by hand in Step 1.

### Step 0.2: The locker and the do-not-pack list

```bash
cat > .env <<'EOF'
OPENAI_API_KEY=paste_your_openai_key_here
OPENAI_MODEL=gpt-5.4
EOF

cat > .gitignore <<'EOF'
.env
venv/
__pycache__/
results.csv
EOF
```

Open `.env` in VS Code and paste your real key. Model names change over time; if you get "model not found", list the models your key can use:

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); from openai import OpenAI; [print(m.id) for m in OpenAI().models.list() if m.id.startswith('gpt')]"
```

### Step 1: Send the order slip BY HAND

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **D2 By Hand vs SDK**

Before any ready-made tool, we do it the hard way once, to SEE what travels over the internet.

```python
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
```

```bash
python raw_call.py
```

| Code | Restaurant |
| ---- | ---------- |
| url | which restaurant and counter (endpoint) |
| headers with Authorization | our membership card (API key) |
| order_slip | the JSON order slip |
| requests.post | the waiter carries it to the kitchen |
| response.json() | the food and the bill come back in JSON |

In the long reply, find `"text"` (the summary) and `"usage"` (the bill). Status code 200 means success. A 401 means the key is wrong, which is exactly what you see if you forget to paste it. Notice that even errors come back as JSON, and OpenAI masks the key in the message.

### Step 2: Let the SDK do it

```bash
cat > summariser.py <<'EOF'
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model=os.getenv("OPENAI_MODEL"),
    instructions="You are a customer support assistant. Summarise this email in one line.",
    input="Paisa kat gaya but order nahi aaya",
)

print("SUMMARY:", response.output_text)
EOF
python summariser.py
```

No URL, no headers, no digging through JSON. Same order slip, same kitchen. The SDK does the boring work.

### Step 3: Read the bill

```bash
cat >> summariser.py <<'EOF'
print("INPUT TOKENS :", response.usage.input_tokens)
print("OUTPUT TOKENS:", response.usage.output_tokens)
EOF
python summariser.py
```

Run it twice. In our live run the input stayed at 35 tokens, while the output changed from 17 to 15 and the words changed. Same input, the chef cooks fresh every time. That is why we never test the exact words an AI writes.

### Step 4: Turn tokens into money

```bash
cat >> .env <<'EOF'
INPUT_PRICE=2.50
OUTPUT_PRICE=15.00
EOF

cat >> summariser.py <<'EOF'
input_price = float(os.getenv("INPUT_PRICE"))
output_price = float(os.getenv("OUTPUT_PRICE"))
cost = response.usage.input_tokens / 1_000_000 * input_price + response.usage.output_tokens / 1_000_000 * output_price
print(f"COST: ${cost:.6f}")
EOF
python summariser.py
```

Prices are USD per million tokens from https://openai.com/api/pricing (gpt-5.4 at the time of the session). Prices live in the locker, so a price change never touches the code.

### Step 5: Summarise all 10 emails

```bash
cat > emails.json <<'EOF'
[
  {"id": 1, "email": "I ordered a laptop five days ago. The tracking page still says not dispatched. Please help."},
  {"id": 2, "email": "I ordered a laptop bag but received a mobile cover. I want a refund."},
  {"id": 3, "email": "My bank account was charged but the order confirmation says payment failed."},
  {"id": 4, "email": "The headphones I received are damaged. The left side is not working."},
  {"id": 5, "email": "I want to cancel my order because I accidentally selected the wrong size."},
  {"id": 6, "email": "The delivery agent marked my package delivered, but I have not received it."},
  {"id": 7, "email": "I received two products instead of the three products I purchased."},
  {"id": 8, "email": "I was charged twice for the same order. Please investigate."},
  {"id": 9, "email": "Paisa kat gaya but order nahi aaya"},
  {"id": 10, "email": "I do NOT want a refund, I want a replacement."}
]
EOF

cat > summariser.py <<'EOF'
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
input_price = float(os.getenv("INPUT_PRICE"))
output_price = float(os.getenv("OUTPUT_PRICE"))

with open("emails.json") as file:
    emails = json.load(file)

for email in emails:
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL"),
        instructions="You are a customer support assistant. Summarise this email in one line.",
        input=email["email"],
    )
    cost = response.usage.input_tokens / 1_000_000 * input_price + response.usage.output_tokens / 1_000_000 * output_price
    print(f"Email {email['id']} | {response.output_text} | ${cost:.6f}")
EOF
python summariser.py
```

The loop does what Priya did by hand. Emails 9 and 10 are the two that broke our keyword rules in Part A. Watch the AI get them right.

### Step 6: Same restaurant, two chefs

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **D3 Two Chefs Same Shape**

Every customer asks an FDE: can we use the smaller model and save money? Let us answer with data.

```bash
cat >> .env <<'EOF'
OPENAI_MODEL_2=gpt-5.4-mini
INPUT_PRICE_2=0.75
OUTPUT_PRICE_2=4.50
EOF

cat > summariser.py <<'EOF'
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHEFS = {
    os.getenv("OPENAI_MODEL"): (float(os.getenv("INPUT_PRICE")), float(os.getenv("OUTPUT_PRICE"))),
    os.getenv("OPENAI_MODEL_2"): (float(os.getenv("INPUT_PRICE_2")), float(os.getenv("OUTPUT_PRICE_2"))),
}

with open("emails.json") as file:
    emails = json.load(file)

for email in emails:
    for model, (input_price, output_price) in CHEFS.items():
        response = client.responses.create(
            model=model,
            instructions="You are a customer support assistant. Summarise this email in one line.",
            input=email["email"],
        )
        cost = response.usage.input_tokens / 1_000_000 * input_price + response.usage.output_tokens / 1_000_000 * output_price
        print(f"Email {email['id']} | {model:12} | ${cost:.6f} | {response.output_text}")
EOF
python summariser.py
```

`CHEFS` is a menu of two chefs. Compare each pair: is the mini's summary three times worse, or just as good for a third of the price?

### Step 7: Save the results and print the final bill

This is the final version of the lab, also saved in this folder as `summariser.py`.

```python
import os
import csv
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHEFS = {
    os.getenv("OPENAI_MODEL"): (float(os.getenv("INPUT_PRICE")), float(os.getenv("OUTPUT_PRICE"))),
    os.getenv("OPENAI_MODEL_2"): (float(os.getenv("INPUT_PRICE_2")), float(os.getenv("OUTPUT_PRICE_2"))),
}

with open("emails.json") as file:
    emails = json.load(file)

rows = []
for email in emails:
    for model, (input_price, output_price) in CHEFS.items():
        try:
            response = client.responses.create(
                model=model,
                instructions="You are a customer support assistant. Summarise this email in one line.",
                input=email["email"],
            )
            cost = response.usage.input_tokens / 1_000_000 * input_price + response.usage.output_tokens / 1_000_000 * output_price
            rows.append({"email_id": email["id"], "model": model, "summary": response.output_text,
                         "input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens,
                         "cost_usd": round(cost, 6)})
            print(f"Email {email['id']} | {model:12} | done")
        except Exception as error:
            print(f"Email {email['id']} | {model:12} | FAILED | {error}")

with open("results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("\n===== FINAL BILL =====")
for model in CHEFS:
    total = sum(r["cost_usd"] for r in rows if r["model"] == model)
    print(f"{model:12} | ${total:.6f}")
print("Saved: results.csv")
```

```bash
python summariser.py
```

`try/except` means one failed call never stops the other 19. `results.csv` is the report the support manager opens in Excel. The final bill shows which chef was cheaper; read the summaries to judge which was better.

### Step 8: Prove our key is safe

```bash
git init
git status
```

You should see `summariser.py`, `raw_call.py`, `emails.json`, `requirements.txt` and `.gitignore`. You must NOT see `.env`, `venv/` or `results.csv`. If `.env` appears, stop and fix `.gitignore` before any commit.

---

## Part E: Production Thinking

> Diagram: open `../diagrams/Topic1-Your-First-LLM-API-Call.drawio` in draw.io, page **D Summary Today vs Production**

We started with Priya reading 500 emails by hand. Now a program reads every email, asks the AI, knows the exact cost, compares two models and saves a report. But it still runs only on one laptop.

| Today | A real company needs | Where we learn it |
| ----- | -------------------- | ----------------- |
| A script run by hand | A web service other systems can call | FastAPI service |
| Fails and moves on | Retries and timeouts | FastAPI service |
| Free-text summary | Validated structured output | FastAPI service |
| print and CSV | Proper logs | Topic 2 |
| Runs on my laptop | Tested, reviewed, packaged in Docker, on the cloud | Topic 2 |

---

## Interview Questions

1. Where does an LLM actually run when you use ChatGPT?
2. Explain an API to a non-technical person in one line.
3. Why do APIs use JSON instead of plain sentences?
4. What are the parts of an LLM API request?
5. Why do we track input and output tokens separately?
6. Does a ChatGPT Plus subscription give you API access?
7. What is the difference between calling the API directly and using the SDK?
8. The same email gives different output tokens on two runs. Why?
9. Why are the model name and prices in `.env` and not in the code?
10. How would you decide between a big model and a mini model?

Practice tasks are in [ASSIGNMENTS.md](../ASSIGNMENTS.md).

---

## Keep learning with me

I am Rahul Chaubey. I build and teach Cloud, DevOps and AI engineering the way it is done in real companies: problem first, then concept, then hands-on.

- YouTube: https://www.youtube.com/@BuildAutomateArchitect
- System Design playlist: https://www.youtube.com/playlist?list=PLeAHTLMwFYQ0
- Telegram: https://t.me/BuildAutomateArchitect
- LinkedIn: https://www.linkedin.com/in/chaubeyrahul/
- Website: https://rahulchaubeyconsulting.com/

If this helped you, star the repo and share it with one friend who is learning AI engineering.
