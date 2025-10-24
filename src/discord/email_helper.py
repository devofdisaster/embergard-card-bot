import re
import urllib.parse
from typing import Optional, Tuple

SUBJECT_PATTERN = r"\[\[\s*(.*?)\s*\]\]\s*\n?(.*)"
RECIPIENT_EMAIL = "whunderworlds@gwplc.com"


def parse_email_request(message_content: str) -> Optional[Tuple[str, str]]:
    """
    Parse a Discord message for email request pattern.

    Expected format:
    [[Subject Line]]
    Email body content
    Can be multiple lines

    Args:
        message_content: The full Discord message content

    Returns:
        Tuple of (subject, body) if pattern matches, None otherwise
    """
    match = re.search(SUBJECT_PATTERN, message_content, re.DOTALL)

    if not match:
        return None

    subject = match.group(1).strip()
    body = match.group(2).strip()

    if not subject or not body:
        return None

    return subject, body


def generate_mailto_link(subject: str, body: str) -> str:
    encoded_subject = urllib.parse.quote(subject)
    encoded_body = urllib.parse.quote(body)

    return f"mailto:{RECIPIENT_EMAIL}?subject={encoded_subject}&body={encoded_body}"
