import re


def display_name(raw_name):
    name = str(raw_name or "").strip()
    if "," in name:
        surname, first = [part.strip() for part in name.split(",", 1)]
        return f"{first} {surname}".strip()
    return " ".join(name.split())


def name_key(raw_name):
    name = display_name(raw_name).casefold()
    return re.sub(r"[^a-z0-9]", "", name)

