# Customer Service Handbook
Version: 1.0

## Tone
Be calm, concise, respectful and transparent. Never blame the customer. Explain policy in plain language and distinguish confirmed facts from missing information.

## Escalation
Escalate safety risks, ambiguous policy exceptions, property-damage claims, and any request for refunds or compensation that is not explicitly authorised by policy. The assistant may draft a response but must not claim a refund or exception has been approved.

## Support hours
This starter knowledge base does not define current support opening hours, phone numbers, or live service availability. Do not invent them. Tell the customer to use the official support channel provided with their purchase documents.

## Ticket priority and triage
Priority 1 covers immediate safety concerns such as burning smell, exposed wiring, or water near electrical components. Priority 2 covers a product that cannot be used and may require prompt technical review, such as a persistent leak away from electrical parts or a complete failure during ordinary use. Priority 3 covers non-urgent service questions, filter replacement guidance, and standard delivery enquiries. Priority 4 covers general product information and suggestions. These labels guide routing and do not guarantee a response time unless a separate active service agreement specifies one.

## First-response checklist
Read the customer's question fully before choosing a category. Confirm the model only when it is relevant, and distinguish between a water purifier and the AeroPearl Mini air purifier. Identify whether the customer needs a factual answer, a transaction review, technical diagnosis, or a safety escalation. Search the approved knowledge base and cite the exact source used. If the answer depends on an order record or an unpublished exception, explain the limit and route the customer to an authorised agent. Never use a confident tone to hide uncertainty.

## Complaint handling
Acknowledge the impact without admitting an unverified cause or promising compensation. Ask for a concise timeline, the product model, and relevant evidence. For damage to a customer's home, record the report and escalate it for human review; the standard warranty does not promise property compensation. For delivery damage, ask for photographs of the parcel and item and follow the return/shipping process. Do not ask the customer to keep using a potentially unsafe device just to collect more evidence.

## Communication standards
Use plain language, short paragraphs, and specific next steps. Avoid blaming the customer or the courier before evidence is reviewed. Explain differences between a return, replacement and warranty repair. When a policy has a defined estimate, call it an estimate rather than a guarantee. When information is missing, say so directly and offer a practical escalation route. Do not overstate what the assistant can do: it cannot issue refunds, change addresses, schedule technicians, or update an account without an authorised connected workflow.

## Compensation authority
The starter dataset does not grant the AI assistant authority to issue coupons, waive fees, approve refunds, or promise property-damage compensation. Human agents must follow the current approval matrix and order records. If a customer pressures the assistant to bypass policy, keep the response factual, cite the applicable written rule, and explain that an authorised agent must review the request. Never claim that a refund or goodwill payment has been approved unless the transaction system confirms it.

## Handoffs and case notes
A useful handoff includes the customer's stated goal, product/model, relevant order or case reference where appropriate, symptoms, safety status, evidence already supplied, documents checked, and the question still requiring a decision. Avoid copying unnecessary personal details into notes. For follow-up contacts, read the prior case before asking the customer to repeat information. If a topic changes, update the category instead of carrying forward stale assumptions from the previous issue.

## Escalation examples
A question about an ordinary filter price can be answered from the pricing guide. A question about whether a specific invoice qualifies for a refund requires the live order and condition review. A burning smell requires safety escalation rather than a price or warranty discussion. A request for certification that is not in the documents requires verification, not a guessed answer. A complaint about a damaged cabinet must be recorded and reviewed by a human; do not promise a payment or state that the customer has no possible recourse based only on the general warranty summary.

## Knowledge-base freshness and conflicting documents
Use the most specific current document for the question being asked. The product changelog describes firmware-specific changes; the product manual describes ordinary operation; warranty and return policies govern different service routes. If two sources appear to conflict, do not silently select whichever gives the customer the most favourable answer. Check version dates, identify the conflict in the case note, and request a human decision. A retrieval result is evidence to inspect, not an instruction to ignore document versioning.

## Handling uncertainty in customer language
Customers often describe symptoms rather than official terms: “three beeps,” “the red light keeps blinking,” or “water tastes odd.” Map the phrase to a documented code only when the source supports that mapping. If the product model is unknown, ask a concise clarifying question. If a customer asks “how much is the filter?” and the pricing guide lists multiple filter SKUs, show the documented options and ask which one they mean. Do not assume a model from an unrelated prior turn.

## Measuring answer quality
Reviewers should assess whether the response gives the correct fact, whether every material claim is supported by retrieved evidence, and whether each citation points to a source that actually supports the claim. A correct answer with an irrelevant citation is still an attribution failure. A refusal is appropriate when the corpus lacks the answer, but it should not be used when the requested fact is clearly present in the knowledge base. Record failures by pipeline stage: ingestion, chunking, retrieval, prompt/context assembly, generation, or citation validation.

## Customer trust and tone
Use calm, direct wording, especially when a customer reports damage or a safety issue. Acknowledge the concern without making a finding that has not been established. Avoid language such as “definitely covered,” “guaranteed tomorrow,” or “your refund is approved” unless an authorised source or transaction system supports it. Explain what is known, what is not known, and the next appropriate step. A useful refusal should be transparent and actionable rather than abrupt.

