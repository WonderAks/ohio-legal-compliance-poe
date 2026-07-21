import json
import re
from pathlib import Path


__version__ = "0.1.0-deterministic"


class OhioStatuteTool:
    def __init__(self):
        import json
        from pathlib import Path
        from typing import List


        class OhioStatuteTool:
            """A deterministic, baseline statute retrieval tool.

            This baseline checks each statute's keywords and returns statutes when
            any keyword appears in the clause. It is intentionally simple and
            deterministic so it can be committed separately from the weighted
            retrieval improvement.
            """

            def __init__(self, data_path: str = None):
                if data_path is None:
                    data_path = Path(__file__).parent.parent / "data" / "sample_ohio_laws.json"
                else:
                    data_path = Path(data_path)

                with open(data_path, "r", encoding="utf-8") as fh:
                    self.laws = json.load(fh)

            def search_statutes(self, clause: str) -> str:
                clause_lower = clause.lower()
                matches: List[dict] = []

                for law in self.laws:
                    keywords = law.get("keywords", [])
                    for kw in keywords:
                        if kw and kw.lower() in clause_lower:
                            matches.append(law)
                            break

                if not matches:
                    return "No relevant Ohio statutes found."

                out_lines = []
                for law in matches:
                    out_lines.append(f"Section: {law.get('section')}")
                    out_lines.append(f"Title: {law.get('title')}")
                    out_lines.append(f"Summary: {law.get('summary')}\n")

                return "\n".join(out_lines)
            "buyer",
            "seller",
            "goods",
            "written",
            "signed",
            "writing",
            "verbal",
            "oral"
        }


        # ---------------------------------------
        # MATERIAL LEGAL CONCEPTS
        # ---------------------------------------

        material_keywords = {
            "accepted",
            "acceptance",
            "payment",
            "notice",
            "breach",
            "quantity",
            "delivery",
            "modification",
            "waiver",
            "rescission",
            "confirmation",
            "repudiates",
            "damages"
        }


        for law in self.laws:

            score = 0
            matched_keywords = []

            keywords = law.get(
                "keywords",
                []
            )


            # ---------------------------------------
            # WEIGHTED KEYWORD MATCHING
            # ---------------------------------------

            for keyword in keywords:

                keyword_lower = (
                    keyword
                    .lower()
                    .strip()
                )

                if keyword_lower in clause:

                    # Weak contextual words
                    if (
                        keyword_lower
                        in generic_keywords
                    ):

                        weight = 0.5


                    # Material legal concepts
                    elif (
                        keyword_lower
                        in material_keywords
                    ):

                        weight = 1.0


                    # Multi-word legal concepts
                    elif " " in keyword_lower:

                        weight = 2.0


                    # Other single-word concepts
                    else:

                        weight = 1.0


                    score += weight

                    matched_keywords.append(
                        f"{keyword} "
                        f"({weight:.1f})"
                    )


            # ---------------------------------------
            # TITLE WORD MATCHING
            # ---------------------------------------

            title_words = re.findall(
                r"\b[a-zA-Z]{4,}\b",
                law["title"].lower()
            )


            for word in title_words:

                if word in clause:

                    score += 0.25


            # ---------------------------------------
            # INITIAL RETRIEVAL
            # ---------------------------------------

            if score >= 0.5:

                matches.append(
                    {
                        "law": law,
                        "score": score,
                        "matched_keywords": (
                            matched_keywords
                        )
                    }
                )


        # ---------------------------------------
        # SORT BY RELEVANCE
        # ---------------------------------------

        matches.sort(
            key=lambda item: item["score"],
            reverse=True
        )


        if not matches:

            return (
                "No relevant Ohio statutes found."
            )


        # ---------------------------------------
        # RELATIVE RELEVANCE FILTER
        # ---------------------------------------

        highest_score = matches[0]["score"]

        relative_threshold = (
            highest_score * 0.25
        )


        matches = [
            match
            for match in matches
            if match["score"]
            >= relative_threshold
        ]


        # ---------------------------------------
        # FORMAT TOOL OUTPUT
        # ---------------------------------------

        output = ""


        for match in matches:

            law = match["law"]

            output += (
                f"Section: "
                f"{law['section']}\n"

                f"Title: "
                f"{law['title']}\n"

                f"Summary: "
                f"{law['summary']}\n"

                f"Retrieval Score: "
                f"{match['score']:.2f}\n"

                f"Matched Concepts: "
                f"{', '.join(match['matched_keywords'])}\n\n"
            )


        return output