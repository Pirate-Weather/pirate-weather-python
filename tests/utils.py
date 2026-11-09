"""Helpers for the tests."""


def snake_case_key(key: str) -> str:
    """Convert a camelCase API field name to its snake_case attribute name."""
    assert isinstance(key, str)
    new_key = key[0]
    for char in key[1:]:
        if char.isupper():
            new_key += f"_{char.lower()}"
        elif char == "-":
            new_key += "__"
        else:
            new_key += char
    return new_key
