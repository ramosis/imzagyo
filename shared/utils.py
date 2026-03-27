from bleach import clean
from flask import jsonify
from shared.extensions import cache

def invalidate_entity_cache(entity_type: str):
    """
    Clears cache for a specific entity type (Portfolio or Lead).
    In SimpleCache, we primarily use brute force delete for the view keys.
    """
    # For now, clear the whole cache to ensure consistency as requested in Phase 17
    # This addresses the 'Ben ekledim ama göremiyorum' issue.
    cache.clear()

def api_error(code, message, details=None, status_code=400):
    """
    Returns a standardized JSON error response (DX Phase 13).
    """
    response = {
        "error": {
            "code": code,
            "message": message
        }
    }
    if details:
        response["error"]["details"] = details
    return jsonify(response), status_code

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
