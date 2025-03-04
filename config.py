import os
import typesense

GITHUB_BASE = (
    "https://raw.githubusercontent.com/dig-Eds-cat/digEds_cat/refs/heads/main/"
)

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


MODEL = [
    {
        "name": "id",
        "type": "string",
        "sort": True,
        "verbose_name": "id",
        "help_text": "An internal identifier. Provided by the data-curation team",
    },
    {
        "name": "historical_period",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Historical Period",
        "help_text": """
This field broadly categorises the source material of a digital edition by the following periods:

* Antiquity [700 BC - 500 AD]
* Middle Ages [500 - 1500]
* Early Modern [1500 - 1789]
* Long Nineteenth Century [1789 - 1914]
* Modern [1914 - 1965]
* Contemporary [1965 - Today]""",
    },
    {
        "name": "time_century",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Time/Century",
        "help_text": """
The specific year(s) or century of the digital edition's source material.
Year ranges can also be added in the format `YYYY-YYYY`.""",
    },
    {
        "name": "edition_name",
        "type": "string",
        "sort": True,
        "verbose_name": "Edition name",
        "help_text": "The name of the digital edition project.",
    },
    {
        "name": "url",
        "type": "string",
        "sort": True,
        "verbose_name": "URL",
        "help_text": "The URL of the digital edition project.",
    },
    {
        "name": "scholarly",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Scholarly",
        "help_text": """
Here the values yes or no should be used to say whether the edition is _scholarly_ in accordance with [Patrick Sahle](https://www.digitale-edition.de/exist/apps/editions-browser/about.html)'s definition of the term:
>An edition must be critical, must have critical components - a pure facsimile is not an edition, a digital library is not an edition.""",  # noqa: E501
    },
    {
        "name": "digital",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Digital vs. Digitised",
        "help_text": """
Here the values yes or no should be used to say whether the digital edition is _digital_ in accordance with [Patrick Sahle](https://www.digitale-edition.de/exist/apps/editions-browser/about.html)'s definition of the term:
>"A digitized print edition is not a "digital edition". If the paradigm of an edition is limited to the two-dimensional space of the "page" and to typographic means of information representation, then it's not a digital edition." (see: https://www.digitale-edition.de/exist/apps/editions-browser/about.html)""",  # noqa: E501
    },
    {
        "name": "edition",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Edition",
        "help_text": """
Here the values values yes and no should be used to say whether the digital edition is an _edition_ in accordance with [Patrick Sahle](https://www.digitale-edition.de/exist/apps/editions-browser/about.html)'s definition of the term:
>An edition must represent its material (usually as transcribed/edited text) - a catalog, an index, a descriptive database is not an edition.""",  # noqa: E501
    },
    {
        "name": "language",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Language",
        "help_text": """
Here the values values yes and no should be used to say whether the digital edition is an _edition_ in accordance with [Patrick Sahle](https://www.digitale-edition.de/exist/apps/editions-browser/about.html)'s definition of the term:
>An edition must represent its material (usually as transcribed/edited text) - a catalog, an index, a descriptive database is not an edition.""",  # noqa: E501
    },
    {
        "name": "writing_support",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Writing support",
        "help_text": """
The nature of the source material (manuscript, letter, notebook, etc.). Use the singular form of the tag only (e.g. "Letter" even if the edition contains multiple) and capitalise the first letter. Separate multiple source materials with a semicolon.""",  # noqa: E501
    },
    {
        "name": "begin_date",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Begin date",
        "help_text": """
Year the project started. If not specified, use `not provided`.""",
    },
    {
        "name": "end_date",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "End date",
        "help_text": """
Year the project ended. If ongoing type `present`. If not specified, use `not provided`.""",
    },
    {
        "name": "manager_or_editor",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Manager",
        "help_text": """
Name and surname of principal investigator/manager/coordinator.
If multiple, separate with a semicolon.""",
    },
    {
        "name": "institution_s",
        "type": "object[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Participating institution(s)",
        "help_text": """
Institution(s) involved in the project. If multiple, separate with a semicolon.
If not specified, use `not provided`.""",
    },
    {
        "name": "audience",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Audience",
        "help_text": """
The target audience of the digital edition project (scholars, students, general public, etc.).
If not specified, use `not provided`. If multiple, separate with a semicolon.""",
    },
    {
        "name": "philological_statement",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Philological statement",
        "help_text": """
* `no`: No information on the editorial methods and practices nor on the source (digital or printed) of the text.
* `partly`: Some information about the source, and of the author, date and accuracy of the digital edition.
* `yes`: Complete information on the source of the text, as well as on the author, date and accuracy of the digital edition; (Digital Humanities) standards implemented, including modelling, markup language, data structure and software.""",  # noqa:
    },
    {
        "name": "account_of_textual_variance",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Account of textual variance",
        "help_text": """
* `no`: No account of textual variance is given. The digital edition is a reproduction of a given print edition without any account of variants.
* `partly`: The digital edition is a reproduction of a given print scholarly edition and reproduces the selected textual variants extant in the apparatus criticus of that edition; or the edition does not follow a digital paradigm, in that the variants are not automatically computable the way they are encoded.
* `yes`: This edition is “based on full-text transcription of original texts into electronic form” """,  # noqa:
    },
    {
        "name": "value_of_witnesses",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Value of witnesses",
        "help_text": """
* `N/A`: Not applicable, as no information about the source of the text is given, though it is easily assumable that the source is another digital or printed edition (possibly even a scholarly edition).
* `no`: The only witness modelled digitally is a printed non-scholarly edition used as a source for the digital edition.
* `partly`: Same as above, but the witness/source is a scholarly edition.
* `yes`: The witnesses are traditional philological primary sources (including manuscripts, inscriptions or papyri).""",  # noqa:
    },
    {
        "name": "xml_tei_transcription",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "XML-TEI transcription",
        "help_text": """
The source material is encoded in XML-TEI. Values:
* `no`: XML not used
* `partly`: XML but not TEI
* `yes`: XML-TEI is used""",
    },
    {
        "name": "xml_tei_available_to_download",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "XML(-TEI) transcription is available to download",
        "help_text": """
The source material is encoded in XML-TEI. Values:
* `no`
* `partly`
* `yes`""",
    },
]
