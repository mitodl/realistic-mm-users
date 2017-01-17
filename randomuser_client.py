import requests
from datetime import datetime
from utils import (
    date_from_randomuser_dob,
    increment_year,
    year_diff,
    case_insensitive_lookup,
    random_item_from_iterable,
    list_product
)
from settings import (
    USERS_TO_GENERATE,
    COUNTRY_STATE_CODE_MAP,
    GRAD_AGES,
    MIN_AGE,
)


RANDOMUSER_URL='https://randomuser.me/api/'
USER_GROUP_PARAMS = {
    'nat': ['us', 'ca', 'es'],
    'gender': ['female', 'male']
}
USER_GROUP_SORTING = {
    'nat': 0,
    'gender': 1
}
PREFERRED_LANG_MAP = {
    'nat=us': 'en',
    'nat=ca': 'en',
    'nat=es': 'sp'
}


def determine_user_count_per_group():
    """Calculates the number of users that should be generated for each group"""
    return int(
        USERS_TO_GENERATE/
        len(list_product(USER_GROUP_PARAMS.values()))
    )


def create_param_groups():
    """Produces combinations of randomuser.me params that we want"""
    querystrung_group_params = []
    # Sort the API group params. This is just here to ensure the API requests are called in a predictable order.
    group_params = sorted(USER_GROUP_PARAMS.items(), key=lambda t: USER_GROUP_SORTING.get(t[0], None))
    for param_name, value_list in group_params:
        querystrung_group_params.append(['{}={}'.format(param_name, value) for value in value_list])
    return list_product(querystrung_group_params)


def api_param_iter(user_count_per_group):
    results_count_param = 'results={}'.format(user_count_per_group)
    for api_param_group in create_param_groups():
        # nationality_param = filter(lambda param: 'nat=' in param, api_param_group)[0]
        # preferred_lang_param = PREFERRED_LANG_MAP[nationality_param]
        yield '&'.join(api_param_group + (results_count_param, ))


def parse_gender(gender_value):
    return dict(
        male='m',
        female='f'
    )[gender_value]


def parse_randomuser_data(user, now=None):
    # TODO: profile pictures
    now = now or datetime.now()
    dob = date_from_randomuser_dob(user['dob'])
    if year_diff(dob, now) < MIN_AGE:
        # Coerce < 18 y/o users to be older. Randomly assign 18, 22, or 30 years old
        dob = increment_year(now, random_item_from_iterable([age * -1 for age in GRAD_AGES])).date()
    state_code_dict = COUNTRY_STATE_CODE_MAP[user['nat']]
    state_code = case_insensitive_lookup(state_code_dict, user['location']['state'])
    if not state_code:
        state_code = list(state_code_dict.values())[0]
    return {
        'first_name': user['name']['first'].title(),
        'last_name': user['name']['last'].title(),
        'date_of_birth': dob.isoformat(),
        'gender': parse_gender(user['gender']),
        'country': user['nat'],
        'state_or_territory': u'{}-{}'.format(user['nat'], state_code),
        'city': user['location']['city'].title(),
        'email': user['email']
    }


def get_all_user_api_results():
    user_count_per_group = determine_user_count_per_group()
    param_groups = api_param_iter(user_count_per_group)
    api_call_metadata = []
    user_results = []
    for params in param_groups:
        api_url = '{}?{}'.format(RANDOMUSER_URL, params)
        resp = requests.get(api_url)
        resp_json = resp.json()
        api_call_metadata.append({'url': api_url, 'seed': resp_json['info']['seed']})
        user_results += resp_json['results']
    return user_results, api_call_metadata
