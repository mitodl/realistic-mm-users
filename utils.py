import os
import json
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dateutil.parser
from random import randint


def load_json_from_file(path):
    with open(path, 'r') as f:
        data = json.loads(f.read())
    return data


def write_json_to_file(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def datetime_from_epoch(epoch_time):
    return datetime.fromtimestamp(epoch_time)


def year_diff(start_date, end_date):
    return relativedelta(end_date, start_date).years


def increment_year(date, years):
    return date.replace(year=date.year + years)


def parse_iso_datetime(iso):
    return dateutil.parser.parse(iso)


def random_item_from_iterable(iterable):
    return random.choice(iterable)


def random_index_from_iterable(iterable):
    return random.choice(range(len(iterable)))


def random_key(d):
    return random_item_from_iterable(list(d.keys()))


def random_n_up_to_limit(n, range_limit):
    return random.sample(range(range_limit), n)


def split_list(list_to_split, first_chunk_size):
    return list_to_split[0:first_chunk_size], list_to_split[first_chunk_size:]


def incrementally_split_list(remaining_list, percentage, original_list_size):
    return split_list(remaining_list, int(original_list_size * percentage))


def list_section(list_to_section, start_index, num_items):
    return list_to_section[start_index:start_index+num_items]


def random_iterable_index_range(iterable, num_items_desired):
    start_index = randint(0, len(iterable) - num_items_desired)
    return start_index, start_index + num_items_desired


def case_insensitive_lookup(d, key_to_find):
    try:
        key = next(k for k in d.keys() if key_to_find.lower() == k.lower())
        return d[key]
    except:
        return None


def filter_dict_keys(orig_dict, keys_to_keep):
    return {key: orig_dict[key] for key in keys_to_keep}


def create_dir_if_none_exists(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
