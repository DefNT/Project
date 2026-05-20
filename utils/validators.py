import re

def validate_not_empty(text):
    return bool(text and str(text).strip())

def validate_score(score):
    try:
        val = float(score)
        if 0 <= val <= 100:
            return True, val
        return False, None
    except (ValueError, TypeError):
        return False, None

def validate_name(name):
    if not name or not str(name).strip():
        return False
    return bool(re.match(r"^[a-zA-Z]+([\s\-][a-zA-Z]+)*$", name)) and 2 <= len(name) <= 50

def validate_credits(credits_str):
    try:
        val = int(credits_str)
        return 1 <= val <= 10
    except (ValueError, TypeError):
        return False