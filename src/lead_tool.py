from __future__ import annotations


def mock_lead_capture(name: str, email: str, platform: str) -> dict:
    message = f"Lead captured successfully: {name}, {email}, {platform}"
    print(message)
    return {
        "status": "success",
        "message": message,
        "lead": {"name": name, "email": email, "platform": platform},
    }
