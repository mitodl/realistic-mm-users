from utils import load_json_from_file
from path import (
    FIELDS_OF_STUDY_PATH,
    US_STATE_CODE_MAP,
    CANADA_STATE_CODE_MAP,
    SPAIN_STATE_CODE_MAP,
)

USERS_TO_GENERATE = 120
# Percentage of users to be enrolled in at least one course.
# Users will be divided evenly among the fake programs.
PCT_USERS_ENROLLED = 0.9

# Course settings
PAST_COURSE_RUNS_TO_CREATE = 3
COURSE_RUN_MONTH_RANGES = [(1, 5), (8, 12)]
COURSE_DAY = 15
ENROLLMENT_DELTA = dict(days=14)
UPGRADE_DELTA = dict(days=7)

FIELDS_OF_STUDY = load_json_from_file(FIELDS_OF_STUDY_PATH)
DEGREES = {
    'MASTERS': {
        'name': 'm',
        'school_suffix': 'University',
        'grad_age': 30
    },
    'BACHELORS': {
        'name': 'b',
        'school_suffix': 'University',
        'grad_age': 22
    },
    'HIGH_SCHOOL': {
        'name': 'hs',
        'school_suffix': 'High School',
        'grad_age': 18
    }
}
GRAD_AGES = [degree_info['grad_age'] for degree_info in DEGREES.values()]
MIN_AGE = 18

EMPLOYMENT = {
    "Computer Software": {
        'company_name': ['Google', 'Microsoft', 'Apple'],
        'position': ['Software Engineer', 'DevOps']
    },
    "Banking": {
        'company_name': ['TD Bank', 'Chase', 'Bank of America', 'Fidelity'],
        'position': ['Branch Manager', 'Teller']
    },
    "Financial Services": {
        'company_name': ['Goldman Sachs', 'Berkshire Hathaway', 'Vanguard'],
        'position': ['Financial Analyst', 'Fund Manager']
    },
    "Automotive": {
        'company_name': ['Ford', 'Toyota', 'Hyundai', 'Audi', 'Volvo'],
        'position': ['Mechanic', 'Salesperson']
    }
}
EMPLOYMENT_YEAR_LENGTH = 2

COUNTRY_STATE_CODE_MAP = {
    'US': load_json_from_file(US_STATE_CODE_MAP),
    'CA': load_json_from_file(CANADA_STATE_CODE_MAP),
    'ES': load_json_from_file(SPAIN_STATE_CODE_MAP)
}

COPY_TO_FIELDS = [
    ('country', 'nationality'),
    ('country', 'birth_country'),
    ('first_name', 'preferred_name'),
    ('first_name', 'edx_name')
]
