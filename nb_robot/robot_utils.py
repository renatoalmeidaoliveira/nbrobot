def is_same_keyword(first: str, second: str):
    return _get_normalized_keyword(first) == _get_normalized_keyword(second)


def _get_normalized_keyword(keyword: str):
    return keyword.lower().replace(" ", "").replace("_", "")

