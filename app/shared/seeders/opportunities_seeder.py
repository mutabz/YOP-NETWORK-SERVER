from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.opportunities.models import Opportunity
from app.modules.opportunities.enums import (
    OpportunityStatus,
    OpportunityType,
)


class OpportunitySeeder:
    DEFAULT_OPPORTUNITIES = (

        # =========================================================
        # 1. JOB
        # =========================================================
        {
            "title": "Junior Software Engineer",
            "slug": "junior-software-engineer",

            "slug_list": [
                # -------------------------------------------------
                # Canonical / title variations
                # -------------------------------------------------
                "junior-software-engineer",
                "junior-software-engineer-job",
                "junior-software-engineering-job",
                "junior-software-developer",
                "junior-software-developer-job",
                "software-engineer",
                "software-engineer-job",
                "software-developer",
                "software-developer-job",
                "entry-level-software-engineer",
                "entry-level-software-developer",
                "graduate-software-engineer",
                "graduate-software-developer",

                # -------------------------------------------------
                # Opportunity type
                # -------------------------------------------------
                "job",
                "jobs",
                "employment",
                "career",
                "careers",
                "full-time",
                "full-time-job",
                "full-time-jobs",
                "ft-job",
                "ft-jobs",

                # -------------------------------------------------
                # Category
                # -------------------------------------------------
                "technology",
                "tech",
                "information-technology",
                "it",
                "software",
                "software-development",
                "software-engineering",
                "programming",
                "web-development",
                "computer-science",
                "cs",
                "ict",

                # -------------------------------------------------
                # Skills / searchable technologies
                # -------------------------------------------------
                "python",
                "javascript",
                "js",
                "rest-api",
                "rest-apis",
                "api",
                "apis",
                "git",
                "version-control",
                "web-applications",
                "web-app",
                "frontend",
                "backend",
                "full-stack",
                "fullstack",

                # -------------------------------------------------
                # Experience / level
                # -------------------------------------------------
                "junior",
                "entry-level",
                "entrylevel",
                "graduate",
                "early-career",
                "0-2-years",
                "2-years-experience",
                "no-experience",
                "little-experience",

                # -------------------------------------------------
                # Organization
                # -------------------------------------------------
                "novatech-solutions",
                "novatech",
                "nova-tech",

                # -------------------------------------------------
                # Country
                # -------------------------------------------------
                "united-states",
                "united-states-of-america",
                "usa",
                "us",
                "u-s",
                "america",
                "united-states-usa",

                # -------------------------------------------------
                # City / location
                # -------------------------------------------------
                "austin",
                "austin-texas",
                "austin-tx",
                "texas",
                "tx",
                "austin-texas-usa",
                "austin-usa",

                # -------------------------------------------------
                # Remote
                # -------------------------------------------------
                "remote",
                "remote-job",
                "remote-jobs",
                "work-from-home",
                "wfh",
                "work-remotely",
                "remote-work",

                # -------------------------------------------------
                # Education
                # -------------------------------------------------
                "computer-science-degree",
                "computer-science-diploma",
                "cs-degree",
                "software-engineering-degree",
                "technology-degree",
                "tech-degree",
            ],

            "type": OpportunityType.JOB,
            "category": "technology",

            "organization": "NovaTech Solutions",

            "country": "United States",
            "city": "Austin",
            "location": "Austin, Texas / Remote",
            "remote": True,

            "deadline": None,
            "start_date": None,
            "end_date": None,

            "summary": [
                "NovaTech Solutions is looking for a Junior Software Engineer "
                "to join its product development team.",
                "The role is suitable for early-career developers interested "
                "in building modern web applications."
            ],

            "description": [
                {
                    "heading": "About the role",
                    "content": (
                        "The successful candidate will work with experienced "
                        "engineers to design, develop, test, and maintain "
                        "web-based applications."
                    ),
                },
                {
                    "heading": "Responsibilities",
                    "items": [
                        "Develop and maintain software applications.",
                        "Write clean and maintainable code.",
                        "Participate in code reviews.",
                        "Work with designers and product teams.",
                        "Investigate and fix software issues.",
                    ],
                },
            ],

            "eligibility": [
                "Open to candidates with up to 2 years of professional experience.",
                "Applicants must have a degree, diploma, or equivalent practical "
                "experience in Computer Science or a related field.",
                "Applicants must be legally eligible to work in the selected "
                "employment location.",
            ],

            "requirements": [
                "Basic knowledge of Python, JavaScript, or another programming language.",
                "Understanding of Git and version control.",
                "Basic knowledge of REST APIs.",
                "Good communication and problem-solving skills.",
            ],

            "application_url": "https://example.test/opportunities/junior-software-engineer",

            "source_url": "https://example.test/jobs/junior-software-engineer",
            "source_name": "Example Jobs",

            "status": OpportunityStatus.DRAFT,

            "extras": {
                "employment_type": "Full-time",
                "experience_level": "Entry-level",
                "salary": {
                    "min": 55000,
                    "max": 70000,
                    "currency": "USD",
                    "period": "year",
                },
                "work_schedule": "40 hours/week",
                "benefits": [
                    "Health insurance",
                    "Paid time off",
                    "Professional development",
                ],
            },
        },


        # =========================================================
        # 2. SCHOLARSHIP
        # =========================================================
        {
            "title": "Global Future Scholars Program",
            "slug": "global-future-scholars-program",

            "slug_list": [
                # -------------------------------------------------
                # Canonical / title variations
                # -------------------------------------------------
                "global-future-scholars-program",
                "global-future-scholars",
                "future-scholars-program",
                "global-scholars-program",
                "future-scholars",
                "global-scholarship",
                "future-scholarship",
                "global-future-scholarship",
                "global-future-scholars-scholarship",

                # -------------------------------------------------
                # Opportunity type
                # -------------------------------------------------
                "scholarship",
                "scholarships",
                "fully-funded-scholarship",
                "fully-funded-scholarships",
                "funded-scholarship",
                "student-scholarship",
                "international-scholarship",
                "study-scholarship",
                "education-scholarship",
                "academic-scholarship",
                "financial-aid",
                "student-funding",

                # -------------------------------------------------
                # Category
                # -------------------------------------------------
                "education",
                "educational",
                "academic",
                "studies",
                "higher-education",
                "university",
                "college",
                "learning",

                # -------------------------------------------------
                # Study levels
                # -------------------------------------------------
                "undergraduate",
                "undergraduate-scholarship",
                "bachelor",
                "bachelors",
                "bachelor-degree",
                "postgraduate",
                "postgraduate-scholarship",
                "masters",
                "master",
                "master-degree",
                "phd",
                "doctoral",
                "doctorate",

                # -------------------------------------------------
                # Fields of study
                # -------------------------------------------------
                "computer-science",
                "cs",
                "computer-science-scholarship",
                "engineering",
                "engineering-scholarship",
                "business",
                "business-scholarship",
                "economics",
                "economics-scholarship",
                "public-policy",
                "public-policy-scholarship",

                # -------------------------------------------------
                # Funding
                # -------------------------------------------------
                "fully-funded",
                "fully-funded-study",
                "full-funding",
                "tuition",
                "tuition-fees",
                "tuition-support",
                "living-allowance",
                "stipend",
                "financial-support",
                "mentorship",
                "career-development",

                # -------------------------------------------------
                # Organization
                # -------------------------------------------------
                "futurebridge-foundation",
                "futurebridge",
                "future-bridge",

                # -------------------------------------------------
                # Country
                # -------------------------------------------------
                "united-kingdom",
                "uk",
                "u-k",
                "great-britain",
                "britain",
                "england",

                # -------------------------------------------------
                # City / location
                # -------------------------------------------------
                "london",
                "london-uk",
                "london-united-kingdom",

                # -------------------------------------------------
                # Student / applicant terms
                # -------------------------------------------------
                "students",
                "student",
                "international-students",
                "international-student",
                "scholar",
                "scholars",
                "academic-excellence",
                "leadership",
                "community-impact",
            ],

            "type": OpportunityType.SCHOLARSHIP,
            "category": "education",

            "organization": "FutureBridge Foundation",

            "country": "United Kingdom",
            "city": "London",
            "location": "United Kingdom",
            "remote": False,

            "deadline": None,
            "start_date": None,
            "end_date": None,

            "summary": [
                "The Global Future Scholars Program supports talented students "
                "who want to pursue undergraduate or postgraduate studies.",
                "Selected scholars receive financial support and access to "
                "professional development opportunities."
            ],

            "description": [
                {
                    "heading": "About the scholarship",
                    "content": (
                        "The program is designed to support academically strong "
                        "students who demonstrate leadership potential and a "
                        "commitment to creating positive impact in their communities."
                    ),
                },
                {
                    "heading": "Scholarship benefits",
                    "items": [
                        "Tuition fee support.",
                        "Living allowance.",
                        "Academic mentoring.",
                        "Career development workshops.",
                    ],
                },
            ],

            "eligibility": [
                "Applicants must be enrolled in or applying to an accredited institution.",
                "Applicants must demonstrate strong academic performance.",
                "Applicants must demonstrate leadership or community involvement.",
                "Applicants must meet the admission requirements of their chosen program.",
            ],

            "requirements": [
                "Academic transcript.",
                "Curriculum vitae.",
                "Personal statement.",
                "Two recommendation letters.",
                "Proof of admission or application.",
            ],

            "application_url": (
                "https://example.test/opportunities/global-future-scholars"
            ),

            "source_url": (
                "https://example.test/scholarships/global-future-scholars"
            ),

            "source_name": "FutureBridge Foundation",

            "status": OpportunityStatus.DRAFT,

            "extras": {
                "funding": "Fully funded",
                "study_levels": [
                    "Undergraduate",
                    "Postgraduate",
                ],
                "fields_of_study": [
                    "Computer Science",
                    "Engineering",
                    "Business",
                    "Economics",
                    "Public Policy",
                ],
                "benefits": [
                    "Tuition",
                    "Living allowance",
                    "Mentorship",
                    "Career development",
                ],
            },
        },


        # =========================================================
        # 3. INTERNSHIP
        # =========================================================
        {
            "title": "Digital Innovation Internship",
            "slug": "digital-innovation-internship",

            "slug_list": [
                # -------------------------------------------------
                # Canonical / title variations
                # -------------------------------------------------
                "digital-innovation-internship",
                "digital-innovation",
                "innovation-internship",
                "digital-internship",
                "technology-internship",
                "tech-internship",
                "digital-innovation-internship-opportunity",
                "digital-innovation-program",
                "innovation-internship-program",

                # -------------------------------------------------
                # Opportunity type
                # -------------------------------------------------
                "internship",
                "internships",
                "intern",
                "intern-program",
                "internship-program",
                "student-internship",
                "graduate-internship",
                "summer-internship",
                "professional-internship",
                "work-placement",

                # -------------------------------------------------
                # Category
                # -------------------------------------------------
                "technology",
                "tech",
                "information-technology",
                "it",
                "software",
                "software-development",
                "digital",
                "digital-innovation",
                "innovation",
                "computer-science",
                "cs",
                "ict",
                "development",
                "digital-development",

                # -------------------------------------------------
                # Fields of study
                # -------------------------------------------------
                "computer-science",
                "cs",
                "economics",
                "statistics",
                "public-administration",
                "information-technology",
                "software-engineering",
                "data-analysis",
                "data-science",
                "technology-development",

                # -------------------------------------------------
                # Organization
                # -------------------------------------------------
                "global-development-lab",
                "global-development",
                "development-lab",

                # -------------------------------------------------
                # Country
                # -------------------------------------------------
                "bahamas",
                "the-bahamas",
                "bs",
                "bhs",

                # -------------------------------------------------
                # City / location
                # -------------------------------------------------
                "nassau",
                "nassau-bahamas",
                "nassau-bs",

                # -------------------------------------------------
                # Education
                # -------------------------------------------------
                "undergraduate",
                "undergraduate-internship",
                "university-student",
                "college-student",
                "student",
                "students",

                # -------------------------------------------------
                # Languages
                # -------------------------------------------------
                "english",
                "spanish",

                # -------------------------------------------------
                # Internship duration / schedule
                # -------------------------------------------------
                "5-month-internship",
                "5-months",
                "5.5-month-internship",
                "40-hours",
                "full-time-internship",
                "full-time",
            ],

            "type": OpportunityType.INTERNSHIP,
            "category": "technology",

            "organization": "Global Development Lab",

            "country": "Bahamas",
            "city": "Nassau",
            "location": "Nassau, Bahamas",
            "remote": False,

            "deadline": None,
            "start_date": None,
            "end_date": None,

            "summary": [
                "Global Development Lab is offering a digital innovation "
                "internship for students interested in technology and development.",
                "The internship provides practical experience working on "
                "digital solutions for real-world development challenges."
            ],

            "description": [
                {
                    "heading": "About the internship",
                    "content": (
                        "Interns will work alongside technical and development "
                        "teams to research, prototype, and support digital "
                        "solutions."
                    ),
                },
                {
                    "heading": "Internship activities",
                    "items": [
                        "Support software and digital product development.",
                        "Conduct research and data analysis.",
                        "Assist with technical documentation.",
                        "Participate in team meetings.",
                        "Support testing and evaluation of digital solutions.",
                    ],
                },
            ],

            "eligibility": [
                "Applicants must be currently enrolled in an undergraduate program.",
                "Applicants must have completed at least 50% of their coursework.",
                "Applicants must be citizens or legal residents of eligible countries.",
                "Applicants must be available for the full internship period.",
            ],

            "requirements": [
                "Resume.",
                "Cover letter.",
                "Academic transcript.",
                "University confirmation letter.",
            ],

            "application_url": (
                "https://example.test/opportunities/digital-innovation-internship"
            ),

            "source_url": (
                "https://example.test/internships/digital-innovation"
            ),

            "source_name": "Global Development Lab",

            "status": OpportunityStatus.DRAFT,

            "extras": {
                "contract_type": "Internship",
                "contract_length": "5.5 months",
                "weekly_hours": 40,
                "languages": [
                    "English",
                    "Spanish",
                ],
                "education_level": "Undergraduate",
                "fields_of_study": [
                    "Computer Science",
                    "Economics",
                    "Statistics",
                    "Public Administration",
                ],
                "documents_required": [
                    "Resume",
                    "Cover Letter",
                    "Academic Transcript",
                    "University Letter",
                ],
                "minimum_coursework_completed": "50%",
            },
        },


        # =========================================================
        # 4. COMPETITION
        # =========================================================
        {
            "title": "Future Impact Innovation Challenge 2026",
            "slug": "future-impact-innovation-challenge-2026",

            "slug_list": [
                # -------------------------------------------------
                # Canonical / title variations
                # -------------------------------------------------
                "future-impact-innovation-challenge-2026",
                "future-impact-innovation-challenge",
                "future-impact-challenge-2026",
                "future-impact-challenge",
                "innovation-challenge-2026",
                "innovation-challenge",
                "impact-innovation-challenge",
                "future-innovation-challenge",
                "future-impact-competition",
                "innovation-competition-2026",

                # -------------------------------------------------
                # Opportunity type
                # -------------------------------------------------
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
                "entrepreneurship-competition",
                "business-competition",
                "pitch-competition",
                "hackathon",

                # -------------------------------------------------
                # Category
                # -------------------------------------------------
                "entrepreneurship",
                "entrepreneur",
                "startup",
                "startups",
                "innovation",
                "technology",
                "tech",
                "social-innovation",
                "social-impact",
                "environment",
                "environmental",
                "sustainability",
                "development",
                "economic-development",
                "social-development",

                # -------------------------------------------------
                # Impact areas
                # -------------------------------------------------
                "social-impact",
                "environmental-impact",
                "climate",
                "climate-change",
                "sustainable-development",
                "sustainability",
                "community-development",
                "economic-impact",
                "technology-solutions",

                # -------------------------------------------------
                # Organization
                # -------------------------------------------------
                "impactworks-network",
                "impactworks",
                "impact-works",

                # -------------------------------------------------
                # Location
                # -------------------------------------------------
                "online",
                "online-competition",
                "online-challenge",
                "virtual",
                "virtual-competition",
                "virtual-challenge",
                "worldwide",
                "global",
                "international",

                # -------------------------------------------------
                # Eligibility
                # -------------------------------------------------
                "young-innovators",
                "young-entrepreneurs",
                "youth",
                "youth-competition",
                "young-people",
                "18-30",
                "18-to-30",
                "ages-18-30",
                "individual",
                "individuals",
                "teams",
                "team",

                # -------------------------------------------------
                # Team size
                # -------------------------------------------------
                "team-size-1-5",
                "teams-of-5",
                "1-5-members",

                # -------------------------------------------------
                # Prize / awards
                # -------------------------------------------------
                "prize",
                "cash-prize",
                "10000-usd",
                "10k-usd",
                "funding",
                "mentorship",
                "networking",
                "recognition",
                "project-exposure",
                "awards",

                # -------------------------------------------------
                # Fee
                # -------------------------------------------------
                "free-entry",
                "free-registration",
                "no-registration-fee",
                "no-fee",
                "free-to-enter",

                # -------------------------------------------------
                # Year
                # -------------------------------------------------
                "2026",
                "2026-challenge",
                "2026-competition",
            ],

            "type": OpportunityType.COMPETITION,
            "category": "entrepreneurship",

            "organization": "ImpactWorks Network",

            "country": None,
            "city": None,
            "location": "Online",
            "remote": True,

            "deadline": None,
            "start_date": None,
            "end_date": None,

            "summary": [
                "The Future Impact Innovation Challenge invites young innovators "
                "to develop solutions to major social and environmental challenges.",
                "Participants compete for funding, mentorship, and recognition."
            ],

            "description": [
                {
                    "heading": "About the competition",
                    "content": (
                        "Participants are invited to submit innovative ideas, "
                        "products, or projects that address a meaningful social, "
                        "economic, technological, or environmental challenge."
                    ),
                },
                {
                    "heading": "Competition stages",
                    "items": [
                        "Online registration.",
                        "Project submission.",
                        "Initial judging.",
                        "Finalist presentations.",
                        "Final evaluation and awards.",
                    ],
                },
            ],

            "eligibility": [
                "Applicants must be between 18 and 30 years old.",
                "Individuals and teams are eligible to participate.",
                "Participants may apply from any eligible country.",
                "Submitted projects must address a clearly defined problem.",
            ],

            "requirements": [
                "Complete the online registration form.",
                "Submit a project description.",
                "Provide a short project presentation.",
                "Explain the expected impact of the proposed solution.",
            ],

            "application_url": (
                "https://example.test/opportunities/future-impact-challenge"
            ),

            "source_url": (
                "https://example.test/competitions/future-impact-challenge-2026"
            ),

            "source_name": "ImpactWorks Network",

            "status": OpportunityStatus.DRAFT,

            "extras": {
                "prize": {
                    "amount": 10000,
                    "currency": "USD",
                },
                "eligibility_age": {
                    "minimum": 18,
                    "maximum": 30,
                },
                "team_size": {
                    "minimum": 1,
                    "maximum": 5,
                },
                "registration_fee": {
                    "amount": 0,
                    "currency": "USD",
                },
                "submission_format": "Online",
                "awards": [
                    "Cash prize",
                    "Mentorship",
                    "Professional networking",
                    "Project exposure",
                ],
            },
        },

    )

    @classmethod
    async def seed(
        cls,
        db: AsyncSession,
    ):

        result = await db.execute(
            select(Opportunity).where(
                Opportunity.source_url.in_(
                    [
                        opportunity["source_url"]
                        for opportunity
                        in cls.DEFAULT_OPPORTUNITIES
                    ]
                )
            )
        )

        existing_opportunities = {
            opportunity.source_url: opportunity
            for opportunity in result.scalars().all()
        }

        opportunities = {}

        for data in cls.DEFAULT_OPPORTUNITIES:

            opportunity = existing_opportunities.get(
                data["source_url"]
            )

            if opportunity is None:

                opportunity = Opportunity(
                    title=data["title"],
                    slug=data["slug"],
                    slug_list=data["slug_list"],
                    type=data["type"],
                    category=data["category"],

                    organization=data["organization"],

                    country=data["country"],
                    city=data["city"],
                    location=data["location"],
                    remote=data["remote"],

                    deadline=data["deadline"],
                    start_date=data["start_date"],
                    end_date=data["end_date"],

                    summary=data["summary"],
                    description=data["description"],
                    eligibility=data["eligibility"],
                    requirements=data["requirements"],

                    application_url=data["application_url"],

                    source_url=data["source_url"],
                    source_name=data["source_name"],

                    status=data["status"],
                    extras=data["extras"],
                )

                db.add(opportunity)

            else:

                opportunity.title = data["title"]
                opportunity.slug = data["slug"]
                opportunity.type = data["type"]
                opportunity.category = data["category"]

                opportunity.organization = data["organization"]

                opportunity.country = data["country"]
                opportunity.city = data["city"]
                opportunity.location = data["location"]
                opportunity.remote = data["remote"]

                opportunity.deadline = data["deadline"]
                opportunity.start_date = data["start_date"]
                opportunity.end_date = data["end_date"]

                opportunity.summary = data["summary"]
                opportunity.description = data["description"]
                opportunity.eligibility = data["eligibility"]
                opportunity.requirements = data["requirements"]

                opportunity.application_url = data["application_url"]

                opportunity.source_name = data["source_name"]

                opportunity.status = data["status"]
                opportunity.extras = data["extras"]

            opportunities[data["slug"]] = opportunity

        await db.flush()

        return opportunities