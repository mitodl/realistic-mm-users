import os

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

RESULT_DIR_NAME = 'data'
RESULT_DIR = os.path.join(PACKAGE_DIR, RESULT_DIR_NAME)
BASE_PROGRAM_DATA_PATH = os.path.join(PACKAGE_DIR, 'settings/base_program_data.json')
RESULT_PROGRAM_DATA_PATH = os.path.join(RESULT_DIR, 'realistic_program_data.json')
USER_DATA_PATH = os.path.join(RESULT_DIR, 'realistic_user_data.json')
API_RESULT_DATA_PATH = os.path.join(RESULT_DIR, 'randomuser_results.json')
API_METADATA_PATH = os.path.join(RESULT_DIR, 'randomuser_results_metadata.json')

SETTINGS_DIR_NAME = 'settings'
SETTINGS_DIR = os.path.join(PACKAGE_DIR, SETTINGS_DIR_NAME)
FIELDS_OF_STUDY_PATH = os.path.join(SETTINGS_DIR, 'fields_of_study.json')
US_STATE_CODE_MAP = os.path.join(SETTINGS_DIR, 'us_states.json')
CANADA_STATE_CODE_MAP = os.path.join(SETTINGS_DIR, 'canada_states.json')
SPAIN_STATE_CODE_MAP = os.path.join(SETTINGS_DIR, 'spain_states.json')
