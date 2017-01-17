import os
import argparse

from utils import (
    create_dir_if_none_exists,
    load_json_from_file,
    write_json_to_file,
)
from randomuser_client import get_all_user_api_results
from api import (
    build_full_program_data,
    create_user_from_result,
    edit_full_user_data,
    fill_in_edx_data
)
from path import (
    API_RESULT_DATA_PATH,
    API_METADATA_PATH,
    RESULT_PROGRAM_DATA_PATH,
    USER_DATA_PATH,
    RESULT_DIR,
    RESULT_DIR_NAME
)


def fetch_api_results(save=True):
    (api_result_data, api_call_metadata) = get_all_user_api_results()
    if save:
        write_json_to_file(api_result_data, API_RESULT_DATA_PATH)
        write_json_to_file(api_call_metadata, API_METADATA_PATH)
    return api_result_data


def generate_user_and_program_data(api_result_data):
    program_data = build_full_program_data()
    write_json_to_file(program_data, RESULT_PROGRAM_DATA_PATH)
    user_data = [create_user_from_result(user_result) for user_result in api_result_data]
    user_data = edit_full_user_data(user_data)
    user_data = fill_in_edx_data(user_data, program_data)
    write_json_to_file(user_data, USER_DATA_PATH)


parser = argparse.ArgumentParser(description='''
    Queries randomuser.me and generates realistic user and program data for use in Micromasters.

    Realistic user and program data will be saved as JSON. The script will also save metadata and results of
     requests to randomuser.me. Result JSON files will be saved in the '{}' directory.
'''.format(RESULT_DIR_NAME))
parser.add_argument('--create-from-api', action='store_true', help='Generate data from new randomuser.me API results')
parser.add_argument('--save-api-results', action='store_true', help='Save randomuser.me API results')

if __name__ == "__main__":
    args = parser.parse_args()
    create_dir_if_none_exists(RESULT_DIR)
    api_results_exist = os.path.isfile(API_RESULT_DATA_PATH)
    if not api_results_exist or args.create_from_api or args.save_api_results:
        # save results if the flag was set or if the results don't exist yet
        save_results = args.save_api_results or not api_results_exist
        api_results = fetch_api_results(save=save_results)
    else:
        api_results = load_json_from_file(API_RESULT_DATA_PATH)
    generate_user_and_program_data(api_results)
