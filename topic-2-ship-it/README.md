# Topic 2: Ship It

**Testing, Git, Docker and Logs, on a real cloud server**
**By Rahul Chaubey**

---

## Table of Contents

- [Part A: The Problem](#part-a-the-problem)
  - A1. It works on my laptop, now what?
  - A2. Four real disasters
  - A3. A restaurant chain has four guards
- [Part B: The Four Guards](#part-b-the-four-guards)
  - B1. Testing, the taste test
  - B2. Git branch and pull request, head chef approval
  - B3. Docker, ship the kitchen with the dish
  - B4. Logs, the black box
  - B5. The shipping line
- [Part C: Why the cloud, and Terraform](#part-c-why-the-cloud-and-terraform)
- [Part D: The Lab on AWS EC2](#part-d-the-lab-on-aws-ec2)
- [Part E: Production Thinking](#part-e-production-thinking)
- [Interview Questions](#interview-questions)

**Learning outcomes.** By the end you can explain why working code is not shippable code, write a unit test with a fake LLM, use a branch to protect the main code, package an AI app in Docker without leaking secrets, read logs to fix a failure, and build a cloud server from an empty AWS account with Terraform.

---

## Part A: The Problem

### A1. It works on my laptop, now what?

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-A1 It Works on My Laptop**

Topic 1 was a success. The manager says: ship it. Run it every day for 500 emails on the company server, and 5 engineers will keep improving it.

At home you cook dal for your family. A restaurant chain cooks the same dal, in 50 kitchens, every day, at the same taste. Shipping means going from home cook to restaurant chain.

**Concept: code that works once on one laptop is a DEMO. Code that works every day, for everyone, on any server, is a PRODUCT.**

### A2. Four real disasters

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-A2 Four Disasters**

| Disaster | The story | Root cause |
| -------- | --------- | ---------- |
| Silent break | Ravi edits the code on Friday. Cost now shows the wrong value. Nobody notices for a week. | Nobody checked |
| Two cooks, one recipe | Ravi and Sneha edit the same file. One overwrites the other. A day of work is lost. | Nobody reviewed |
| Works on my laptop | The server has a different Python and no openai library. It crashes. | Different kitchen |
| The 2 AM failure | The job fails at night. Morning: 500 emails not done. Why? Nobody knows. | No record |

Real world: in July 2024, one faulty software update from CrowdStrike crashed millions of Windows computers. Airlines, banks and hospitals stopped. Shipping without enough checks is expensive.

### A3. A restaurant chain has four guards

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-A3 Four Guards**

| Disaster | Restaurant chain fix | Software fix |
| -------- | -------------------- | ------------ |
| Silent break | Taste test before serving | Testing (pytest) |
| Two cooks, one recipe | Head chef approves recipe changes | Git branch + pull request |
| Works on my laptop | Same kitchen kit in every branch | Docker |
| The 2 AM failure | CCTV and logbook | Logs |

---

## Part B: The Four Guards

### B1. Testing, the taste test

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-B1 Guard 1 Testing**

A test is a known input and an expected answer. `pytest` runs all tests and shows green (passed) or red (failed).

```python
def test_cost():
    # 1000 input tokens at $2, 500 output tokens at $8 = $0.006
    assert round(calculate_cost(1000, 500, 2.0, 8.0), 6) == 0.006
```

What do we test? Our own logic: the cost maths, and that we read the response correctly. Not the exact words the AI writes, because they change every run.

**Concept: the dummy chef.** Tests use a fake response instead of the real LLM. No internet, no cost, same answer every time, runs in seconds.

### B2. Git branch and pull request, head chef approval

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-B2 Guard 2 Git PR**

| Step | Restaurant | Software |
| ---- | ---------- | -------- |
| 1 | The official recipe | main |
| 2 | Ravi's draft copy | branch |
| 3 | Please review my change | pull request |
| 4 | Head chef tastes it, tests run | review |
| 5 | Approved, becomes official | merge |

It is maker-checker in a bank: one person makes the change, another approves it. Git is version history for code: every change has a name, a time and a reason.

### B3. Docker, ship the kitchen with the dish

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-B3 Guard 3 Docker**

| Word | Meaning | Analogy |
| ---- | ------- | ------- |
| Dockerfile | instructions for what goes in the box | packing list |
| Image | the sealed box, built once | sealed shipping container |
| Container | the box running on a machine | the container opened at the port |

Inside the box: Python, the libraries and our code. Not inside the box: the API key. It is handed in when the box runs.

**Concept: like a shipping container, one standard box works on any ship and any port.** "Works on my laptop" becomes "works in the box, and the box works everywhere".

### B4. Logs, the black box

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-B4 Guard 4 Logs**

```
02:13:05 | INFO  | Email 41 | gpt-5.4 | tokens 35+15 | $0.000313
02:13:07 | ERROR | Email 42 | gpt-wrong | FAILED | model not found
```

| Level | Meaning |
| ----- | ------- |
| INFO | all good, recorded |
| WARNING | look at this soon |
| ERROR | something failed |

`print` is shouting in the kitchen: gone once said. A log is the written logbook with time and severity. Never write API keys or private customer data in logs.

### B5. The shipping line

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-B Summary Shipping Line**

```
change on a branch -> pytest -> pull request review -> merge to main
   -> docker build -> docker run on the server -> logs
```

---

## Part C: Why the cloud, and Terraform

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-D1 Lab Infrastructure Terraform**

Production does not run on laptops. It runs on servers in the cloud. Our AWS account is completely empty, with no default network. Clicking 50 times in the console cannot be repeated or reviewed, so we write the setup as code. That is Terraform.

**Concept: Infrastructure as Code is a recipe card for the cloud.** Same card, same kitchen, every time.

| File | What it builds |
| ---- | -------------- |
| providers.tf | AWS, Mumbai region (ap-south-1) |
| variables.tf | settings: region, server size, who may SSH in |
| network.tf | VPC, internet gateway, public subnet, route table, security group (22 and 8000) |
| ec2.tf | Ubuntu 24.04 image, SSH key saved in your Downloads folder, t3.medium server |
| outputs.tf | public IP and the ready SSH command |

The private key is saved outside the project on purpose, because the project goes to GitHub.

---

## Part D: The Lab on AWS EC2

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-D2 Lab Steps**

### Step 1: Build the server with Terraform (on your laptop)

```bash
cd topic-2-ship-it/terraform
aws sts get-caller-identity
terraform init
terraform plan
terraform apply -auto-approve
```

`plan` is the shopping bill before you pay: it lists everything it will create without creating anything. `apply` builds it in about 3 minutes.

### Step 2: Log in and install the tools

```bash
terraform output -raw ssh_command
```

Run the printed command, then on the server:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip git docker.io
sudo usermod -aG docker ubuntu
newgrp docker
docker run hello-world
```

A fresh server has nothing. We install by hand so you see exactly what production needs. Using PuTTY: convert the `.pem` key to `.ppk` with PuTTYgen first.

### Step 3: Project, venv and the locker on the server

```bash
mkdir shopease-summariser && cd shopease-summariser
python3 -m venv venv
source venv/bin/activate
pip install openai python-dotenv pytest

cat > .env <<'EOF'
OPENAI_API_KEY=paste_your_openai_key_here
OPENAI_MODEL=gpt-5.4
OPENAI_MODEL_2=gpt-5.4-mini
INPUT_PRICE=2.50
OUTPUT_PRICE=15.00
INPUT_PRICE_2=0.75
OUTPUT_PRICE_2=4.50
EOF
nano .env
```

Paste your real key in `nano`, then save with Ctrl+O, Enter, Ctrl+X.

### Step 4: Create the final project, all files in one go

The files are in `topic-2-ship-it/app/`. Copy them to the server, or create them with these commands.

**requirements.txt, .gitignore, .dockerignore**

```bash
cat > requirements.txt <<'EOF'
openai
python-dotenv
EOF

cat > .gitignore <<'EOF'
.env
venv/
__pycache__/
.pytest_cache/
output/
EOF

cat > .dockerignore <<'EOF'
.env
venv/
__pycache__/
.pytest_cache/
output/
.git
EOF
```

**emails.json** is the same file as in Topic 1.

**summariser.py**: the same summariser, now with logs, small testable functions, and output saved to the `output` folder.

```python
import os
import csv
import json
import logging
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("shopease")

INSTRUCTIONS = "You are a customer support assistant. Summarise this email in one line."


def calculate_cost(input_tokens, output_tokens, input_price, output_price):
    return input_tokens / 1_000_000 * input_price + output_tokens / 1_000_000 * output_price


def summarise(client, model, email_text):
    response = client.responses.create(model=model, instructions=INSTRUCTIONS, input=email_text)
    return response.output_text, response.usage.input_tokens, response.usage.output_tokens


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        log.error("OPENAI_API_KEY is missing. Check the .env file.")
        raise SystemExit(1)

    client = OpenAI(api_key=api_key)
    chefs = {
        os.getenv("OPENAI_MODEL"): (float(os.getenv("INPUT_PRICE")), float(os.getenv("OUTPUT_PRICE"))),
        os.getenv("OPENAI_MODEL_2"): (float(os.getenv("INPUT_PRICE_2")), float(os.getenv("OUTPUT_PRICE_2"))),
    }

    with open("emails.json") as file:
        emails = json.load(file)

    rows = []
    for email in emails:
        for model, (input_price, output_price) in chefs.items():
            try:
                summary, input_tokens, output_tokens = summarise(client, model, email["email"])
                cost = calculate_cost(input_tokens, output_tokens, input_price, output_price)
                rows.append({"email_id": email["id"], "model": model, "summary": summary,
                             "input_tokens": input_tokens, "output_tokens": output_tokens,
                             "cost_usd": round(cost, 6)})
                log.info("Email %s | %s | tokens %s+%s | $%.6f", email["id"], model, input_tokens, output_tokens, cost)
            except Exception as error:
                log.error("Email %s | %s | FAILED | %s", email["id"], model, error)

    if not rows:
        log.error("No email was summarised. Read the errors above.")
        raise SystemExit(1)

    os.makedirs("output", exist_ok=True)
    with open("output/results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    for model in chefs:
        total = sum(r["cost_usd"] for r in rows if r["model"] == model)
        log.info("FINAL BILL | %s | $%.6f", model, total)
    log.info("Saved output/results.csv")


if __name__ == "__main__":
    main()
```

**test_summariser.py**: the taste test with a dummy chef.

```python
from types import SimpleNamespace
from summariser import calculate_cost, summarise


def test_cost():
    # 1000 input tokens at $2, 500 output tokens at $8 = $0.006
    assert round(calculate_cost(1000, 500, 2.0, 8.0), 6) == 0.006


class DummyChef:
    """A fake OpenAI client. No internet, no cost, same answer every time."""

    def __init__(self):
        self.responses = SimpleNamespace(create=self.create)

    def create(self, model, instructions, input):
        return SimpleNamespace(
            output_text="Payment deducted, order not created.",
            usage=SimpleNamespace(input_tokens=35, output_tokens=10),
        )


def test_summarise_returns_summary_and_tokens():
    summary, input_tokens, output_tokens = summarise(DummyChef(), "any-model", "Paisa kat gaya")
    assert summary == "Payment deducted, order not created."
    assert input_tokens == 35
    assert output_tokens == 10
```

**Dockerfile**: the packing list.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY summariser.py emails.json ./
CMD ["python", "summariser.py"]
```

| File | Role |
| ---- | ---- |
| summariser.py | the product, with logs and testable functions |
| test_summariser.py | taste test, uses a fake OpenAI client |
| Dockerfile | packing list for the box |
| .dockerignore | keeps the key out of the box |
| .gitignore | keeps the key out of git |

```bash
python summariser.py
```

### Step 5: Taste test and the first git save

```bash
pytest -v
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git init -b main
git add .
git status
git commit -m "ShopEase summariser: first working version"
```

Two tests pass in green. `git status` shows no `.env` and no `venv`. The commit saves the official recipe on `main`.

### Step 6: Ravi breaks the code, the test catches him

```bash
git checkout -b ravi-cost-change
sed -i 's|input_tokens / 1_000_000|input_tokens / 1_000|' summariser.py
git diff
pytest -v
```

Ravi works on his own branch. `git diff` shows exactly what he changed. pytest fails in red: it expected $0.006 and got about $2.004. Caught in seconds, not after a week.

```bash
git checkout -- summariser.py
pytest -v
git checkout main
git merge ravi-cost-change
git log --oneline
```

The broken change is thrown away and tests are green again. On GitHub this merge would be a pull request: a teammate reviews it and the tests run automatically. Red tests mean no merge.

### Step 7: Pack it in Docker and run it

> Diagram: open `../diagrams/Topic2-Ship-It.drawio` in draw.io, page **T2-D3 Docker Volume**

```bash
docker build -t shopease-summariser .
docker images
docker run --rm --env-file .env -v "$PWD/output:/app/output" shopease-summariser
ls output/
```

| Part | Meaning |
| ---- | ------- |
| docker build -t | follow the Dockerfile and seal the image, named shopease-summariser |
| docker run --rm | open the box and run it; remove the stopped container afterwards |
| --env-file .env | hand the key to the box at run time; it is never inside the image |
| -v "$PWD/output:/app/output" | connect the server's output folder to the box's output folder |

**Concept: what is -v?** A volume. `$PWD` is the folder you are in. Left of the colon is the server folder, right of the colon is the folder inside the box. A container is a sealed tiffin box: anything written inside is thrown away when it closes. The volume is a pipe from the box to the server shelf, so `results.csv` survives.

### Step 8: The 2 AM failure. Break the config, read the logs, fix it

```bash
docker run --rm --env-file .env -e OPENAI_MODEL=gpt-wrong -v "$PWD/output:/app/output" shopease-summariser 2>&1 | tee run.log
grep ERROR run.log | head -3
```

`-e` overrides one setting, simulating a typo in the model name. The log shows exactly what failed, for which email and model, and when. The other model still worked: one failure did not stop the job.

```bash
docker run --rm --env-file .env -v "$PWD/output:/app/output" shopease-summariser
```

Fixed in seconds because the log pointed to the exact problem.

### Cleanup (on your laptop)

```bash
cd topic-2-ship-it/terraform
terraform destroy -auto-approve
```

One command builds, one command cleans, so the bill stops.

---

## Part E: Production Thinking

We shipped the summariser like a restaurant chain: taste-tested, reviewed, packed with its kitchen, CCTV on, on a real cloud server. What is still missing?

| Today | A real company needs |
| ----- | -------------------- |
| A script a person runs | A service other systems can call, for example a FastAPI endpoint |
| Tests run by hand | Tests run automatically on every pull request (CI) |
| Branch merged on the server | Pull requests on GitHub with review rules on main |
| Logs in the terminal | Logs collected in one place and alerts on ERROR |
| .env file on the server | A secrets manager, for example AWS Secrets Manager |
| One server built by hand | Deployments that roll out and roll back safely |

---

## Interview Questions

1. What is the difference between a demo and production software?
2. Why should unit tests not call the real LLM?
3. Why do teams never push directly to main?
4. Image vs container: what is the difference?
5. Why must secrets never be baked into a Docker image?
6. What does `-v` do in `docker run`, and why did we need it?
7. print() vs logging: why do production apps use logging?
8. terraform plan vs terraform apply?
9. A new AWS account has no default VPC. What must exist before an EC2 server can reach the internet?
10. Walk me through how a code change reaches production safely.

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
