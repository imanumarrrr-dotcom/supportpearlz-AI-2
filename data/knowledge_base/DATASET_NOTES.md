# Dataset design notes

This is a fictional teaching dataset authored for the SupportPearlz assignment. It contains internally consistent product, policy, troubleshooting, pricing, privacy and service information. The current plain-text/CSV word count at generation time was **9,990 words** (computed across Markdown, text and CSV files; this count is an approximate corpus check, not a page count). Re-run the command below after edits to get the current count.

## Deliberate cross-document seams
1. A leaking unit with cabinet damage requires warranty exclusions plus the service claim process; neither document alone answers the full question.
2. An unusual taste after a cartridge change requires the product manual's flushing procedure plus the installation guide's escalation boundary.
3. Firmware 2.4's E-05 display behaviour is only documented in the changelog; the product manual deliberately does not define that code.
4. Return shipping responsibility and delivery damage require the return policy plus shipping evidence handling.

## Deliberate knowledge gaps
- Student discounts are not specified.
- Instalment payments are not specified.
- NSF certification is not specified.
- A universal installation fee is not specified.
- International shipping availability is not specified.
- Undefined alert codes E-01, E-02, E-04, E-06, E-07 and E-08 are not defined.

These gaps must remain gaps: evaluation should expect refusal or a request for human verification rather than invented facts.
