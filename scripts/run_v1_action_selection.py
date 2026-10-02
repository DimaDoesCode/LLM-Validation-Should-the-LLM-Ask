"""
LLM Validation — V1 Action Selection

Tests whether the LLM correctly chooses the appropriate next action
for a user request:

    ANSWER
    ASK
    CHALLENGE

V1 is resumable:
- saves results after every successful case;
- skips already completed cases;
- retries incomplete/error cases;
- stops cleanly on Groq rate limits.

Provider: Groq
Model: openai/gpt-oss-120b
Temperature: 0
"""

from pathlib import Path
import json

import pandas as pd
from groq import Groq


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "openai/gpt-oss-120b"
TEMPERATURE = 0

DATA_PATH = Path("data/validation_cases.csv")
OUTPUT_PATH = Path(
    "reports/v1_action_selection.csv"
)

VALID_ACTIONS = {
    "ANSWER",
    "ASK",
    "CHALLENGE",
}


# ============================================================
# CLIENT
# ============================================================

client = Groq()


# ============================================================
# PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are evaluating a user request.

Choose the appropriate next action:

- ANSWER — provide a useful answer now.
- ASK — ask a clarifying question because essential information
  is missing or the request is materially ambiguous.
- CHALLENGE — identify and address a false or unsupported premise
  before proceeding.

Return ONLY valid JSON with exactly these fields:

{
    "action": "ANSWER" or "ASK" or "CHALLENGE",
    "reason": "brief explanation of the decision"
}

Do not include markdown, code fences, or any additional text.

Do not assume information that is not present in the user's request.
Do not use hidden labels, case metadata, or external information.

User request:
"""


# ============================================================
# LLM CALL
# ============================================================

def evaluate_case(user_input):
    """
    Send one user request to the LLM and return the structured result.
    """

    prompt = SYSTEM_PROMPT + "\n" + user_input

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
    )

    content = response.choices[0].message.content

    result = json.loads(content)

    action = result.get("action")
    reason = result.get("reason")

    if action not in VALID_ACTIONS:
        raise ValueError(
            f"Invalid action returned by model: {action}"
        )

    if not isinstance(reason, str) or not reason.strip():
        raise ValueError(
            "Model returned an empty or invalid reason."
        )

    return action, reason, content


# ============================================================
# RATE LIMIT DETECTION
# ============================================================

def is_rate_limit_error(error):
    message = str(error)

    return (
        "429" in message
        or "rate_limit_exceeded" in message
        or "Rate limit reached" in message
    )


# ============================================================
# LOAD EXISTING RESULTS
# ============================================================

def load_existing_results():
    if not OUTPUT_PATH.exists():
        return pd.DataFrame()

    existing = pd.read_csv(OUTPUT_PATH)

    print()
    print("=" * 70)
    print("EXISTING RESULTS FOUND")
    print("=" * 70)
    print(f"File:                 {OUTPUT_PATH}")
    print(f"Rows in file:         {len(existing)}")

    required_columns = {
        "case_id",
        "actual_action",
        "reason",
        "raw_response",
    }

    missing = required_columns - set(existing.columns)

    if missing:
        print(
            "Existing file has incompatible structure. "
            "Starting from scratch."
        )
        return pd.DataFrame()

    completed_mask = (
        existing[
            [
                "actual_action",
                "reason",
                "raw_response",
            ]
        ]
        .notna()
        .all(axis=1)
    )

    completed_count = completed_mask.sum()

    print(f"Completed cases:      {completed_count}")
    print(
        f"Incomplete cases:     "
        f"{len(existing) - completed_count}"
    )

    return existing


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(existing, new_result):
    new_row = pd.DataFrame([new_result])

    combined = pd.concat(
        [existing, new_row],
        ignore_index=True,
    )

    # Keep the latest result for each case.
    combined = combined.drop_duplicates(
        subset=["case_id"],
        keep="last",
    )

    # Preserve dataset order.
    combined = combined.sort_values("case_id")

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    combined.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    return combined


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("LLM VALIDATION — V1 ACTION SELECTION")
    print("=" * 70)

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    print()
    print("[1] LOADING DATA")

    df = pd.read_csv(DATA_PATH)

    print(f"Dataset shape: {df.shape}")

    required_columns = {
        "case_id",
        "category",
        "scenario_type",
        "user_input",
        "expected_action",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    print("Required columns: OK")

    # --------------------------------------------------------
    # LOAD EXISTING RESULTS
    # --------------------------------------------------------

    existing = load_existing_results()

    if len(existing) > 0:

        completed_mask = (
            existing[
                [
                    "actual_action",
                    "reason",
                    "raw_response",
                ]
            ]
            .notna()
            .all(axis=1)
        )

        completed_cases = set(
            existing.loc[
                completed_mask,
                "case_id",
            ]
        )

    else:
        completed_cases = set()

    total_cases = len(df)

    print()
    print("=" * 70)
    print("RESUME STATUS")
    print("=" * 70)
    print(f"Total cases:          {total_cases}")
    print(f"Already completed:    {len(completed_cases)}")
    print(
        f"Remaining:            "
        f"{total_cases - len(completed_cases)}"
    )

    if len(completed_cases) == total_cases:

        print()
        print("All cases are already completed.")
        print("Nothing to do.")
        return

    # --------------------------------------------------------
    # PROCESS CASES
    # --------------------------------------------------------

    for index, row in df.iterrows():

        case_id = row["case_id"]

        if case_id in completed_cases:
            continue

        print()
        print(
            f"Case {index + 1:02d}/{total_cases}: "
            f"{case_id} | {row['category']} | "
            f"{row['scenario_type']}"
        )

        result = {
            "case_id": case_id,
            "category": row["category"],
            "scenario_type": row["scenario_type"],
            "user_input": row["user_input"],
            "expected_action": row["expected_action"],

            "actual_action": None,
            "is_correct": None,

            "reason": None,
            "raw_response": None,

            "error": None,
        }

        try:

            actual_action, reason, raw_response = evaluate_case(
                row["user_input"]
            )

            result["actual_action"] = actual_action
            result["is_correct"] = (
                actual_action == row["expected_action"]
            )
            result["reason"] = reason
            result["raw_response"] = raw_response

            print(
                f"  Expected: {row['expected_action']}"
            )

            print(
                f"  Actual:   {actual_action}"
            )

            print(
                f"  Correct:  {result['is_correct']}"
            )

            print(
                f"  Reason:   {reason}"
            )

            # ------------------------------------------------
            # SAVE IMMEDIATELY
            # ------------------------------------------------

            existing = save_results(
                existing,
                result,
            )

            completed_cases.add(case_id)

            print(
                f"  Saved: {OUTPUT_PATH}"
            )

        except Exception as error:

            if is_rate_limit_error(error):

                print()
                print("=" * 70)
                print("GROQ RATE LIMIT REACHED")
                print("=" * 70)
                print()
                print(
                    "The rate limit or token quota "
                    "has been reached."
                )
                print(
                    "Stopping V1 now. Successfully completed "
                    "cases are already saved."
                )
                print()
                print(
                    "Run this same script again after "
                    "the quota resets."
                )

                break

            # ------------------------------------------------
            # OTHER ERRORS
            # ------------------------------------------------

            print(
                f"  ERROR: {error}"
            )

            # The case is intentionally NOT marked completed.
            # It will be retried on the next run.

            continue

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    if OUTPUT_PATH.exists():

        final_df = pd.read_csv(OUTPUT_PATH)

        completed_mask = (
            final_df[
                [
                    "actual_action",
                    "reason",
                    "raw_response",
                ]
            ]
            .notna()
            .all(axis=1)
        )

        completed_count = completed_mask.sum()

    else:
        completed_count = 0

    print()
    print("=" * 70)
    print("V1 STATUS")
    print("=" * 70)

    print(
        f"Completed: {completed_count}/{total_cases}"
    )

    print(
        f"Remaining: {total_cases - completed_count}"
    )

    if completed_count == total_cases:

        print()
        print(
            "V1 ACTION SELECTION COMPLETE"
        )

        print(
            f"Results saved to: {OUTPUT_PATH}"
        )

    else:

        print()
        print(
            "V1 is incomplete but all successful "
            "results have been preserved."
        )


if __name__ == "__main__":
    main()