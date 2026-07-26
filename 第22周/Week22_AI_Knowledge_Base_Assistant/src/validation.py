import re

def validate_document(text: str) -> bool:
    if not text or len(text.strip()) == 0:
        return False
    if len(text) < 10:
        return False
    return True

def prompt_filter(prompt: str) -> bool:
    bad_words = ["hack", "exploit", "password"]
    for w in bad_words:
        if w in prompt.lower():
            return False
    return True

def check_permission(user_role: str, metadata: dict) -> bool:
    if user_role == "admin":
        return True
    if metadata.get("private", False):
        return False
    return True