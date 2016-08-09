import os
from utils import load_json_from_file


PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
FIELDS_OF_STUDY_PATH = os.path.join(PACKAGE_DIR, 'fields_of_study.json')
US_STATE_CODE_MAP = os.path.join(PACKAGE_DIR, 'us_states.json')
CANADA_STATE_CODE_MAP = os.path.join(PACKAGE_DIR, 'canada_states.json')
SPAIN_STATE_CODE_MAP = os.path.join(PACKAGE_DIR, 'spain_states.json')


# Course settings
COURSE_YEARS_TO_FILL_IN = 2
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

# TODO: actual states? can just build json files for each country
COUNTRY_STATE_CODE_MAP = {
    'US': load_json_from_file(US_STATE_CODE_MAP),
    'CA': load_json_from_file(CANADA_STATE_CODE_MAP),
    'ES': load_json_from_file(SPAIN_STATE_CODE_MAP)
}

COPY_TO_FIELDS = [
    ('country', 'birth_country'),
    ('state_or_territory', 'birth_state_or_territory'),
    ('city', 'birth_city'),
    ('first_name', 'preferred_name'),
    ('first_name', 'edx_name')
]

STATIC_FIELDS = {
    'account_privacy': 'private',
    'edx_requires_parental_consent': False,
    'email_optin': True,
    'filled_out': True,
    'has_profile_image': False,
}