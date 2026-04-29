import re

def sanitize_input(data):
    """Basic input sanitization logic."""
    if isinstance(data, str):
        # Remove script tags etc.
        return re.sub(r'<script.*?>.*?</script>', '', data, flags=re.DOTALL)
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_input(i) for i in data]
    return data
