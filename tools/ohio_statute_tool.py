"""Weighted statute retrieval tool for Ohio statutes.

This implementation uses weighted keyword matching, title boosts, and
relative relevance filtering to return a ranked list of matching statutes.
"""

import json
import re
from pathlib import Path
from typing import List


__version__ = "0.2.0-weighted"


class OhioStatuteTool:
    def __init__(self, data_path: str = None):
        if data_path is None:
            data_path = Path(__file__).parent.parent / "data" / "sample_ohio_laws.json"
        else:
            data_path = Path(data_path)

        with open(data_path, "r", encoding="utf-8") as fh:
            self.laws = json.load(fh)

    def search_statutes(self, clause: str) -> str:
        clause = re.sub(r"\s+", " ", clause.lower()).strip()

        matches = []

        generic_keywords = {
            "buyer",
            "seller",
            "goods",
            "written",
            "signed",
            "writing",
            "verbal",
            "oral",
        }

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
            "damages",
        }

        for law in self.laws:
            score = 0.0
            matched_keywords = []
            keywords = law.get("keywords", [])

            for keyword in keywords:
                keyword_lower = keyword.lower().strip()
                if not keyword_lower:
                    continue
                if keyword_lower in clause:
                    if keyword_lower in generic_keywords:
                        weight = 0.5
                    elif keyword_lower in material_keywords:
                        weight = 1.0
                    elif " " in keyword_lower:
                        weight = 2.0
                    else:
                        weight = 1.0

                    score += weight
                    matched_keywords.append(f"{keyword} ({weight:.1f})")

            title_words = re.findall(r"\b[a-zA-Z]{4,}\b", law.get("title", "").lower())
            for word in title_words:
                if word in clause:
                    score += 0.25

            if score >= 0.5:
                matches.append({"law": law, "score": score, "matched_keywords": matched_keywords})

        matches.sort(key=lambda item: item["score"], reverse=True)

        if not matches:
            return "No relevant Ohio statutes found."

        highest_score = matches[0]["score"]
        relative_threshold = highest_score * 0.25

        matches = [m for m in matches if m["score"] >= relative_threshold]

        output = []
        for match in matches:
            law = match["law"]
            output.append(f"Section: {law['section']}")
            output.append(f"Title: {law['title']}")
            output.append(f"Summary: {law['summary']}")
            output.append(f"Retrieval Score: {match['score']:.2f}")
            output.append(f"Matched Concepts: {', '.join(match['matched_keywords'])}\n")

        return "\n".join(output)
