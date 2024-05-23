""" some helper functions """

import typesense


def strip(some_string: str) -> str:
    """removes leading and trailing whitespaces

    Args:
        some_string (str): some string

    Returns:
        str: the same string without whitespaces
    """
    return some_string.strip()


def resolve_number_codes(number_code: str) -> str:
    """translates number codes into something human readable

    Args:
        number_code (str): either 0, 0.5, 1, 2, or 3

    Returns:
        str: "no", "partly", "yes"
    """
    if str(number_code) == "0":
        return "no"
    if str(number_code) == "0.5":
        return "partly"
    if str(number_code) == "1":
        return "yes"
    if str(number_code) == "1.5":
        return "Open Access and Open Sourc (some data)"
    if str(number_code) == "2":
        return "Open Access and Open Source (all data)"
    if str(number_code) == "2.0":
        return "Open Access and Open Source (all data)"
    return str(number_code)


def make_schema(
    record, ts_schema_name, mandatory_fields, no_facet_field, no_index_fields
):
    TS_SCHEMA = {"name": ts_schema_name, "enable_nested_fields": True, "fields": []}
    for key, value in record.items():
        if key in mandatory_fields:
            TS_SCHEMA["fields"].append({"name": key, "type": "string", "sort": True})
        elif key in no_index_fields:
            TS_SCHEMA["fields"].append(
                {
                    "name": key,
                    "type": "string",
                    "facet": False,
                    "index": False,
                }
            )
        elif key in no_facet_field:
            TS_SCHEMA["fields"].append(
                {
                    "name": key,
                    "type": "string",
                    "facet": False,
                    "optional": True,
                    "sort": True,
                }
            )
        elif isinstance(value, list):
            if isinstance(value[0], dict):
                TS_SCHEMA["fields"].append(
                    {"name": key, "type": "object[]", "facet": True, "optional": True}
                )
            else:
                TS_SCHEMA["fields"].append(
                    {"name": key, "type": "string[]", "facet": True, "optional": True}
                )
        else:
            TS_SCHEMA["fields"].append(
                {"name": key, "type": "string", "facet": True, "optional": True}
            )
    return TS_SCHEMA


def delete_and_create_schema(ts_client, ts_schema_name, ts_schema):
    try:
        ts_client.collections[ts_schema_name].delete()
    except typesense.api_call.ObjectNotFound:
        pass
    created = ts_client.collections.create(ts_schema)
    return created
