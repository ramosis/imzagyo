from bleach import clean

def sanitize_input(data):
    """
    Recursively sanitizes input data to prevent XSS (Audit Section 6.2).
    """
    if isinstance(data, str):
        # Strip all tags by default for generic fields
        return clean(data, tags=[], strip=True)
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    return data

def sanitize_html(html_content: str) -> str:
    """
    Sanitizes HTML content allowing a safe set of tags.
    """
    allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3']
    return clean(html_content, tags=allowed_tags, strip=True)
