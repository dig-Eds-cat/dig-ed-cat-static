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
    {
        "name": "images",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Images",
        "help_text": """
The values `no`, `partly` or `yes` are used to specify if the edition comes with images. The value `not provided` is used for digital editions protected by access restrictions or paywalls whose homepage does not make clear whether images are provided.""",  # noqa: E501
    },
    {
        "name": "zoom_images",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Zoom images",
        "help_text": """
The values `yes` or `no` are used to specify if the user can zoom in or out of images.""",
    },
    {
        "name": "image_manipulation_brightness_rotation_etc",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Image manipulation",
        "help_text": """
The values `yes`or `no` are used to specify whether the user can manipulate the images (e.g. rotation, brightness, etc.).""",  # noqa: E501
    },
    {
        "name": "text_image_linking",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Image manipulation",
        "help_text": """
The values `yes` or `no` are used to tell us whether the transcription and the image are linked so that clicking on a word (or line) in the image brings up the corresponding word in the transcription and vice-versa.""",  # noqa: E501
    },
    {
        "name": "source_text_translation",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Source text translation",
        "help_text": """
The project provides a translation of the source material (not necessarily into English). If so, the corresponding [three-letter ISO codes](http://www.loc.gov/standards/iso639-2/php/code_list.php) should be used. If not, type `no`.""",  # noqa: E501
    },
    {
        "name": "website_language",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Website language",
        "help_text": """
The project website is available in multiple languages. If so, the corresponding [three-letter ISO codes](http://www.loc.gov/standards/iso639-2/php/code_list.php) should be used. If not, simply type `no`.""",  # noqa: E501
    },
    {
        "name": "glossary",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Glossary",
        "help_text": """
The values `yes` or `no` are used to specify if the digital edition provides a glossary.""",  # noqa: E501
    },
    {
        "name": "indices",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Indices",
        "help_text": """
The values `yes` or `no` are used to specify if the digital edition provides indices.""",
    },
    {
        "name": "string_matching",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "String matching search",
        "help_text": """
The values `yes` or `no` are used to specify if the edition provides string matching (full text) search possibilities.
""",
    },
    {
        "name": "advanced_search",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Advanced search",
        "help_text": """
The values `yes` or `no` are used to specify if the digital edition provides advanced search functionality."""
    },
    {
        "name": "creative_commons_license",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Creative Commons License",
        "help_text": """
The values `yes`, `partially` or `no` are used to specify if the digital edition is protected by a Creative Commons License."""  # noqa: E501
    },
    {
        "name": "open_source_open_access",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Open Source/Open Access",
        "help_text": """
* `no`: Proprietary, all material is copyrighted. The source is closed and not reusable by other research projects. To access the material, users must pay a subscription fee.
* `partly`: Same as above but the subscription is free of charge.
* `yes`: Open Access. The texts may be accessed through specific software but the source is not accessible.
* `Open Access and Open Source (some data)`: Open Access and Open Source. Part of the data underlying the digital edition (e.g. text but not images) is freely available for access and reuse.
* `Open Access and Open Source (all data)`: Open Access and Open Source. All data underlying the digital edition is freely available for access and reuse."""  # noqa: E501
    },
    {
        "name": "linked_open_data",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Linked Open Data (LOD)",
        "help_text": """
The values `yes` or `no` are used to specify if the digital edition makes use of [Linked Open Data](https://programminghistorian.org/lessons/intro-to-linked-data) (LOD) standards and if it is linked to other projects/data."""  # noqa: E501
    },
    {
        "name": "api",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Application Programming Interface (API)",
        "help_text": """
The values `yes` or `no` are used to specify if the digital edition comes with an API."""
    },
    {
        "name": "crowdsourcing",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Crowdsourcing",
        "help_text": """
The values `yes` or `no` are used to specify if the digital edition relies/relied on crowdsourced contributions."""
    },
    {
        "name": "feedback",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Feedback",
        "help_text": """
The values `yes` or `no` are used to specify if the digital edition provides a feedback space or contact information for users to make comments or suggestions."""  # noqa: E501
    },
    {
        "name": "technological_statement",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Technological statement",
        "help_text": """
This category assesses whether the digital edition provides complete information about technical aspects and practices.
* `no`: no information.
* `partly`: partial information.
* `yes`: complete information."""  # noqa: E501
    },
    {
        "name": "links_to_ext_resources",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Technological statement",
        "help_text": """The values `yes` or `no` are used to specify if the digital edition provides links to external relevant resources."""  # noqa: E501
    },
    {
        "name": "ocr_or_keyed",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "OCR'd or keyed",
        "help_text": """The source text was digitised with Optical Character Recognition (OCR) software or manually Keyed in. Use `Keyed`, `OCR` or `Keyed; OCR"""  # noqa: E501
    },
    {
        "name": "mobile_friendly_application",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Mobile-friendly/application",
        "help_text": """The values `yes` or `no` are used to tell if the project is mobile friendly"""  # noqa: E501
    },
    {
        "name": "print_friendly_view",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Print-friendly view",
        "help_text": """The values `yes` or `no` are used to specify if the digital edition provides a print-friendly view of the text (e.g. PDF) or if the browser produces a suitable, printable version of the content."""  # noqa: E501
    },
    {
        "name": "print_facsimile_complementary_output",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Print facsimile (complementary output)",
        "help_text": """The values `yes` or `no` are used to specify if the digital project is complemented by a printed facsimile."""  # noqa: E501
    },
    {
        "name": "repository_of_source_material_s",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "optional": True,
        "verbose_name": "Repository of source material",
        "help_text": """The institution(s) that house the source text(s). `N/A` is used if the source is a new edition without a physical location, and `not provided` is used to indicate that the project website does not give clear information about the source's current repository."""  # noqa: E501
    },
    {
        "name": "place_of_origin_of_source_material_s",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Place of origin of source material",
        "help_text": """If known, the location from which the source text originated or where it was produced. `N/A` is used to indicate that the project does not have a physical provenance, and `not provided` is used to indicate that the project website does not give clear information about the source's provenance."""  # noqa: E501
    },
    {
        "name": "sponsor_funding_body",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Sponsor/Funding body",
        "help_text": """The name of the funding agency. `N/A` is used if the project isn't supported by third-party funding."""  # noqa: E501
    },
    {
        "name": "budget_rough",
        "type": "string",
        "facet": True,
        "optional": True,
        "sort": True,
        "verbose_name": "Budget (rough)",
        "help_text": """How much the project cost. All currencies are supported and the numeric value should use commas as thousands separators (e.g. £10,000). The value `not provided` is used to indicate that the project website does not make this information known; `0` is used to indicate that the project specifies that it does not rely on funding."""  # noqa: E501
    },
    {
        "name": "infrastructure",
        "type": "string[]",
        "facet": True,
        "optional": True,
        "verbose_name": "Infrastructure",
        "help_text": """The technologies used to build the digital edition (Drupal, Omeka, MySQL, etc.). If multiple, please separate with a semicolon."""  # noqa: E501
    },
    {
        "name": "current_availability",
        "type": "string",
        "facet": True,
        "optional": True,
        "verbose_name": "Current availability",
        "help_text": """Even if completed in the past, the digital edition is still viewable online today. The values `yes`(alive) and `no` (not available) are used."""  # noqa: E501
    },
    {
        "name": "ride_review",
        "type": "string",
        "facet": False,
        "optional": True,
        "sort": True,
        "verbose_name": "Reviewed in RIDE",
        "help_text": """Was the edition reviewed in [RIDE](https://ride.i-d-e.de/), add the URL to the review or `no`"""  # noqa: E501
    },
    {
        "name": "sahle_catalog",
        "type": "string",
        "facet": False,
        "optional": True,
        "sort": True,
        "verbose_name": "Sahle Catalog",
        "help_text": """Is the edition mentioned in [https://www.digitale-edition.de](https://www.digitale-edition.de) add the URL to the entry (e.g. https://digitale-edition.de/e862) or `no`"""  # noqa: E501
    },
]
