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
