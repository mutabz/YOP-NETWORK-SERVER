from app.modules.opportunities.enums import OpportunityType


TYPE_ALIASES: dict[OpportunityType, tuple[str, ...]] = {
    OpportunityType.JOB: (
        "job",
        "jobs",
        "employment",
        "career",
        "careers",
        "full-time",
        "full-time-job",
        "full-time-jobs",
    ),

    OpportunityType.SCHOLARSHIP: (
        "scholarship",
        "scholarships",
        "student-scholarship",
        "international-scholarship",
        "study-scholarship",
        "education-scholarship",
        "academic-scholarship",
        "financial-aid",
        "student-funding",
    ),

    OpportunityType.INTERNSHIP: (
        "internship",
        "internships",
        "intern",
        "intern-program",
        "internship-program",
        "student-internship",
        "graduate-internship",
        "professional-internship",
        "work-placement",
    ),

    OpportunityType.COMPETITION: (
        "competition",
        "competitions",
        "contest",
        "contests",
        "challenge",
        "challenges",
        "innovation-challenge",
        "innovation-competition",
        "startup-competition",
        "startup-challenge",
        "pitch-competition",
        "hackathon",
    ),
}


COUNTRY_ALIASES: dict[str, tuple[str, ...]] = {
    "united states": (
        "united-states",
        "united-states-of-america",
        "usa",
        "us",
        "u-s",
        "america",
    ),

    "united kingdom": (
        "united-kingdom",
        "uk",
        "u-k",
        "great-britain",
        "britain",
        "england",
    ),

    "canada": (
        "canada",
        "ca",
        "can",
    ),

    "australia": (
        "australia",
        "au",
        "aus",
    ),

    "germany": (
        "germany",
        "de",
        "deutschland",
    ),

    "france": (
        "france",
        "fr",
    ),

    "japan": (
        "japan",
        "jp",
        "japanese",
    ),

    "china": (
        "china",
        "cn",
        "chinese",
    ),

    "south korea": (
        "south-korea",
        "korea",
        "republic-of-korea",
        "kr",
        "korean",
    ),

    "india": (
        "india",
        "in",
        "indian",
    ),

    "rwanda": (
        "rwanda",
        "rw",
        "rwandan",
    ),

    "south africa": (
        "south-africa",
        "za",
        "south-african",
    ),

    "netherlands": (
        "netherlands",
        "holland",
        "nl",
        "dutch",
    ),

    "switzerland": (
        "switzerland",
        "ch",
        "swiss",
    ),

    "sweden": (
        "sweden",
        "se",
        "swedish",
    ),

    "norway": (
        "norway",
        "no",
        "norwegian",
    ),

    "denmark": (
        "denmark",
        "dk",
        "danish",
    ),

    "finland": (
        "finland",
        "fi",
        "finnish",
    ),

    "new zealand": (
        "new-zealand",
        "nz",
        "new-zealander",
    ),
}


DEGREE_ALIASES: dict[str, tuple[str, ...]] = {
    "undergraduate": (
        "undergraduate",
        "undergraduate-degree",
        "undergraduate-study",
        "bachelor",
        "bachelors",
        "bachelor-degree",
        "bachelors-degree",
        "college",
    ),

    "masters": (
        "master",
        "masters",
        "master-degree",
        "masters-degree",
        "master's",
        "master's-degree",
        "postgraduate",
        "postgraduate-degree",
    ),

    "phd": (
        "phd",
        "ph-d",
        "doctoral",
        "doctorate",
        "doctoral-degree",
    ),

    "postgraduate": (
        "postgraduate",
        "postgraduate-degree",
        "graduate",
        "graduate-study",
    ),
}


REMOTE_ALIASES: tuple[str, ...] = (
    "remote",
    "remote-work",
    "remote-opportunity",
    "work-from-home",
    "wfh",
    "work-remotely",
    "online",
    "virtual",
)


CATEGORY_ALIASES: dict[str, tuple[str, ...]] = {
    "technology": (
        "technology",
        "tech",
        "information-technology",
        "it",
        "software",
        "software-development",
        "software-engineering",
        "programming",
        "computer-science",
        "cs",
        "ict",
    ),

    "business": (
        "business",
        "business-administration",
        "management",
        "entrepreneurship",
        "commerce",
    ),

    "engineering": (
        "engineering",
        "engineer",
        "engineering-studies",
    ),

    "economics": (
        "economics",
        "economic",
        "economy",
    ),

    "health": (
        "health",
        "healthcare",
        "medicine",
        "medical",
        "public-health",
    ),

    "education": (
        "education",
        "educational",
        "academic",
        "studies",
        "higher-education",
        "university",
        "college",
        "learning",
    ),

    "science": (
        "science",
        "scientific",
        "natural-sciences",
        "research",
    ),

    "social-sciences": (
        "social-sciences",
        "social-science",
        "sociology",
        "political-science",
        "psychology",
    ),

    "law": (
        "law",
        "legal",
        "legal-studies",
    ),

    "environment": (
        "environment",
        "environmental",
        "climate",
        "climate-change",
        "sustainability",
        "sustainable-development",
    ),

    "entrepreneurship": (
        "entrepreneurship",
        "entrepreneur",
        "startup",
        "startups",
        "innovation",
        "business-innovation",
    ),
}