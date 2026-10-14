# Conekta Inbound Message Triage

A lightweight AI-powered message triage system for property management and real estate inquiries.

The system accepts an inbound message, classifies it into one of four categories, assigns the corresponding operational queue, and independently flags urgent situations requiring rapid human attention.

## Problem

Conekta receives inbound messages from tenants, landlords, artisans and investors through channels such as WhatsApp and email. Manual triage creates a bottleneck because one person must read each message, determine what it is about, decide where it should go, and identify urgent cases.

This prototype demonstrates how AI can automate the first stage of that triage process while keeping the routing rules explicit and testable.

## Solution

The workflow is:

```text
Inbound message
      |
      v
LLM classification
      |
      +----> Category
      |
      +----> Operational queue
      |
      +----> Urgency flag
      |
      v
Structured JSON result
```

The classifier returns structured JSON such as:

```json
{
  "category": "maintenance",
  "queue": "operations",
  "urgent": true,
  "reason": "Tenant reports active flooding caused by a burst pipe."
}
```

## Categories and Routing

| Category | Queue | Examples |
|---|---|---|
| `rent_finance` | `support` | Rent amounts, payments, invoices, balances, deposits |
| `maintenance` | `operations` | Repairs, plumbing, electrical, utilities, property damage |
| `listing` | `support` | Listings, availability, viewings, property details |
| `investment` | `partnerships` | Investment opportunities, investors, partnerships |

Urgency is evaluated independently of category.

Examples of urgent situations include flooding, fire, gas leaks, serious electrical hazards and security threats.

## Technology

- Python
- OpenAI API
- `gpt-5.4-mini`
- `python-dotenv`
- Git/GitHub

The prototype intentionally uses a small Python implementation rather than introducing unnecessary infrastructure. The task is to demonstrate the triage logic, prompt design, testing approach and awareness of failure modes.

## Project Structure

```text
conekta-message-triage/
├── README.md
├── classifier.py
├── evaluate.py
├── test_api.py
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   └── sample_messages.json
└── docs/
    ├── prompt-notes.md
    └── evidence/
        ├── evaluation-summary.png
        └── failure-fix.png
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/gregodprogrammer/conekta-message-triage.git
cd conekta-message-triage
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file:

```bash
cp .env.example .env
```

Then add your API key to `.env`.

Never commit the `.env` file or expose the API key.

## Run the Classifier

Start the interactive classifier:

```bash
python classifier.py
```

Enter an inbound message when prompted.

Example:

```text
The kitchen pipe has burst and water is flooding the apartment.
```

The classifier returns structured JSON containing the category, queue, urgency flag and a short reason.

## Evaluation

The prototype was evaluated against 20 synthetic messages covering:

- Rent and finance requests
- Maintenance requests
- Urgent maintenance incidents
- Listing requests
- Investment requests
- Short WhatsApp-style messages
- Poorly formatted messages
- A multi-intent message
- An ambiguous classification case

No real company or personal data was used.

The initial evaluation produced:

| Metric | Result |
|---|---:|
| Total messages | 20 |
| Category accuracy | 95.0% |
| Queue accuracy | 100.0% |
| Urgency accuracy | 100.0% |
| End-to-end accuracy | 95.0% |

Evaluation evidence is available in:

`docs/evidence/evaluation-summary.png`

## Observed Failure and Prompt Refinement

One classification failure was observed during the initial evaluation.

### Failed Case

**Message:**

> How much is the monthly rent for the three bedroom flat?

**Expected:**

`rent_finance / support / urgent=false`

**Initial prediction:**

`listing / support / urgent=false`

### Why It Happened

The original `listing` definition included "pricing inquiries". This created an ambiguity between property listing information and questions specifically about monthly rent.

### Change Made

The prompt was refined so that:

- Monthly rent amounts are explicitly included under `rent_finance`.
- Questions specifically asking for the monthly rent amount are explicitly excluded from `listing`.

### Targeted Retest

The failed message was tested again after the prompt refinement and was correctly classified as:

`rent_finance / support / urgent=false`

Evidence:

`docs/evidence/failure-fix.png`

The full 20-message evaluation was not rerun after the prompt change because the purpose of the retest was specifically to verify the observed failure correction without unnecessarily consuming API credits.

## Failure Modes and Limitations

### 1. Ambiguous Intent

A message may contain language that overlaps categories. For example, property pricing can refer either to listing information or monthly rent.

**Mitigation:** make category boundaries explicit in the system prompt and add boundary-focused test cases.

### 2. Multi-Intent Messages

A message can contain more than one request, such as a maintenance problem and a rent question.

The current prototype assigns one primary category. A production system could support multiple intents or create separate tasks for each request.

**Next change:** support multiple intents or split multi-intent messages into separate operational tasks.

### 3. Urgency Interpretation

The model may not recognize every possible emergency or may incorrectly flag unusual wording.

A production implementation should combine model classification with explicit emergency rules and human escalation.

**Next change:** add deterministic emergency rules alongside the LLM and route uncertain cases for human review.

### 4. Queue Assumptions

The queue mappings in this prototype are based on the task specification. A production deployment would require confirmation of Conekta's actual operational teams, escalation paths and service-level expectations.

**Next change:** validate queue ownership and escalation rules with the operations team before production deployment.

## Prompt Design

The exact final system prompt and the reasoning behind the prompt design are documented in:

`docs/prompt-notes.md`

The prompt uses:

- Explicit category definitions
- Fixed queue mappings
- Independent urgency assessment
- Structured JSON output
- Clear category boundaries
- Instructions not to invent information

## AI and Tool Disclosure

AI and online resources were permitted for this assessment.

The following tools were used:

- **ChatGPT:** used for problem decomposition, prompt refinement, documentation review and development guidance.
- **OpenAI API:** used to classify the synthetic inbound messages.
- **Python:** used to implement the classifier and evaluation script.
- **Git/GitHub:** used for version control and repository delivery.

No real company or personal data was used.

## Design Approach

The implementation was intentionally kept small and focused on the core problem:

1. Define the classification taxonomy.
2. Map each category to a queue.
3. Separate urgency from category.
4. Require structured output.
5. Create synthetic test data.
6. Measure classification performance.
7. Investigate an observed failure.
8. Refine the prompt.
9. Perform a targeted retest.

This approach prioritizes testability and clear reasoning over unnecessary infrastructure.

## Future Improvements

If this prototype were developed further, the next improvements would be:

- Add more boundary-focused test cases.
- Add confidence or uncertainty handling.
- Support multiple intents in a single message.
- Add deterministic emergency rules alongside the LLM.
- Connect the classifier to an actual email or WhatsApp intake channel.
- Route classified messages into real operational queues.
- Add logging and monitoring for production evaluation.

## Assessment Summary

This prototype demonstrates a complete AI-assisted inbound triage workflow from message intake through classification, routing and urgency detection.

The implementation was tested using 20 synthetic messages and achieved:

- **95.0% category accuracy**
- **100.0% queue accuracy**
- **100.0% urgency accuracy**
- **95.0% end-to-end accuracy**

The evaluation also demonstrated an iterative development process: an actual classification failure was identified, the prompt was refined to address the ambiguity, and the failed case was retested successfully.

The main production considerations are ambiguity, multi-intent messages, urgency detection and validation of real operational routing rules.
