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
    if not name: return False
    return bool(re.match(r"^[a-zA-Z\s\-]{2,50}$", name))