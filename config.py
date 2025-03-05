import os
import typesense

GITHUB_BASE = (
    "https://raw.githubusercontent.com/dig-Eds-cat/digEds_cat/refs/heads/main"
)

DATA_SCHEMA_URL = f"{GITHUB_BASE}/schema.json"
EDITIONS = f"{GITHUB_BASE}/digEds_cat.csv"
INSTITUTIONS = f"{GITHUB_BASE}/institutions_places_enriched.csv"

TS_CLIENT = typesense.Client(
    {
        "nodes": [
            {
                "host": os.environ.get("TYPESENSE_HOST", "localhost"),
                "port": os.environ.get("TYPESENSE_PORT", "8108"),
                "protocol": os.environ.get("TYPESENSE_PROTOCOL", "http"),
            }
        ],
        "api_key": os.environ.get("TYPESENSE_API_KEY", "xyz"),
        "connection_timeout_seconds": 2,
    }
)

TS_SCHEMA_NAME = "dig-ed-cat"

MANDATORY_FIELDS = ["id", "edition_name", "url"]

#  fields listed here expect multiple values separated with ";"
FACET_FIELDS = [
    "historical_period",
    "language",
    "writing_support",
    "manager_or_editor",
    "audience",
    "language",
    "ocr_or_keyed",
    "repository_of_source_material_s",
    "place_of_origin_of_source_material_s",
    "sponsor_funding_body",
    "infrastructure",
    "website_language",
]

#  fields listed here contain unique values
NO_FACET_FIELDS = [
    "edition_name",
    "url",
    "handle_pid",
    "budget_rough",
    "ride_review",
]

NO_INDEX_FIELDS = [
    "resolver",
    "next",
    "prev",
]
