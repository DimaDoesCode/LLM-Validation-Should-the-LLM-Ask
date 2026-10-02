# LLM Validation — Should the LLM Ask a Question?

A compact black-box validation project for evaluating whether an LLM can correctly decide **when to answer, when to ask for clarification, and when to challenge a false or unsupported premise**.

The project focuses on a simple but important interaction boundary:

```text
User request
     ↓
Is the available information sufficient?
     │
     ├── YES → ANSWER
     │
     └── NO  → ASK
```

A third action is evaluated separately:

```text
False or unsupported premise
          ↓
      CHALLENGE
```

The goal is not to evaluate the quality of the final answer itself, but the **decision about what the LLM should do next**.

---

## Contents

* [Overview](#overview)
* [Validation Question](#validation-question)
* [Why This Matters](#why-this-matters)
* [Validation Framework](#validation-framework)
* [V1 — Action Selection](#v1--action-selection)
* [V1 Results](#v1-results)
* [V1 Failure Modes](#v1-failure-modes)
* [V2 — Clarification Quality](#v2--clarification-quality)
* [Model and Experimental Setup](#model-and-experimental-setup)
* [Repository Structure](#repository-structure)
* [Validation Reports](#validation-reports)
* [Literature](#literature)
* [Relation to Existing Research](#relation-to-existing-research)
* [Limitations](#limitations)
* [Status](#status)

---

## Overview

Large Language Models are usually evaluated on whether they can produce a good answer.

This project evaluates a different capability:

> **Does the model know whether it should answer at all?**

A useful assistant should not automatically generate an answer whenever a user provides a request.

Sometimes:

* the required information is already available → **ANSWER**
* a critical piece of information is missing → **ASK**
* the request contains a false or unsupported premise → **CHALLENGE**

The validation target is therefore the **action-selection boundary**, rather than answer generation.

---

## Validation Question

The central validation question is:

> **Can an LLM correctly determine whether the available information is sufficient to respond without clarification?**

This creates two symmetric failure modes:

### Premature Answer

The model should ask a question but answers anyway.

```text
Expected: ASK
Actual:   ANSWER
```

### Unnecessary Clarification

The model should answer directly but asks for information that is not necessary.

```text
Expected: ANSWER
Actual:   ASK
```

A third class is evaluated separately:

### False Premise Acceptance

The user provides a false, unsupported, or unjustified premise and the model accepts it instead of challenging it.

```text
Expected: CHALLENGE
Actual:   ANSWER
```

---

## Why This Matters

Clarification is not simply a conversational style choice.

Recent research increasingly treats clarification as a distinct capability involving ambiguity recognition, information needs, and interaction decisions.

For example, *Clarify When Necessary* studies how language models resolve ambiguity through interaction and explicitly addresses the question of **when clarification is warranted**. [[1]](#1-clarify-when-necessary--naacl-2025)

Other work shows that models can recognize ambiguity without necessarily expressing that uncertainty through a clarification question. [[5]](#5-knowing-but-not-showing--2026)

This distinction is important:

```text
Recognize ambiguity
        ↓
Decide whether clarification is necessary
        ↓
Ask the right question
        ↓
Use the new information
        ↓
Complete the task
```

This project initially focuses on the **second step**.

---

## Validation Framework

The validation framework is intentionally compact.

### Level 1 — Action Selection

The model must choose one of three actions:

| Action      | Meaning                                                                 |
| ----------- | ----------------------------------------------------------------------- |
| `ANSWER`    | Available information is sufficient                                     |
| `ASK`       | Essential information is missing or the request is materially ambiguous |
| `CHALLENGE` | The request contains a false or unsupported premise                     |

### Level 2 — Clarification Quality

If the model chooses `ASK`, a second question becomes relevant:

> **Did it ask for the right missing information?**

This separates two capabilities:

```text
LEVEL 1
Should I ask?
        ↓
LEVEL 2
What should I ask?
```

Recent clarification research makes a similar distinction between identifying information needs and generating useful clarification questions. [[2]](#2-clamber--acl-2024) [[3]](#3-learning-and-evaluating-factual-clarification-question-generation--2025) [[6]](#6-askbench--acl-findings-2026)

---

# V1 — Action Selection

V1 evaluates whether the model chooses the correct next action.

### Dataset

The validation set contains **42 synthetic cases**.

| Category  | Description                  |  Cases | Expected action |
| --------- | ---------------------------- | -----: | --------------- |
| A         | Sufficient Information       |     10 | `ANSWER`        |
| B         | Critical Information Missing |     10 | `ASK`           |
| C         | Material Ambiguity           |      8 | `ASK`           |
| D         | Harmless Ambiguity           |      8 | `ANSWER`        |
| E         | False / Unverified Premise   |      6 | `CHALLENGE`     |
| **Total** |                              | **42** |                 |

The dataset deliberately contains both positive and negative cases around the action boundary.

Controlled pairs are used where possible. For example:

```text
A05                         B01
Complete scheduling request  Missing meeting time
        ↓                           ↓
     ANSWER                       ASK
```

This makes it possible to test whether a small change in available information changes the expected action.

### V1 Prompt

The model receives only the user request and is instructed to return:

```json
{
    "action": "ANSWER | ASK | CHALLENGE",
    "reason": "brief explanation"
}
```

No case labels, expected actions, or validation metadata are exposed to the model.

---

# V1 Results

Model:

```text
Groq
openai/gpt-oss-120b
temperature = 0
```

### Overall

**33 / 42 correct — 78.6%**

| Category                         | Correct | Accuracy |
| -------------------------------- | ------: | -------: |
| A — Sufficient Information       |  9 / 10 |    90.0% |
| B — Critical Information Missing |  9 / 10 |    90.0% |
| C — Material Ambiguity           |   4 / 8 |    50.0% |
| D — Harmless Ambiguity           |   8 / 8 |   100.0% |
| E — False / Unverified Premise   |   3 / 6 |    50.0% |

For the main `ASK` / `ANSWER` boundary, excluding the separate premise-challenge cases:

**30 / 36 — 83.3%**

### Confusion Matrix

| Expected \ Actual | ANSWER | ASK | CHALLENGE |
| ----------------- | -----: | --: | --------: |
| ANSWER            |     17 |   1 |         0 |
| ASK               |      5 |  13 |         0 |
| CHALLENGE         |      3 |   0 |         3 |

The result shows a clear asymmetry: the model generally handles straightforward sufficient-information cases well, while **material ambiguity and unsupported premises are substantially harder**.

---

# V1 Failure Modes

The observed errors fall into several useful categories.

### 1. Execution-vs-Decision Confusion

In one scheduling case, the request contained enough information to formulate the scheduling action, but the model asked for additional operational details such as identity or calendar information.

This indicates a distinction between:

```text
"What information is required to answer?"
```

and:

```text
"What information would be required to actually execute the action?"
```

The validation target is the former.

---

### 2. Task Substitution

In one case, the model transformed an underspecified request into a related task it could answer immediately.

Instead of asking for the missing identity of a person, it effectively treated the request as a request to draft or prepare something.

This produces a useful failure pattern:

```text
User task
   ↓
Missing information
   ↓
Model substitutes easier task
   ↓
ANSWER
```

---

### 3. Helpful-Answer Substitution

Several `ASK` cases produced a useful generic answer instead of a clarification question.

For example, when a decision depended on an unstated objective, the model explained the trade-off rather than asking which objective mattered.

This is superficially helpful but fails the validation criterion.

The distinction is:

```text
"Here are the trade-offs."
```

versus:

```text
"Which objective should I optimize for?"
```

---

### 4. Ambiguity Blindness

Several materially ambiguous requests were answered directly.

This was especially visible in cases involving:

* deletion scope
* database reset semantics
* decision objectives
* comparison periods

The model often interpreted the request in a reasonable way instead of recognizing that **multiple materially different interpretations were possible**.

---

### 5. Unsupported Premise Acceptance

Three false or unsupported premises were accepted rather than challenged.

Examples included:

* an unsupported causal explanation
* an unjustified conversion-rate inference
* the assumption that higher accuracy automatically means a model is better overall

This indicates that the ability to distinguish:

```text
Given fact
     vs.
User interpretation
     vs.
Unsupported conclusion
```

is relevant to action selection.

---

## V2 — Clarification Quality

V2 extends the validation from:

> **Should the model ask?**

to:

> **If it asks, does it ask for the right information?**

The intended pipeline is:

```text
V1
Should I ASK?
      ↓
V2
What information is missing?
      ↓
Is the clarification relevant?
```

V2 is planned as a compact validation set of approximately **30–40 cases**.

The current design will examine:

1. Correct `ASK` + relevant clarification
2. Correct `ASK` + partial clarification
3. Correct `ASK` + irrelevant clarification
4. Premature `ANSWER`
5. Explicitly missing information
6. Implicit or materially missing information
7. Cases where several questions are possible but one critical target exists
8. Over-asking — requesting information that is unnecessary

A useful controlled pattern is:

```text
INSUFFICIENT INFORMATION
        ↓
       ASK
        ↓
ONE CRITICAL FACT ADDED
        ↓
SUFFICIENT INFORMATION
```

The exact V2 dataset will be frozen before implementation.

---

## Model and Experimental Setup

### Model

```text
Provider: Groq
Model:    openai/gpt-oss-120b
Mode:     black-box API
Temperature: 0
```

### Design principles

The experiments intentionally avoid:

* model weights
* hidden states
* fine-tuning
* internal reasoning access
* model-specific heuristics
* post-hoc decision correction

The model is evaluated through its externally observable behavior.

### Reproducibility

The validation scripts:

* use a fixed synthetic dataset
* use deterministic temperature settings
* store raw model responses
* store parsed actions
* store validation results
* support resumable execution
* stop cleanly on API rate limits

The goal is a small, reproducible experiment rather than a large benchmark.

---

## Repository Structure

```text
LLM-Validation-Should-the-LLM-Ask/
│
├── data/
│   └── validation_cases.csv
│
├── scripts/
│   ├── generate_cases.py
│   └── run_v1_action_selection.py
│
├── reports/
│   ├── V1_action_selection.md
│   └── v1_action_selection.csv
│
├── README.md
├── requirements.txt
└── .gitignore
```

The project deliberately avoids unnecessary framework layers.

---

## Validation Reports

### V1

* [V1 Action Selection Report](reports/V1_action_selection.md)
* [V1 Raw Results](reports/v1_action_selection.csv)

### V2

Planned:

* V2 Clarification Quality
* V2 raw evaluation results
* V2 analysis report

---

# Literature

The project is informed by recent research on ambiguity, clarification, information needs, and multi-turn interaction.

### [1] Clarify When Necessary — NAACL 2025

Michael J. Q. Zhang, Eunsol Choi.

**Clarify When Necessary: Resolving Ambiguity Through Interaction with LMs.**

[ACL Anthology](https://aclanthology.org/2025.findings-naacl.306/)

This work is particularly relevant to the distinction between ambiguity recognition and the decision to initiate clarification.

---

### [2] CLAMBER — ACL 2024

Tong Zhang et al.

**CLAMBER: A Benchmark of Identifying and Clarifying Ambiguous Information Needs in Large Language Models.**

[ACL Anthology](https://aclanthology.org/2024.acl-long.578/)

Relevant to the identification of ambiguous information needs and the generation of clarification behavior.

---

### [3] Clarification Question Generation — 2025

Matthew Toles, Yukun Huang, Zhou Yu.

**Learning and Evaluating Factual Clarification Question Generation Without Examples.**

[ACL Anthology](https://aclanthology.org/2025.gem-1.15/)

Relevant to the distinction between identifying what information is needed and generating a useful clarification question.

---

### [4] ClarifyMT-Bench — 2025

Sichun Luo et al.

**ClarifyMT-Bench: Benchmarking and Improving Multi-Turn Clarification for Conversational Large Language Models.**

[arXiv](https://arxiv.org/abs/2512.21120)

Relevant to multi-turn clarification and the subsequent use of information obtained from the user.

---

### [5] Knowing but Not Showing — 2026

Jinyan Su, Claire Cardie.

**Knowing but Not Showing: LLMs Recognize Ambiguity but Rarely Ask Clarifying Questions.**

[arXiv](https://arxiv.org/abs/2605.25284)

Particularly relevant to this project's central question: a model may recognize ambiguity internally or behaviorally without actually asking the user for clarification.

---

### [6] AskBench — ACL Findings 2026

Jiale Zhao, Ke Fang, Lu Cheng.

**When and What to Ask: AskBench and Rubric-Guided RLVR for LLM Clarification.**

[ACL Anthology](https://aclanthology.org/2026.findings-acl.845/)

Relevant to both dimensions evaluated in this project:

```text
WHEN to ask
    +
WHAT to ask
```

---

# Relation to Existing Research

Existing benchmarks and research provide broader evaluation frameworks for ambiguity detection, clarification generation, and multi-turn interaction. [[2]](#2-clamber--acl-2024) [[4]](#4-clarifymt-bench--2025) [[6]](#6-askbench--acl-findings-2026)

This project takes a narrower validation perspective.

Rather than attempting to build another large benchmark, it isolates a specific behavioral boundary:

```text
             User request
                  │
                  ▼
       Is information sufficient?
             /           \
           YES            NO
            │              │
            ▼              ▼
         ANSWER           ASK
                           │
                           ▼
                 What should be asked?
```

This allows individual failure modes to be inspected directly.

The project therefore complements broader benchmarks rather than attempting to replace them.

---

# Limitations

The current validation has several limitations.

### Synthetic Dataset

The 42 V1 cases are manually designed synthetic scenarios.

They provide controlled experimental conditions but do not represent the full distribution of real-world user requests.

### Single Model

V1 evaluates one model:

```text
openai/gpt-oss-120b
```

The results should therefore not be generalized to LLMs as a whole.

### Black-Box Evaluation

Only observable model behavior is evaluated.

The experiment cannot determine whether a failure is caused by:

* failure to recognize ambiguity
* incorrect prioritization
* instruction-following behavior
* response-generation tendencies
* another internal mechanism

### Human Judgment in Dataset Design

The expected actions are defined by the validation dataset.

Some real-world cases can legitimately admit multiple interpretations, particularly around the boundary between harmless and material ambiguity.

### No End-to-End Task Execution

V1 evaluates the action decision itself.

It does not verify whether an `ANSWER` would ultimately solve the user's problem or whether an `ASK` would lead to successful task completion.

That distinction is intentionally left for later validation stages.

---

# Status

### Completed

* [x] Validation concept
* [x] V1 validation matrix
* [x] Synthetic dataset
* [x] Dataset audit
* [x] Groq runner
* [x] Resumable execution
* [x] V1 evaluation
* [x] V1 failure-mode analysis
* [x] Initial literature review

### Current

* [ ] V2 validation matrix
* [ ] V2 dataset
* [ ] V2 runner
* [ ] V2 analysis

### Planned

The broader validation path is currently:

```text
V1 — Action Selection
      ↓
Should the LLM ask?

V2 — Clarification Quality
      ↓
Does it ask for the right information?

V3 — Information Update
      ↓
Does the model correctly use the information provided?

V4 — Clarification Efficiency
      ↓
Does it obtain the necessary information
without unnecessary questioning?
```

The exact scope of subsequent stages will be determined from the observed validation results rather than fixed in advance.
