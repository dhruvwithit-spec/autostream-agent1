from __future__ import annotations

import re
from typing import Any

PLATFORM_PATTERNS = {
    "youtube": re.compile(r"\byoutube\b", re.IGNORECASE),
    "instagram": re.compile(r"\binstagram\b", re.IGNORECASE),
    "tiktok": re.compile(r"\btiktok\b", re.IGNORECASE),
    "linkedin": re.compile(r"\blinkedin\b", re.IGNORECASE),
    "facebook": re.compile(r"\bfacebook\b", re.IGNORECASE),
    "twitter": re.compile(r"\btwitter\b", re.IGNORECASE),
    "x": re.compile(r"\bon\s+x\b|\bplatform\s*[:\-]?\s*x\b", re.IGNORECASE),
    "podcast": re.compile(r"\bpodcast\b", re.IGNORECASE),
    "twitch": re.compile(r"\btwitch\b", re.IGNORECASE),
}


class LeadInfoExtractor:
    email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
    name_patterns = [
        re.compile(r"(?:my name is|i am|i'm)\s+([A-Za-z][A-Za-z\s'-]{1,50}?)(?=\s+(?:and\s+my\s+email|and\s+email|my\s+email|email\s+is)\b|[.!?,]|$)", re.IGNORECASE),
        re.compile(r"name\s*[:\-]\s*([A-Za-z][A-Za-z\s'-]{1,50}?)(?=\s+(?:and\s+my\s+email|and\s+email|my\s+email|email\s+is)\b|[.!?,]|$)", re.IGNORECASE),
    ]

    def update_state_from_message(self, state: dict[str, Any], message: str) -> dict[str, Any]:
        updated = dict(state)

        email_match = self.email_regex.search(message)
        if email_match:
            updated["email"] = email_match.group(0)

        for platform, pattern in PLATFORM_PATTERNS.items():
            if pattern.search(message):
                updated["platform"] = "X" if platform == "x" else platform.title()
                break

        for pattern in self.name_patterns:
            match = pattern.search(message)
            if match:
                candidate = match.group(1).strip().rstrip(".!,")
                updated["name"] = " ".join(word.capitalize() for word in candidate.split())
                break

        return updated

    @staticmethod
    def missing_fields(state: dict[str, Any]) -> list[str]:
        missing = []
        for field in ["name", "email", "platform"]:
            if not state.get(field):
                missing.append(field)
        return missing
