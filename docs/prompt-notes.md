# Prompt Notes

## Purpose

The prompt instructs the LLM to classify inbound property-management and
real-estate messages into one of four operational categories, assign the
corresponding queue, and independently identify urgent situations.

## Final System Prompt

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

## Prompt Design Decisions

### 1. Fixed categories

Four categories were selected to match the task requirements while keeping
the classification problem small enough to evaluate consistently.

### 2. Explicit queue mapping

Each category has one predefined queue. This prevents the model from
inventing operational destinations.

### 3. Independent urgency detection

Urgency is evaluated separately from category. For example, a maintenance
message can be urgent when it reports flooding or a gas leak, while another
maintenance request can be routine.

### 4. Boundary clarification

The initial evaluation produced one classification failure:

- Message: "How much is the monthly rent for the three bedroom flat?"
- Expected: rent_finance
- Predicted: listing

The original listing definition included "pricing inquiries", creating
an ambiguity between listing-related property information and rent/finance
questions.

The prompt was refined to explicitly include monthly rent amounts under
rent_finance and explicitly exclude monthly-rent questions from listing.

A targeted retest then correctly classified the message as:

- Category: rent_finance
- Queue: support
- Urgent: false

## Output Format

The model is instructed to return JSON so that the Python application can
parse the classification programmatically rather than relying on
free-form text.

## Model

The implementation uses the OpenAI API with the `gpt-5.4-mini` model.

## Evaluation Approach

The classifier was evaluated against 20 synthetic messages. The evaluation
measured category accuracy, queue accuracy, urgency accuracy, and
end-to-end accuracy.

Initial evaluation:

- Category accuracy: 95.0%
- Queue accuracy: 100.0%
- Urgency accuracy: 100.0%
- End-to-end accuracy: 95.0%

The observed category failure was investigated and addressed through prompt
refinement. A targeted retest of the failed case passed after the change.

## Evidence

- `docs/evidence/evaluation-summary.png` — initial 20-message evaluation
- `docs/evidence/failure-fix.png` — targeted retest after prompt refinement
