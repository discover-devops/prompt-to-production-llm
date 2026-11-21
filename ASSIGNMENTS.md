# Assignments: Prompt to Production

**By Rahul Chaubey**

Work through these after each topic. Concept questions check that you can explain the idea in your own words, the way you would to a customer or a manager. Hands-on tasks make you build it yourself. Challenge tasks are optional and go one step further.

How to submit: push your work to your own public GitHub repo, then share the link. Submit code, `.env.example` and outputs. Never submit `.env` or any API key.

---

## Table of Contents

- [Topic 1: Your First LLM API Call](#topic-1-your-first-llm-api-call)
  - Part A: The Problem
  - Part B: How programs talk to an LLM
  - Part C: The Toolkit
  - Part D: The Lab
  - Part E: Production Thinking
  - Topic 1 Capstone
- [Topic 2: Ship It](#topic-2-ship-it)
  - Part A: The Problem
  - Part B: The Four Guards
  - Part C: Cloud and Terraform
  - Part D: The Lab
  - Part E: Production Thinking
  - Topic 2 Capstone
- [Self Check](#self-check)

---

## Topic 1: Your First LLM API Call

### Part A: The Problem

**Concept questions**

1. In your own words, what is the problem ShopEase is trying to solve? Write the problem statement in one line.
2. Priya gets 500 emails a day at 3 minutes each. How many hours of reading is that? How many full-time people would it need at 8 hours a day?
3. Why do keyword rules fail? Give three different reasons, each with an example email.
4. The email "I do NOT want a refund, I want a replacement" was put in the Refund category by our rules. Explain why.
5. ChatGPT in the browser understood the Hinglish email correctly. Why is that still not a complete solution for ShopEase?

**Hands-on**

6. Write 5 new customer emails where keyword rules would fail. Use at least one Hinglish email, one with negation, and one with no obvious keyword.
7. Think of a problem from your own job where people read or sort text by hand (tickets, invoices, resumes, complaints). Write it as a ShopEase-style problem statement with the daily volume and the time it takes.

### Part B: How programs talk to an LLM

**Concept questions**

1. Where does the model actually run when you use ChatGPT? Why can a normal laptop still use it?
2. Explain an API using the restaurant analogy. Who is the customer, the waiter, the chef, the menu and the bill?
3. Give two examples of APIs you use every day in apps on your phone.
4. Why do programs exchange data in JSON instead of normal sentences? Give two reasons.
5. Name the three parts of every LLM API request and explain each in one line.
6. What is the difference between `instructions` (system message) and `input` (user message)?
7. Why is an API key compared to an ATM PIN? What can someone do with a leaked key?
8. Does a ChatGPT Plus subscription give you API access? Explain.
9. What is a token? Roughly how many tokens are in 100 English words?
10. Why are input tokens and output tokens priced separately? Which one is usually more expensive?
11. What is a context window? Why should we not send all 500 emails in one request?
12. The same idea works with OpenAI, Anthropic and Google, but the code differs. What differs?

**Hands-on**

13. Calculate the cost by hand: 1,200 input tokens and 300 output tokens, with input at $2.50 and output at $15.00 per million tokens. Show your working.
14. Using the same prices, ShopEase sends 10,000 emails a day with 40 input and 20 output tokens each. What is the cost per day and per month (30 days)?
15. Write, as JSON, an order slip that asks the model to translate an email into Hindi. Include model, instructions and input.

### Part C: The Toolkit

**Concept questions**

1. For each tool, write the problem it solves in one line: Python, SDK, pip, requirements.txt, venv, .env, python-dotenv, git, .gitignore.
2. What is the difference between a library and an SDK?
3. Two projects on your laptop need different versions of the openai library. What happens without venv? How does venv fix it?
4. Why do we commit `requirements.txt` but never commit `.env`?
5. What is the first thing you should do if your API key is pushed to GitHub? Why is deleting the commit not enough?

**Hands-on**

6. Create a fresh project folder with its own venv, install the libraries from a `requirements.txt`, and show the output of `pip list`.
7. Create a `.gitignore`, run `git init` and `git status`, and take a screenshot proving `.env` is not listed.

### Part D: The Lab

**Hands-on**

1. Run `raw_call.py`. From the JSON response, copy the summary text, input tokens, output tokens and total tokens.
2. Change the API key in `.env` to a wrong value and run `raw_call.py` again. What status code and error do you get? Fix it.
3. Run Step 3 twice. Record the input and output tokens of both runs. Which number changed and why?
4. Complete the lab up to Step 7 and submit `results.csv`.
5. Add your 5 emails from Part A to `emails.json` and run again.
6. From `results.csv`, fill in this table for your 15 emails:

| Model | Total input tokens | Total output tokens | Total cost | Your quality score out of 10 |
| ----- | ------------------ | ------------------ | ---------- | ---------------------------- |
| gpt-5.4 | | | | |
| gpt-5.4-mini | | | | |

7. Write 5 lines: which model would you recommend to ShopEase and why? Use both cost and quality.
8. Change the instructions so the model returns a summary AND a category (Refund, Delivery, Payment, Cancellation, Other). Run all emails. How many categories were correct?

**Challenge**

9. Add a third chef: any other model your key can use (list them with `models.list()`), with its prices. Compare all three.
10. Get a free Gemini key from https://aistudio.google.com and write a `summarise_with_gemini` function that returns the same three values: summary, input tokens, output tokens. Hint: Gemini puts the bill in `usage_metadata`.
11. Add a column for summary length in words. Does the cheaper model write shorter or longer summaries?

### Part E: Production Thinking

1. List five things that are missing before this script can be used by a real company.
2. Our script prints to the screen and writes a CSV. Who in a company would need these results, and in what form?
3. If OpenAI is down for 30 minutes, what happens to our script today? What should happen?

### Topic 1 Capstone

Pick a text problem from your own work (Part A, question 7). Build a version of the summariser for it: your own 10 sample inputs, your own instructions, two models compared, and a `results.csv` with cost. Write a one-page README explaining the problem, your design and your recommendation.

---

## Topic 2: Ship It

### Part A: The Problem

**Concept questions**

1. What is the difference between a demo and a product?
2. Explain the four disasters (silent break, two cooks one recipe, works on my laptop, the 2 AM failure) with an example from your own experience or company.
3. What happened in the July 2024 CrowdStrike incident, and what lesson does it teach about shipping software?
4. Match each disaster with its guard and its restaurant chain analogy.

### Part B: The Four Guards

**Concept questions**

1. What is a unit test? What are its two parts?
2. Why do we not test the exact words the AI writes?
3. What is a dummy chef (a fake client), and why do tests use one instead of the real LLM? Give three reasons.
4. Explain main, branch, pull request, review and merge using the head chef analogy.
5. Why is a pull request similar to maker-checker in a bank?
6. Explain Dockerfile, image and container, each in one line.
7. Why must the API key never be inside a Docker image?
8. What is the difference between `print()` and logging? Name the three common log levels.
9. Draw the shipping line from a code change to production.

**Hands-on**

10. Write a new test `test_cost_zero_tokens` that checks the cost is 0 when both token counts are 0.
11. Write a test that checks the cost for 2,000 input and 1,000 output tokens at $0.75 and $4.50 per million.

### Part C: Cloud and Terraform

**Concept questions**

1. Why do companies run production on cloud servers and not on laptops?
2. What is Infrastructure as Code? Why is it better than clicking in the console?
3. What is the difference between `terraform plan` and `terraform apply`?
4. A new AWS account has no default VPC. List the network pieces our Terraform creates and the job of each one.
5. Why is the SSH private key saved in the Downloads folder and not in the project?
6. Why does our security group open port 8000 even though Topic 2 does not use it?

**Hands-on**

7. Run `terraform plan` and count how many resources will be created. List them.
8. Change `allowed_cidr` in a `terraform.tfvars` file to your own public IP (find it at https://checkip.amazonaws.com) and apply again. What changed?

### Part D: The Lab

**Hands-on**

1. Build the server, install the tools, and show the output of `docker run hello-world`.
2. Complete Steps 3 to 5 and show `pytest -v` passing.
3. Do Step 6. Show the red test output and the `git diff` that caused it.
4. Make a GOOD change on a new branch: change the instructions to ask for a summary under 15 words. Run the tests, commit, merge to main, and show `git log --oneline`.
5. Build and run the Docker image. Show `ls output/` and the first 3 lines of `results.csv`.
6. Do Step 8 with a wrong model name. Copy the ERROR lines from the log and explain them.
7. Run the container with a wrong API key using `-e OPENAI_API_KEY=wrong`. What do the logs say?
8. Run `terraform destroy` and confirm all resources are gone.

**Challenge**

9. Push your project to a GitHub repo, create a branch, open a real pull request, and merge it through the GitHub website.
10. Add a GitHub Actions workflow that runs `pytest` automatically on every pull request.
11. Add a log line at WARNING level when a summary is longer than 30 words.
12. Make the Docker image smaller or faster to rebuild. Explain why copying `requirements.txt` before the code helps Docker's cache.

### Part E: Production Thinking

1. Our `.env` file sits on the server. What would a real company use instead?
2. Logs are printed in the terminal and disappear. Where should they go in a real company, and who should be alerted on ERROR?
3. The ticketing system cannot run our script. What do we need to build so other systems can call our summariser?
4. List three checks you would want to pass before any change reaches main.

### Topic 2 Capstone

Take your Topic 1 capstone project and ship it: add at least three tests using a fake client, use a branch for every change, package it in Docker with no secrets inside, add logs with INFO and ERROR, and run it on an EC2 server built with Terraform. Write a README explaining how a new teammate would run your project in under 10 minutes.

---

## Self Check

Can you explain each of these to a non-technical manager in one minute?

- Why keyword rules fail and an LLM does not
- What an API is, using the restaurant
- What travels in an LLM request and what comes back
- What a token is and how the cost is calculated
- Why the API key lives in `.env`
- The four guards of shipping: tests, branches and pull requests, Docker, logs
- Why we build cloud servers with Terraform

If yes, you are ready for the next topic: turning the summariser into a FastAPI service.

---

## Keep learning with me

- YouTube: https://www.youtube.com/@BuildAutomateArchitect
- System Design playlist: https://www.youtube.com/playlist?list=PLeAHTLMwFYQ0
- Telegram: https://t.me/BuildAutomateArchitect
- LinkedIn: https://www.linkedin.com/in/chaubeyrahul/
- Website: https://rahulchaubeyconsulting.com/
