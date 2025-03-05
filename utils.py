"""some helper functions"""

import typesense


def strip(some_string: str) -> str:
    """removes leading and trailing whitespaces

    Args:
        some_string (str): some string

    Returns:
        str: the same string without whitespaces
    """
    return some_string.strip()


def delete_and_create_schema(ts_client, ts_schema_name, ts_schema):
    try:
        ts_client.collections[ts_schema_name].delete()
    except typesense.api_call.ObjectNotFound:
        pass
    created = ts_client.collections.create(ts_schema)
    return created
