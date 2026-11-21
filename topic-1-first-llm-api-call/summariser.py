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
