import re
import unicodedata


def slugify(value: str) -> str:
    """
    Convert a human-readable value into a URL-safe slug.

    Examples:
        "Berliner Antike-Kolleg DAAD PhD Scholarships 2027"
        ->
        "berliner-antike-kolleg-daad-phd-scholarships-2027"
    """

    if not value:
        return ""

    value = unicodedata.normalize(
        "NFKD",
        value,
    )

    value = value.encode(
        "ascii",
        "ignore",
    ).decode("ascii")

    value = value.lower()

    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        value,
    )

    value = re.sub(
        r"-+",
        "-",
        value,
    )

    return value.strip("-")