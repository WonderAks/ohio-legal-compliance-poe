from tools.ohio_statute_tool import OhioStatuteTool


tool = OhioStatuteTool()

clause = """
Buyer accepted all goods but failed to make
payment when payment became due.
""".lower()


print("=" * 70)
print("RAW KEYWORD SCORE DEBUG")
print("=" * 70)


for law in tool.laws:

    score = 0
    matches = []

    for keyword in law.get("keywords", []):

        keyword_lower = keyword.lower()

        if keyword_lower in clause:

            if keyword_lower in {
                "buyer",
                "seller",
                "goods",
                "payment",
                "written",
                "signed",
                "writing",
                "verbal",
                "oral",
                "accepted",
                "notice",
                "breach"
            }:
                weight = 0.5

            elif " " in keyword_lower:
                weight = 2.0

            else:
                weight = 1.0

            score += weight

            matches.append(
                f"{keyword} ({weight})"
            )


    print(
        f"\nSection: {law['section']}"
    )

    print(
        f"Raw Score: {score}"
    )

    print(
        f"Matches: {matches}"
    )