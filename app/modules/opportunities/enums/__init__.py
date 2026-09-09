from enum import StrEnum


class SourceType(StrEnum):
    WEBSITE = "website"
    RSS = "rss"
    API = "api"


class OpportunityType(StrEnum):
    JOB = "job"
    SCHOLARSHIP = "scholarship"
    INTERNSHIP = "internship"
    COMPETITION = "competition"


class OpportunityStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"
    EXPIRED = "expired"
    ARCHIVED = "archived"


__all__ = [
    "SourceType",
    "OpportunityType",
    "OpportunityStatus",
]