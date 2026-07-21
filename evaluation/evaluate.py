import json
__version__ = "0.1.0"

import json
import re

from workflows.poe_workflow import OhioComplianceWorkflow


workflow = OhioComplianceWorkflow(
    name="Ohio Contract Compliance PoE"
)


def extract_statutes(text):
    """
    Extract Ohio statute section numbers such as:
    1302.04
    1335.05
    """
    statutes = re.findall(r"\b\d{4}\.\d{2}\b", text)

    # Remove duplicates while preserving order
    return list(dict.fromkeys(statutes))


def extract_compliance(text):
    """
    Extract compliance classification from agent output.
    """

    text_lower = text.lower()

    # Check Partially Compliant first because it contains
    # the word "Compliant"
    if "partially compliant" in text_lower:
        return "Partially Compliant"

    if "non-compliant" in text_lower or "non compliant" in text_lower:
        return "Non-Compliant"

    if "compliant" in text_lower:
        return "Compliant"

    return "Unknown"


with open(
    "evaluation/ohio_ground_truth.json",
    "r",
    encoding="utf-8"
) as file:
    ground_truth = json.load(file)


results = []

total_score = 0
maximum_score = len(ground_truth) * 100


print("=" * 70)
print("OHIO CONTRACT COMPLIANCE PoE - BASELINE EVALUATION")
print("=" * 70)

print(f"\nGround Truth Cases: {len(ground_truth)}")
print("Starting evaluation...\n")


for test in ground_truth:

    print("-" * 70)
    print(
        f"TEST {test['id']}: "
        f"{test['category']}"
    )
    print("-" * 70)

    try:
        result = workflow.run(
            clause=test["clause"]
        )

        predicted_statutes = extract_statutes(
            result["statutes"]
        )

        predicted_compliance = extract_compliance(
            result["compliance"]
        )

        expected_statutes = set(
            test["expected_statutes"]
        )

        predicted_statute_set = set(
            predicted_statutes
        )

        score = 0

        # ==================================================
        # STATUTE SCORE - 40 POINTS
        # ==================================================

        if predicted_statute_set == expected_statutes:

            statute_score = 40

        elif expected_statutes.intersection(
            predicted_statute_set
        ):

            matched = len(
                expected_statutes.intersection(
                    predicted_statute_set
                )
            )

            statute_score = (
                matched / len(expected_statutes)
            ) * 40

        else:

            statute_score = 0


        score += statute_score


        # ==================================================
        # COMPLIANCE SCORE - 40 POINTS
        # ==================================================

        if (
            predicted_compliance
            == test["expected_compliance"]
        ):

            compliance_score = 40

        else:

            compliance_score = 0


        score += compliance_score


        # ==================================================
        # LEGAL KEYWORD SCORE - 20 POINTS
        # ==================================================

        combined_output = (
            result["statutes"]
            + " "
            + result["compliance"]
            + " "
            + result["recommendation"]
        ).lower()


        keyword_matches = []

        for keyword in test["expected_keywords"]:

            if keyword.lower() in combined_output:

                keyword_matches.append(keyword)


        keyword_score = (
            len(keyword_matches)
            / len(test["expected_keywords"])
        ) * 20


        score += keyword_score

        total_score += score


        # ==================================================
        # DISPLAY RESULT
        # ==================================================

        print(
            f"Expected Statutes  : "
            f"{test['expected_statutes']}"
        )

        print(
            f"Predicted Statutes : "
            f"{predicted_statutes}"
        )

        print(
            f"Expected Compliance  : "
            f"{test['expected_compliance']}"
        )

        print(
            f"Predicted Compliance : "
            f"{predicted_compliance}"
        )

        print(
            f"Keyword Matches : "
            f"{keyword_matches}"
        )


        print("\nSCORE BREAKDOWN")

        print(
            f"Statute Match    : "
            f"{statute_score:.2f}/40"
        )

        print(
            f"Compliance Match : "
            f"{compliance_score:.2f}/40"
        )

        print(
            f"Legal Concepts   : "
            f"{keyword_score:.2f}/20"
        )

        print(
            f"\nTEST ACCURACY    : "
            f"{score:.2f}%"
        )


        results.append(
            {
                "id": test["id"],
                "category": test["category"],
                "expected_statutes": (
                    test["expected_statutes"]
                ),
                "predicted_statutes": (
                    predicted_statutes
                ),
                "expected_compliance": (
                    test["expected_compliance"]
                ),
                "predicted_compliance": (
                    predicted_compliance
                ),
                "keyword_matches": (
                    keyword_matches
                ),
                "statute_score": round(
                    statute_score,
                    2
                ),
                "compliance_score": round(
                    compliance_score,
                    2
                ),
                "keyword_score": round(
                    keyword_score,
                    2
                ),
                "accuracy": round(
                    score,
                    2
                )
            }
        )


    except Exception as error:

        print("[ERROR] Test failed.")

        print(
            f"Error Type : "
            f"{type(error).__name__}"
        )

        print(
            f"Error      : "
            f"{error}"
        )


        results.append(
            {
                "id": test["id"],
                "category": test["category"],
                "error": str(error),
                "accuracy": 0
            }
        )


print("\n")
print("=" * 70)
print("FINAL BASELINE EVALUATION")
print("=" * 70)


overall_accuracy = (
    total_score / maximum_score
) * 100


print(
    f"\nTotal Test Cases : "
    f"{len(ground_truth)}"
)

print(
    f"Maximum Score    : "
    f"{maximum_score}"
)

print(
    f"Obtained Score   : "
    f"{total_score:.2f}"
)

print(
    f"\nOVERALL ACCURACY : "
    f"{overall_accuracy:.2f}%"
)


print("\n" + "=" * 70)


with open(
    "evaluation/results.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        results,
        file,
        indent=4
    )


print(
    "\nDetailed evaluation results saved to:"
)

print(
    "evaluation/results.json"
)