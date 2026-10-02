# V1 Action Selection

## Objective

V1 evaluates whether the LLM selects the appropriate next action for a user request:

* `ANSWER` — sufficient information is available;
* `ASK` — essential information is missing or the request is materially ambiguous;
* `CHALLENGE` — the request contains a false or unsupported premise.

Model:

* **Groq:** `openai/gpt-oss-120b`
* **Temperature:** `0`
* **Evaluation type:** black-box
* **Cases:** 42
* **Output:** structured JSON (`action`, `reason`)

---

## Overall Results

| Metric           |    Result |
| ---------------- | --------: |
| Total cases      |        42 |
| Correct          |        32 |
| Incorrect        |        10 |
| Overall Accuracy | **76.2%** |

The main `ANSWER` / `ASK` boundary contains 36 cases:

| Metric    |    Result |
| --------- | --------: |
| A–D cases |        36 |
| Correct   |        30 |
| Accuracy  | **83.3%** |

The 6 `CHALLENGE` cases are evaluated separately.

---

## Confusion Matrix

### All Actions

| Expected \ Actual | ANSWER | ASK | CHALLENGE |
| ----------------- | -----: | --: | --------: |
| **ANSWER**        |     17 |   1 |         0 |
| **ASK**           |      6 |  12 |         0 |
| **CHALLENGE**     |      3 |   0 |         3 |

### Interpretation

The main errors are:

* `ANSWER → ASK`: 1 case
* `ASK → ANSWER`: 6 cases
* `CHALLENGE → ANSWER`: 3 cases

There were no cases where the model confused `ANSWER` or `ASK` directly with `CHALLENGE`.

---

## Category-Level Results

| Category                         | Expected | Correct |   Accuracy |
| -------------------------------- | -------: | ------: | ---------: |
| A — Sufficient Information       |       10 |       9 |  **90.0%** |
| B — Critical Information Missing |       10 |       9 |  **90.0%** |
| C — Material Ambiguity           |        8 |       4 |  **50.0%** |
| D — Harmless Ambiguity           |        8 |       8 | **100.0%** |
| E — False / Unsupported Premise  |        6 |       2 |  **33.3%** |

The strongest performance was observed on clearly sufficient requests (A), clearly incomplete requests (B), and harmless ambiguity (D).

The largest degradation occurred on material ambiguity (C) and false/unsupported premises (E).

---

## Error Analysis

There were 10 incorrect cases.

### A05 — Unnecessary Clarification

**Expected:** `ANSWER`
**Actual:** `ASK`

> "Schedule a meeting with the project manager tomorrow at 14:00 for 30 minutes."

Model reason:

> "Need clarification on which project manager and calendar details to schedule the meeting"

The model requested information that may be needed for actual execution, but the requested action itself is sufficiently specified for the purpose of this test.

**Failure mode:** execution-vs-decision confusion.

---

### B03 — Premature Answer

**Expected:** `ASK`
**Actual:** `ANSWER`

> "Send the quarterly report to Alex and ask him to review it."

The model interpreted the task as a request for drafting assistance rather than identifying the missing person identity required to execute the request.

Model reason:

> "User requests assistance with sending a report; we can provide a draft email and guidance, which is a direct answer."

**Failure mode:** task substitution / premature answer.

---

### C02 — Material Objective Ambiguity

**Expected:** `ASK`
**Actual:** `ANSWER`

> "We have two suppliers. Supplier A is cheaper, while Supplier B has a shorter delivery time. Which one should we choose?"

The model recognized the trade-off but decided that general advice could be given without clarification.

The missing information is the decision objective or priority between cost and delivery time.

**Failure mode:** helpful-answer substitution.

---

### C04 — Material Scope Ambiguity

**Expected:** `ASK`
**Actual:** `ANSWER`

> "Can you remove the old files from the project folder?"

The model focused on providing safe deletion guidance instead of resolving what "old files" means.

**Failure mode:** helpful-answer substitution / scope blindness.

---

### C05 — Material Operation Ambiguity

**Expected:** `ASK`
**Actual:** `ANSWER`

> "How do I reset the database to its initial state?"

"Reset" can refer to materially different operations, such as clearing data, recreating the schema, or restoring an initial dataset.

The model treated the request as sufficiently specified for generic technical instructions.

**Failure mode:** operation ambiguity blindness.

---

### C08 — Comparison-Horizon Ambiguity

**Expected:** `ASK`
**Actual:** `ANSWER`

> "Which of these two plans is more expensive?"

The plans have different pricing structures:

* Plan A: €20/month + €100 setup fee
* Plan B: €35/month, no setup fee

The answer depends on the comparison period.

The model treated the supplied prices as sufficient for a direct comparison.

**Failure mode:** comparison-scope blindness.

---

### E03 — Unsupported Causal Claim

**Expected:** `CHALLENGE`
**Actual:** `ANSWER`

> "Our website traffic dropped because we changed the font. How can we reverse the effect?"

The model accepted the claimed causal relationship instead of distinguishing correlation from demonstrated causation.

**Failure mode:** unsupported causal-premise acceptance.

---

### E05 — Unsupported Inference

**Expected:** `CHALLENGE`
**Actual:** `ANSWER`

> "Our conversion rate increased from 5% to 6%, so the number of conversions must have increased by 20%."

The model accepted the inference even though conversion count cannot be determined from the conversion-rate change alone.

**Failure mode:** unsupported inference acceptance.

---

### E06 — Unsupported Conclusion

**Expected:** `CHALLENGE`
**Actual:** `ANSWER`

> "The new model has a higher accuracy than the old model, so it is better overall."

The model accepted the conclusion instead of noting that higher accuracy alone does not establish overall superiority.

**Failure mode:** unsupported conclusion acceptance.

---

## Key Findings

### 1. Explicit missing information is handled relatively well

Cases B achieved **90% accuracy**. The model usually recognized when an essential parameter was absent.

### 2. Material ambiguity is substantially harder

Cases C achieved only **50% accuracy**.

The model frequently preferred to provide useful generic advice instead of asking for the missing criterion, scope, or definition.

### 3. Harmless ambiguity did not cause excessive clarification

Cases D achieved **100% accuracy**.

This is important because the model did not simply adopt an "ask whenever anything is ambiguous" strategy.

### 4. Explicit false premises are easier than unsupported reasoning

Within E, the model correctly challenged the three explicit factual errors:

* incorrect percentage calculation;
* immutable Python lists;
* incorrect explanation of Earth's seasons.

However, it failed all three cases involving unsupported causal or logical conclusions.

This indicates a distinction between:

```text
Explicit factual contradiction
        ↓
       easier
```

and

```text
Unsupported inference / causal claim
        ↓
       harder
```

---

## Observed Failure Modes

V1 identified three recurring patterns:

### F1 — Execution-vs-Decision Confusion

The model asks for information needed to execute an action even when the requested action is already sufficiently specified for the validation task.

Observed in: **A05**

### F2 — Helpful-Answer Substitution

The model provides useful generic advice instead of asking for information required to resolve the user's actual request.

Observed in: **C02, C04, C05, C08**

### F3 — Explicit-False vs Unsupported-Premise Gap

The model challenges explicit false facts but often accepts causal or logical claims that are not supported by the information provided.

Observed in: **E03, E05, E06**

---

## Conclusion

V1 shows that `ANSWER` / `ASK` selection is not a single capability.

The model performs relatively well when information is either clearly sufficient or explicitly missing. Performance decreases when the missing information is implicit — such as a decision objective, comparison scope, operational meaning, or definition.

Premise handling shows a similar distinction: explicit factual errors are detected more reliably than unsupported causal or logical inferences.

The main validation signal for subsequent work is therefore not general question-answering ability, but the model's ability to detect **when the missing information materially changes the appropriate response**.
