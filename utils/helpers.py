"""Miscellaneous helper functions."""
import re
from urllib.parse import urlparse


def clean_text(text: str) -> str:
    """
    Normalize extracted text.
    """
    return " ".join(text.split()).strip()


def extract_domain(url: str) -> str:
    """
    Extract domain name from URL.
    """
    parsed = urlparse(url)
    return parsed.netloc


def is_valid_email(email: str) -> bool:
    """
    Basic email regex validation.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern, email) is not None


def safe_get(dictionary: dict, key: str, default=None):
    """
    Safely access dictionary keys.
    """
    return dictionary.get(key, default)