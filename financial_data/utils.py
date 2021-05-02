def to_camel(string: str) -> str:
    first, *rest = string.split("_")
    return "".join([first.lower(), *map(str.title, rest)])
