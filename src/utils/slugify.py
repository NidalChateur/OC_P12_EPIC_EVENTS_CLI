import re


def slugify(value: str) -> str:
    return re.sub(r"\W+", "-", value.lower())
