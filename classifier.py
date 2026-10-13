import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an inbound message triage assistant for a property management
and real estate business.

Your job is to classify each incoming message into exactly one category,
assign the correct operational queue, and determine whether the message
requires urgent attention.

Categories and queues:

1. rent_finance
   Queue: support
   Use for rent, monthly rent amounts, rent payments, invoices,
   balances, deposits, refunds, financial questions, or payment problems.
   If a message asks how much rent costs, how much rent is due,
   or whether rent has been paid, classify it as rent_finance.

2. maintenance
   Queue: operations
   Use for repairs, property damage, utilities, plumbing, electrical,
   appliances, access problems, or other property maintenance issues.

3. listing
   Queue: support
   Use for property listings, availability, viewing requests,
   property details, or requests to advertise a property.
   Do not use listing for questions specifically asking about
   the monthly rent amount.

4. investment
   Queue: partnerships
   Use for investment opportunities, investors, partnerships,
   property investment questions, or requests to discuss investment deals.

Urgency must be assessed independently of category.

Set urgent=true when the message describes an immediate or potentially
dangerous situation requiring rapid human attention, such as flooding,
fire, gas leaks, serious electrical hazards, security threats, or another
situation where significant damage or harm could occur.

Set urgent=false for normal requests that can follow the standard queue.

Return ONLY valid JSON in exactly this structure:

{
  "category": "rent_finance | maintenance | listing | investment",
  "queue": "support | operations | partnerships",
  "urgent": true,
  "reason": "Brief explanation of the classification"
}

Do not invent information that is not present in the message.
"""

def classify_message(message: str) -> dict:
    response = client.responses.create(
        model="gpt-5.4-mini",
        instructions=SYSTEM_PROMPT,
        input=message,
    )

    result = response.output_text.strip()

    try:
        classification = json.loads(result)
    except json.JSONDecodeError:
        raise ValueError(f"Model returned invalid JSON: {result}")

    return classification


if __name__ == "__main__":
    message = input("Enter inbound message: ")

    result = classify_message(message)

    print(json.dumps(result, indent=2))
