# The Builder’s Implementation Checklist

## Phase 1: Workflow Automation (The 60% Rule)

- [ ] **Identify the target:** Pick one high-friction, repeatable internal process (e.g., weekly reporting, support ticket triage, or outbound email prep).
- [ ] **Draw the line:** Map the exact point where "data processing" ends and "human judgment" begins.
- [ ] **Automate the first half:** Deploy a script/prompt chain to handle *only* the first 60% of the task.
- [ ] **Standardize the handoff:** Create a clean UI or dashboard where the human operator reviews the AI's draft, edits it, and hits "Approve/Send."

## Phase 2: Feedback & Iteration Moats

- [ ] **Install micro-feedback UI:** Add a simple mechanism (thumbs up/down, "Was this helpful?") to one core AI feature.
- [ ] **Capture the "Why":** Add an optional open-text field ("What was missing?") immediately after a negative rating.
- [ ] **Centralize the logs:** Pipe all feedback data directly into a dedicated Slack channel or a central tracking sheet.
- [ ] **Establish the ritual:** Schedule a mandatory 30-minute weekly block for the product team to review logs and adjust system prompts.

## Phase 3: Cost & Latency Routing

- [ ] **Audit current API calls:** List every LLM touchpoint in your application.
- [ ] **Down-tier the basics:** Swap the model for all routing, classification, and basic formatting tasks to a faster, cheaper tier (e.g., Gemini 1.5 Flash or Claude Haiku).
- [ ] **Protect the premium tier:** Restrict your most expensive, highest-latency models strictly to the final, user-facing reasoning or synthesis steps.

## Phase 4: Production Reliability

- [ ] **Enforce structured outputs:** Wrap critical generations in strict schema validation (e.g., JSON schemas) before passing the data downstream.
- [ ] **Install the safety net:** Deploy a lightweight banned-word or policy-violation filter *after* the generation step.
- [ ] **Define the fallback:** Write hardcoded, graceful error copy for users when the model times out or fails validation.
- [ ] **Build the escalation path:** Automatically route failed generations to a human admin queue rather than silently dropping them.

## Phase 5: The "Brief, Then Build" Prompt Migration

- [ ] **Identify the weakest output:** Pick the one feature where the AI rambles the most or loses the plot.
- [ ] **Split the prompt:** Break the single prompt into a two-step chain.  
  *Step 1 (Planner):* "Analyze this data and create a strict outline and success criteria."  
  *Step 2 (Executor):* "Follow this outline exactly to generate the final text."
