from collections.abc import MutableMapping

def flatten_dict(data: dict, sep: str = '_', parent_key = '') -> dict:
    """
    Merge two dicts into a single one
    """
    items = []

    for key, value in data.items():
        new_key = parent_key + sep + str(key) if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, sep, new_key).items())
        else:
            items.append((new_key, value))

    return dict(items)