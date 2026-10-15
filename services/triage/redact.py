import re

_EMAIL = re.compile(r"\S+@\S+")


def redact(text: str) -> str:
    return _EMAIL.sub("[redacted-email]", text)
