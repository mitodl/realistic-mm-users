import requests
from datetime import datetime
from itertools import product
from collections import OrderedDict
from utils import (
    datetime_from_epoch,
    increment_year,
    year_diff,
    case_insensitive_lookup,
    random_item_from_iterable,
)
from settings import (
    COUNTRY_STATE_CODE_MAP,
    GRAD_AGES,
    MIN_AGE,
)


RANDOMUSER_URL='https://randomuser.me/api/'
USER_COUNT_PER_GROUP = 10
USER_GROUP_SORTING = {
    'nat': 0,
    'gender': 1
}
USER_GROUP_PARAMS = {
    'nat': ['us', 'ca', 'es'],
    'gender': ['female', 'male']
}

PREFERRED_LANG_MAP = {
    'nat=us': 'en',
    'nat=ca': 'en',
    'nat=es': 'sp'
}


def create_param_groups():
    """Produces combinations of randomuser.me params that we want"""
    querystrung_group_params = []
    # Sort the API group params. This is just here to ensure the API requests are called in a predictable order.
    group_params = sorted(USER_GROUP_PARAMS.items(), key=lambda t: USER_GROUP_SORTING.get(t[0], None))
    for param_name, value_list in group_params:
        querystrung_group_params.append(['{}={}'.format(param_name, value) for value in value_list])
    return list(product(*querystrung_group_params))


def api_param_iter():
    results_count_param = 'results={}'.format(USER_COUNT_PER_GROUP)
    for api_param_group in create_param_groups():
        nationality_param = filter(lambda param: 'nat=' in param, api_param_group)[0]
        preferred_lang_param = PREFERRED_LANG_MAP[nationality_param]
        yield '&'.join(api_param_group + (results_count_param, ))


def parse_gender(gender_value):
    return dict(
        male='m',
        female='f'
    )[gender_value]


def parse_randomuser_data(user, now=None):
    # TODO: profile pictures
    now = now or datetime.now()
    dob = datetime_from_epoch(user['dob']).date()
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
    param_groups = api_param_iter()
    api_call_metadata = []
    user_results = []
    for params in param_groups:
        api_url = '{}?{}'.format(RANDOMUSER_URL, params)
        resp = requests.get(api_url)
        resp_json = resp.json()
        api_call_metadata.append({'url': api_url, 'seed': resp_json['info']['seed']})
        user_results += resp_json['results']
    return user_results, api_call_metadata
