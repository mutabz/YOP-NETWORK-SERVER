class ScholarshipsAdsSelectors:
    """
    Source-specific HTML selectors and section identifiers
    for ScholarshipsAds.

    Parsing logic belongs in the parser.
    """

    # ------------------------------------------------------------------
    # Main page
    # ------------------------------------------------------------------

    TITLE = "h1"

    # ------------------------------------------------------------------
    # Scholarship card
    # ------------------------------------------------------------------

    CARD_INFO = ".card-info"

    CARD_ITEMS = ".card-info li"

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    APPLY_BUTTON = "a.js-apply-auth-trigger"

    # ------------------------------------------------------------------
    # Published information
    # ------------------------------------------------------------------

    PUBLISHED_DATE = ".published-info .text-muted"

    # ------------------------------------------------------------------
    # Section structure
    # ------------------------------------------------------------------

    # Keep this for individual h3 usage.
    SECTION_HEADING = "h3"

    # h2 and h3 are both structural sections on ScholarshipsAds.
    SECTION_HEADINGS = "h2, h3"

    # ------------------------------------------------------------------
    # Common section names
    # ------------------------------------------------------------------

    DEGREE_LEVEL = "Degree Level"

    AVAILABLE_SUBJECTS = "Available Subjects"

    BENEFITS = "Benefits"

    ELIGIBLE_NATIONALITIES = "Eligible Nationalities"

    ELIGIBILITY_CRITERIA = "Eligibility Criteria"

    APPLICATION_PROCEDURE = "Application Procedure"

    IMPORTANT_DEADLINES = "Important Application Deadlines"

    # ------------------------------------------------------------------
    # Dynamic / optional sections
    # ------------------------------------------------------------------

    FULLY_FUNDED = "fully funded"

    WHY_APPLY = "why apply"

    FINAL_THOUGHTS = "final thoughts"

    # ------------------------------------------------------------------
    # Application steps
    # ------------------------------------------------------------------

    APPLICATION_STEP_PREFIX = "step "