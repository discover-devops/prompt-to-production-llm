# Prompt to Production: Build and Ship LLM Applications with Python

**From your first LLM API call to a tested, containerised AI service on the cloud.**
**By Rahul Chaubey**

---

## Who is this for?

Working professionals moving into AI engineering and Forward Deployed Engineering roles: engineers with a few years of experience, and leaders who want to truly understand how AI products are built and shipped. No machine learning background is needed. Basic Python helps.

## The story we follow

ShopEase is an e-commerce company. Priya, a support agent, receives 500 customer emails every day. Reading them takes 25 hours a day. We build, step by step, a program that reads every email, asks an AI to understand it, writes a one-line summary, measures the exact cost, and then we ship it like real production software.

One product. One story. It grows in every topic.

---

## Table of Contents

| Topic | What you learn | Where it runs | Folder |
| ----- | -------------- | ------------- | ------ |
| 1. Your First LLM API Call | Why AI, how programs talk to an LLM, JSON, tokens, cost, comparing models | Laptop + VS Code | [topic-1-first-llm-api-call](topic-1-first-llm-api-call/README.md) |
| 2. Ship It | Testing, Git branches and pull requests, Docker, logs, Terraform on AWS | AWS EC2 | [topic-2-ship-it](topic-2-ship-it/README.md) |
| Assignments | Questions and hands-on tasks for every part | Anywhere | [ASSIGNMENTS.md](ASSIGNMENTS.md) |

Every topic follows the same five parts:

```
Part A  The Problem        why do we need this at all
Part B  The Concept        how it works, explained with everyday examples
Part C  The Toolkit        every tool, and the problem it solves
Part D  The Lab            build it, one baby step at a time
Part E  Production Thinking what is still missing for a real company
```

---

## Repository layout

```
prompt-to-production-llm/
  README.md                         this page
  ASSIGNMENTS.md                    question set and hands-on tasks
  diagrams/
    Topic1-Your-First-LLM-API-Call.drawio   24 teaching pages
    Topic2-Ship-It.drawio                   12 teaching pages
  topic-1-first-llm-api-call/
    README.md                       theory + lab
    raw_call.py                     the LLM call by hand, raw JSON
    summariser.py                   final version of the lab
    emails.json                     10 sample customer emails
    requirements.txt
    .env.example                    copy to .env and add your key
  topic-2-ship-it/
    README.md                       theory + lab
    terraform/                      builds the AWS server from an empty account
    app/                            tested, logged, Dockerised summariser
```

## How to open the diagrams

Go to https://app.diagrams.net, choose **Open Existing Diagram**, and pick a `.drawio` file from the `diagrams` folder. Each file has many pages (tabs at the bottom). The theory pages tell you which diagram page to open.

## Before you start

1. Python 3.10 or above and VS Code.
2. An OpenAI API key with billing enabled at https://platform.openai.com. A ChatGPT Plus subscription is NOT API access. API billing is separate.
3. For Topic 2: an AWS account, AWS CLI configured, and Terraform installed.

## Golden rule

Never put an API key inside code, never commit `.env`, and always run `git status` before your first commit. If a key ever leaks, revoke it in the provider console immediately.

---

## Keep learning with me

I am Rahul Chaubey. I build and teach Cloud, DevOps and AI engineering the way it is done in real companies: problem first, then concept, then hands-on.

- YouTube: https://www.youtube.com/@BuildAutomateArchitect
- System Design playlist: https://www.youtube.com/playlist?list=PLeAHTLMwFYQ0
- Telegram: https://t.me/BuildAutomateArchitect
- LinkedIn: https://www.linkedin.com/in/chaubeyrahul/
- Website: https://rahulchaubeyconsulting.com/

If this helped you, star the repo and share it with one friend who is learning AI engineering.
