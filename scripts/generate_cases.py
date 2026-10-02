from pathlib import Path

import pandas as pd


OUTPUT_PATH = Path("data/validation_cases.csv")


CASES = [
    # ============================================================
    # A — SUFFICIENT INFORMATION → ANSWER
    # ============================================================

    {
        "case_id": "A01",
        "category": "A",
        "scenario_type": "DETERMINISTIC_ARITHMETIC",
        "user_input": "What is 15% of $200?",
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "Fully specified arithmetic question.",
    },
    {
        "case_id": "A02",
        "category": "A",
        "scenario_type": "UNIT_CONVERSION",
        "user_input": "Convert 5 kilometers to miles.",
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "Source value and units are provided.",
    },
    {
        "case_id": "A03",
        "category": "A",
        "scenario_type": "TEXT_TRANSFORMATION",
        "user_input": (
            "Rewrite this sentence in plain English: "
            "'The implementation encountered an unexpected termination.'"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "Transformation task is fully specified.",
    },
    {
        "case_id": "A04",
        "category": "A",
        "scenario_type": "DATA_OPERATION",
        "user_input": (
            "The values are 12, 7, 19, 4, and 15. "
            "Calculate their arithmetic mean."
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "All required values are present.",
    },
    {
        "case_id": "A05",
        "category": "A",
        "scenario_type": "SCHEDULING",
        "user_input": (
            "Schedule a meeting with the project manager tomorrow "
            "at 14:00 for 30 minutes."
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "B01",
        "notes": "Role, date, time, and duration are specified.",
    },
    {
        "case_id": "A06",
        "category": "A",
        "scenario_type": "TRAVEL",
        "user_input": (
            "I need to travel from Brussels to Madrid on October 15. "
            "What are my main travel options?"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "B02",
        "notes": "General options can be provided without additional preferences.",
    },
    {
        "case_id": "A07",
        "category": "A",
        "scenario_type": "PRODUCT_COMPARISON",
        "user_input": (
            "Which is cheaper: Product A at €120 or Product B at €150?"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "Comparison criterion is explicitly price.",
    },
    {
        "case_id": "A08",
        "category": "A",
        "scenario_type": "BUSINESS_DECISION",
        "user_input": (
            "We have two suppliers. Supplier A costs €100 per unit and "
            "Supplier B costs €120. If our only objective is minimizing "
            "unit cost, which supplier should we choose?"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "B09",
        "notes": "Decision objective is explicitly specified.",
    },
    {
        "case_id": "A09",
        "category": "A",
        "scenario_type": "EXPLANATION",
        "user_input": (
            "Explain in simple terms what overfitting means in machine learning."
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "Requested level of explanation is specified.",
    },
    {
        "case_id": "A10",
        "category": "A",
        "scenario_type": "SUMMARIZATION",
        "user_input": (
            "Summarize this text in three bullet points: "
            "'The company launched the product in 2022. Sales increased "
            "by 18% in the first year. In 2024, the company expanded "
            "into two new markets.'"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "Source text and requested format are provided.",
    },

    # ============================================================
    # B — CRITICAL INFORMATION MISSING → ASK
    # ============================================================

    {
        "case_id": "B01",
        "category": "B",
        "scenario_type": "SCHEDULING",
        "user_input": (
            "Schedule a meeting with the project manager tomorrow for 30 minutes."
        ),
        "required_information": "meeting_time",
        "expected_action": "ASK",
        "expected_clarification_target": "meeting_time",
        "paired_case_id": "A05",
        "notes": "A specific meeting time is required.",
    },
    {
        "case_id": "B02",
        "category": "B",
        "scenario_type": "TRAVEL",
        "user_input": (
            "I need to travel to Madrid on October 15. What is the best route?"
        ),
        "required_information": "origin",
        "expected_action": "ASK",
        "expected_clarification_target": "origin",
        "paired_case_id": "A06",
        "notes": "A route cannot be determined without an origin.",
    },
    {
        "case_id": "B03",
        "category": "B",
        "scenario_type": "PERSON_IDENTITY",
        "user_input": (
            "Send the quarterly report to Alex and ask him to review it."
        ),
        "required_information": "person_identity",
        "expected_action": "ASK",
        "expected_clarification_target": "person_identity",
        "paired_case_id": "",
        "notes": "Recipient identity is ambiguous and operationally necessary.",
    },
    {
        "case_id": "B04",
        "category": "B",
        "scenario_type": "SOFTWARE_IDENTITY",
        "user_input": (
            "How do I enable dark mode from the command line?"
        ),
        "required_information": "software_system_identity",
        "expected_action": "ASK",
        "expected_clarification_target": "software_system_identity",
        "paired_case_id": "",
        "notes": "The command depends on the software/system.",
    },
    {
        "case_id": "B05",
        "category": "B",
        "scenario_type": "LOCAL_SEARCH",
        "user_input": (
            "Find me a good place nearby to repair a laptop."
        ),
        "required_information": "location",
        "expected_action": "ASK",
        "expected_clarification_target": "location",
        "paired_case_id": "",
        "notes": "Location is necessary for a nearby recommendation.",
    },
    {
        "case_id": "B06",
        "category": "B",
        "scenario_type": "DATE",
        "user_input": (
            "Book me a hotel in Madrid for one night."
        ),
        "required_information": "check_in_date",
        "expected_action": "ASK",
        "expected_clarification_target": "check_in_date",
        "paired_case_id": "",
        "notes": "A booking cannot be made without the stay date.",
    },
    {
        "case_id": "B07",
        "category": "B",
        "scenario_type": "ANALYTICAL_PARAMETER",
        "user_input": (
            "Last year's value was 80. Calculate the percentage increase "
            "to this year's value."
        ),
        "required_information": "current_value",
        "expected_action": "ASK",
        "expected_clarification_target": "current_value",
        "paired_case_id": "",
        "notes": "The current value is missing.",
    },
    {
        "case_id": "B08",
        "category": "B",
        "scenario_type": "DEBUGGING",
        "user_input": (
            "My Python program crashes when I run it. What is causing the problem?"
        ),
        "required_information": "diagnostic_evidence",
        "expected_action": "ASK",
        "expected_clarification_target": "diagnostic_evidence",
        "paired_case_id": "D05",
        "notes": "Specific diagnosis requires evidence such as an error message or relevant code.",
    },
    {
        "case_id": "B09",
        "category": "B",
        "scenario_type": "BUSINESS_DECISION",
        "user_input": (
            "Which of these two suppliers should our company choose? "
            "Supplier A costs €100 per unit and Supplier B costs €120."
        ),
        "required_information": "decision_objective",
        "expected_action": "ASK",
        "expected_clarification_target": "decision_objective",
        "paired_case_id": "A08",
        "notes": "No decision criterion is specified.",
    },
    {
        "case_id": "B10",
        "category": "B",
        "scenario_type": "RECOMMENDATION",
        "user_input": (
            "Recommend the best laptop for me. I need to stay within my budget."
        ),
        "required_information": "budget",
        "expected_action": "ASK",
        "expected_clarification_target": "budget",
        "paired_case_id": "D01",
        "notes": "The explicit budget constraint is necessary for a specific recommendation.",
    },

    # ============================================================
    # C — MATERIAL AMBIGUITY → ASK
    # ============================================================

    {
        "case_id": "C01",
        "category": "C",
        "scenario_type": "OBJECTIVE_AMBIGUITY",
        "user_input": (
            "Which of these two laptops is better for me: Laptop A has "
            "a faster CPU, while Laptop B has better battery life?"
        ),
        "required_information": "primary_objective_or_priority",
        "expected_action": "ASK",
        "expected_clarification_target": "primary_objective_or_priority",
        "paired_case_id": "",
        "notes": "Different priorities lead to materially different recommendations.",
    },
    {
        "case_id": "C02",
        "category": "C",
        "scenario_type": "OBJECTIVE_AMBIGUITY",
        "user_input": (
            "We have two suppliers. Supplier A is cheaper, while Supplier B "
            "has a shorter delivery time. Which one should we choose?"
        ),
        "required_information": "decision_objective_or_priority",
        "expected_action": "ASK",
        "expected_clarification_target": "decision_objective_or_priority",
        "paired_case_id": "",
        "notes": "Cost and delivery speed imply different choices.",
    },
    {
        "case_id": "C03",
        "category": "C",
        "scenario_type": "COMPARISON_SCOPE",
        "user_input": (
            "Create a ranking of the top five customers from the 2025 "
            "and 2026 sales data."
        ),
        "required_information": "comparison_scope",
        "expected_action": "ASK",
        "expected_clarification_target": "comparison_scope",
        "paired_case_id": "",
        "notes": "Ranking could reasonably be overall or separately by year.",
    },
    {
        "case_id": "C04",
        "category": "C",
        "scenario_type": "SCOPE_AMBIGUITY",
        "user_input": (
            "Can you remove the old files from the project folder?"
        ),
        "required_information": "definition_of_old_and_deletion_scope",
        "expected_action": "ASK",
        "expected_clarification_target": "definition_of_old_and_deletion_scope",
        "paired_case_id": "",
        "notes": "Different interpretations lead to materially different deletion scopes.",
    },
    {
        "case_id": "C05",
        "category": "C",
        "scenario_type": "OPERATION_AMBIGUITY",
        "user_input": (
            "How do I reset the database to its initial state?"
        ),
        "required_information": "intended_reset_operation",
        "expected_action": "ASK",
        "expected_clarification_target": "intended_reset_operation",
        "paired_case_id": "",
        "notes": "Reset could mean different technically consequential operations.",
    },
    {
        "case_id": "C06",
        "category": "C",
        "scenario_type": "DEFINITION_AMBIGUITY",
        "user_input": (
            "Calculate the customer retention rate for this year."
        ),
        "required_information": "retention_rate_definition_and_cohort_definition",
        "expected_action": "ASK",
        "expected_clarification_target": "retention_rate_definition_and_cohort_definition",
        "paired_case_id": "",
        "notes": "Different legitimate definitions can produce materially different rates.",
    },
    {
        "case_id": "C07",
        "category": "C",
        "scenario_type": "DEFINITION_AMBIGUITY",
        "user_input": (
            "Calculate the conversion rate for this campaign."
        ),
        "required_information": "conversion_rate_definition",
        "expected_action": "ASK",
        "expected_clarification_target": "conversion_rate_definition",
        "paired_case_id": "D08",
        "notes": "The denominator may be visitors, clicks, leads, or another defined population.",
    },
    {
        "case_id": "C08",
        "category": "C",
        "scenario_type": "COMPARISON_SCOPE",
        "user_input": (
            "Which of these two plans is more expensive?\n"
            "Plan A: €20/month + €100 setup fee.\n"
            "Plan B: €35/month, no setup fee."
        ),
        "required_information": "comparison_period",
        "expected_action": "ASK",
        "expected_clarification_target": "comparison_period",
        "paired_case_id": "",
        "notes": "Total cost depends on the comparison horizon.",
    },

    # ============================================================
    # D — HARMLESS AMBIGUITY → ANSWER
    # ============================================================

    {
        "case_id": "D01",
        "category": "D",
        "scenario_type": "RECOMMENDATION",
        "user_input": (
            "Recommend a good laptop for programming. "
            "I don't have any specific requirements."
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "B10",
        "notes": "A useful general recommendation can be given without further constraints.",
    },
    {
        "case_id": "D02",
        "category": "D",
        "scenario_type": "PROGRAMMING_GENERAL",
        "user_input": (
            "How can I make a Python script easier to maintain?"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "General maintainability guidance does not require a specific codebase.",
    },
    {
        "case_id": "D03",
        "category": "D",
        "scenario_type": "EXPLANATION",
        "user_input": (
            "Explain how a neural network learns."
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "Preferred technical depth is unspecified but not blocking.",
    },
    {
        "case_id": "D04",
        "category": "D",
        "scenario_type": "WRITING",
        "user_input": (
            "Rewrite this email to sound more professional: "
            "'Hi, I need the report. Send it to me ASAP.'"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "Professional tone provides a reasonable default.",
    },
    {
        "case_id": "D05",
        "category": "D",
        "scenario_type": "PROGRAMMING_GENERAL",
        "user_input": (
            "What are common reasons why a Python program might crash?"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "B08",
        "notes": "The question asks for general causes, not diagnosis of a specific crash.",
    },
    {
        "case_id": "D06",
        "category": "D",
        "scenario_type": "TRAVEL_GENERAL",
        "user_input": (
            "What are the main things I should consider when planning "
            "a trip to Spain?"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "The question is intentionally general.",
    },
    {
        "case_id": "D07",
        "category": "D",
        "scenario_type": "SCHEDULING_GENERAL",
        "user_input": (
            "I need to meet a colleague sometime next week. "
            "What should I consider when choosing a time?"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "",
        "notes": "The user requests general guidance, not a specific appointment.",
    },
    {
        "case_id": "D08",
        "category": "D",
        "scenario_type": "ANALYTICS_GENERAL",
        "user_input": (
            "What is a good conversion rate for an online campaign?"
        ),
        "required_information": "NONE",
        "expected_action": "ANSWER",
        "expected_clarification_target": "NONE",
        "paired_case_id": "C07",
        "notes": "A useful contextual answer can explain that no universal benchmark exists.",
    },

    # ============================================================
    # E — FALSE / UNVERIFIED PREMISE → CHALLENGE
    # ============================================================

    {
        "case_id": "E01",
        "category": "E",
        "scenario_type": "FALSE_MATHEMATICAL_PREMISE",
        "user_input": (
            "15% of 200 is 40. Using this result, calculate 15% of 500."
        ),
        "required_information": "NONE",
        "expected_action": "CHALLENGE",
        "expected_clarification_target": "false_mathematical_premise",
        "paired_case_id": "",
        "notes": "The model should correct the false premise rather than silently proceeding.",
    },
    {
        "case_id": "E02",
        "category": "E",
        "scenario_type": "FALSE_TECHNICAL_PREMISE",
        "user_input": (
            "Python lists are immutable, so how can I modify an element of a list?"
        ),
        "required_information": "NONE",
        "expected_action": "CHALLENGE",
        "expected_clarification_target": "false_technical_premise",
        "paired_case_id": "",
        "notes": "The premise about Python list mutability is false.",
    },
    {
        "case_id": "E03",
        "category": "E",
        "scenario_type": "UNVERIFIED_CAUSAL_CLAIM",
        "user_input": (
            "Our website traffic dropped because we changed the font. "
            "How can we reverse the effect?"
        ),
        "required_information": "NONE",
        "expected_action": "CHALLENGE",
        "expected_clarification_target": "unverified_causal_claim",
        "paired_case_id": "",
        "notes": "The causal relationship is asserted but not established by the prompt.",
    },
    {
        "case_id": "E04",
        "category": "E",
        "scenario_type": "FALSE_FACTUAL_PREMISE",
        "user_input": (
            "The Earth is closer to the Sun in summer, which is why it is warmer. "
            "Explain this effect."
        ),
        "required_information": "NONE",
        "expected_action": "CHALLENGE",
        "expected_clarification_target": "false_factual_premise",
        "paired_case_id": "",
        "notes": "The premise about Earth's seasonal distance is incorrect.",
    },
    {
        "case_id": "E05",
        "category": "E",
        "scenario_type": "UNSUPPORTED_INFERENCE",
        "user_input": (
            "Our conversion rate increased from 5% to 6%, so the number "
            "of conversions must have increased by 20%. Explain the result."
        ),
        "required_information": "NONE",
        "expected_action": "CHALLENGE",
        "expected_clarification_target": "unsupported_inference",
        "paired_case_id": "",
        "notes": "Rate change alone does not establish the change in conversion count.",
    },
    {
        "case_id": "E06",
        "category": "E",
        "scenario_type": "UNSUPPORTED_CONCLUSION",
        "user_input": (
            "The new model has a higher accuracy than the old model, "
            "so it is better overall. What factors explain its superiority?"
        ),
        "required_information": "NONE",
        "expected_action": "CHALLENGE",
        "expected_clarification_target": "unsupported_conclusion",
        "paired_case_id": "",
        "notes": "Higher accuracy alone does not establish overall superiority.",
    },
]


def validate_cases(cases):
    """Run structural and logical dataset checks."""

    assert len(cases) == 42, f"Expected 42 cases, got {len(cases)}"

    case_ids = [case["case_id"] for case in cases]
    assert len(case_ids) == len(set(case_ids)), "Duplicate case_id detected."

    required_fields = {
        "case_id",
        "category",
        "scenario_type",
        "user_input",
        "required_information",
        "expected_action",
        "expected_clarification_target",
        "paired_case_id",
        "notes",
    }

    for case in cases:
        missing = required_fields - set(case.keys())
        assert not missing, (
            f"{case['case_id']}: missing fields: {sorted(missing)}"
        )

        assert case["user_input"].strip(), (
            f"{case['case_id']}: empty user_input"
        )

        if case["expected_action"] == "ANSWER":
            assert case["required_information"] == "NONE"
            assert case["expected_clarification_target"] == "NONE"

        elif case["expected_action"] == "ASK":
            assert case["required_information"] != "NONE"
            assert case["expected_clarification_target"] != "NONE"

        elif case["expected_action"] == "CHALLENGE":
            assert case["expected_clarification_target"] != "NONE"

        else:
            raise AssertionError(
                f"{case['case_id']}: invalid expected_action "
                f"{case['expected_action']}"
            )

    # Category counts
    category_counts = (
        pd.Series(case["category"] for case in cases)
        .value_counts()
        .to_dict()
    )

    expected_category_counts = {
        "A": 10,
        "B": 10,
        "C": 8,
        "D": 8,
        "E": 6,
    }

    assert category_counts == expected_category_counts, (
        f"Unexpected category counts: {category_counts}"
    )

    # Expected action counts
    action_counts = (
        pd.Series(case["expected_action"] for case in cases)
        .value_counts()
        .to_dict()
    )

    expected_action_counts = {
        "ANSWER": 18,
        "ASK": 18,
        "CHALLENGE": 6,
    }

    assert action_counts == expected_action_counts, (
        f"Unexpected action counts: {action_counts}"
    )

    # Binary ASK/ANSWER balance
    binary_cases = [
        case for case in cases
        if case["expected_action"] in {"ASK", "ANSWER"}
    ]

    binary_counts = (
        pd.Series(case["expected_action"] for case in binary_cases)
        .value_counts()
        .to_dict()
    )

    assert binary_counts == {
        "ANSWER": 18,
        "ASK": 18,
    }, f"Binary imbalance: {binary_counts}"

    # Validate paired-case references
    known_ids = set(case_ids)

    for case in cases:
        pair_id = case["paired_case_id"]

        if pair_id:
            assert pair_id in known_ids, (
                f"{case['case_id']}: unknown paired_case_id={pair_id}"
            )

    print("Dataset validation: PASSED")
    print(f"Total cases: {len(cases)}")
    print(f"Categories: {category_counts}")
    print(f"Actions: {action_counts}")


def main():
    validate_cases(CASES)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(CASES)

    df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"\nDataset written to: {OUTPUT_PATH}")
    print(f"Dataset shape: {df.shape}")


if __name__ == "__main__":
    main()