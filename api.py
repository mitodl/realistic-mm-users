from datetime import datetime, timedelta
from random import random, shuffle, randint
import copy

from utils import (
    load_json_from_file,
    year_diff,
    increment_year,
    parse_iso_datetime,
    random_item_from_iterable,
    random_key,
    random_n_up_to_limit,
    incrementally_split_list,
    random_iterable_index_range,
)
from randomuser_client import parse_randomuser_data
from settings import (
    COURSE_YEARS_TO_FILL_IN,
    COURSE_RUN_MONTH_RANGES,
    COURSE_DAY,
    ENROLLMENT_DELTA,
    UPGRADE_DELTA,
    FIELDS_OF_STUDY,
    DEGREES,
    EMPLOYMENT,
    EMPLOYMENT_YEAR_LENGTH,
    COUNTRY_STATE_CODE_MAP,
    COPY_TO_FIELDS,
)
from path import BASE_PROGRAM_DATA_PATH

NOW = datetime.now()


def generate_edx_key(course_title, course_start_date):
    return 'course-v1:MITx+{}+{}'.format(course_title.replace(' ', '+'), course_start_date.strftime('%b_%Y'))


def create_course_run(course_data, start_date, end_date):
    return {
        'title': '{} - {}'.format(course_data['title'], start_date.strftime('%B %Y')),
        'edx_course_key': generate_edx_key(course_data['title'], start_date),
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'enrollment_start': start_date.isoformat(),
        'enrollment_end': (start_date + timedelta(**ENROLLMENT_DELTA)).isoformat(),
        'upgrade_deadline': (start_date + timedelta(**UPGRADE_DELTA)).isoformat(),
    }


def create_course_runs(course_data):
    course_runs = []
    for i in reversed(range(COURSE_YEARS_TO_FILL_IN)):
        course_run_year = NOW.year - i
        for month_range in COURSE_RUN_MONTH_RANGES:
            start_date = datetime(year=course_run_year, month=month_range[0], day=COURSE_DAY)
            end_date = datetime(year=course_run_year, month=month_range[1], day=COURSE_DAY)
            if start_date < NOW:
                course_runs.append(create_course_run(course_data, start_date, end_date))
    return course_runs


### Profile data generation functions

def create_education_record(user, dob, degree_info):
    education_record = {
        'degree_name': degree_info['name'],
        'graduation_date': increment_year(dob, degree_info['grad_age']).date().isoformat(),
        'school_name': u'{} {}'.format(user['city'], degree_info['school_suffix']),
        'school_city': user['city'],
        'school_state_or_territory': user['state_or_territory'],
        'school_country': user['country'],
    }
    if degree_info['name'] != 'High school':
        education_record['field_of_study'] = random_key(FIELDS_OF_STUDY)
    return education_record


def create_education_records(user):
    education_records = []
    dob = parse_iso_datetime(user['date_of_birth'])
    years_old = year_diff(dob, NOW)
    for degree_info in DEGREES.values():
        if years_old >= degree_info['grad_age']:
            education_records.append(create_education_record(user, dob, degree_info))
    return education_records


def create_employment_record(user):
    employment_industry = random_key(EMPLOYMENT)
    return {
        'city': user['city'],
        'country': user['country'],
        'state_or_territory': user['state_or_territory'],
        'industry': employment_industry,
        'company_name': random_item_from_iterable(EMPLOYMENT[employment_industry]['company_name']),
    }


def create_employment_records(user):
    employment_records = []
    base_employment_record = create_employment_record(user)
    rand = random()
    employment_count = 1 if rand <= 0.5 else 2
    for i in range(employment_count):
        employment_record = copy.copy(base_employment_record)
        employment_industry = employment_record['industry']
        employment_record['position'] = EMPLOYMENT[employment_industry]['position'][i]
        # Set employment date ranges to be X years long; if this is the first record,
        #   don't set an end date (which will make it a current employment)
        employment_record['start_date'] = increment_year(NOW, -EMPLOYMENT_YEAR_LENGTH * (i + 1)).date().isoformat()
        if i > 0:
            employment_record['end_date'] = increment_year(NOW, -EMPLOYMENT_YEAR_LENGTH * i).date().isoformat()
        employment_records.append(employment_record)
    return employment_records


def create_user_from_result(user):
    user = parse_randomuser_data(user, NOW)
    for copy_tuple in COPY_TO_FIELDS:
        user[copy_tuple[1]] = user[copy_tuple[0]]
    user['education'] = create_education_records(user)
    user['work_history'] = create_employment_records(user)
    return user


### Enrollment/Certificate generation functions

def create_enrollment(course_data, course_run_index):
    course_run = course_data['course_runs'][course_run_index]
    return {
        "edx_course_key": course_run['edx_course_key']
    }


def create_grade(course_data, course_run_index, grade_range=(60, 100)):
    course_run = course_data['course_runs'][course_run_index]
    return {
        "edx_course_key": course_run['edx_course_key'],
        "grade": "{0:.2f}".format(randint(*grade_range) / 100)
    }


def create_edx_data_set(courses_data, num_enrollments=0, num_grades=None):
    course_run_index_range = random_iterable_index_range(courses_data[0]['course_runs'], num_enrollments)
    course_indices = range(*course_run_index_range)
    num_grades = num_grades or num_enrollments
    return {
        'enrollments': [
            create_enrollment(course_data, course_indices[i])
            for i, course_data in enumerate(courses_data[0:num_enrollments])
        ],
        'grades': [
            create_grade(course_data, course_indices[i])
            for i, course_data in enumerate(courses_data[0:num_grades])
        ]
    }


def create_n_enrollments_with_grades(all_program_data, num_courses_to_enroll=1):
    program_data = random_item_from_iterable(all_program_data)
    return create_edx_data_set(program_data['courses'], num_enrollments=num_courses_to_enroll)


### Program and user JSON file generation functions

def build_full_program_data():
    program_data = load_json_from_file(BASE_PROGRAM_DATA_PATH)
    for program_index in range(len(program_data)):
        for course_data in program_data[program_index]['courses']:
            course_data['course_runs'] = create_course_runs(course_data)
    return program_data


def edit_full_user_data(all_user_data):
    """
    Makes changes to user data after API results are parsed and the user data is in the correct format
    """
    user_count = len(all_user_data)

    # Change set of users to have a nationality different from their current country
    group_indices = random_n_up_to_limit(int(user_count * 0.1), user_count)
    for i in group_indices:
        user_data = all_user_data[i]
        country = user_data['country']
        new_country = random_item_from_iterable([
            k for k in COUNTRY_STATE_CODE_MAP.keys() if k != country
        ])
        user_from_new_country = random_item_from_iterable([
            data for data in all_user_data if
            data['country'] == new_country
        ])
        user_data.update({
            'country': user_from_new_country['country'],
            'state_or_territory': user_from_new_country['state_or_territory'],
            'city': user_from_new_country['city']
        })
        all_user_data[i] = user_data

    return all_user_data


def fill_in_cached_edx_data(all_user_data, all_program_data):
    user_count = len(all_user_data)
    indices = list(range(0, user_count))
    shuffle(indices)

    ### Users w/ 2 courses, enrollment/grade in each
    (group_indices, indices) = incrementally_split_list(indices, 0.4, user_count)
    for i in group_indices:
        all_user_data[i].update(create_n_enrollments_with_grades(all_program_data, num_courses_to_enroll=2))

    ### Users w/ 1 courses & enrollment/grade
    (group_indices, indices) = incrementally_split_list(indices, 0.2, user_count)
    for i in group_indices:
        all_user_data[i].update(create_n_enrollments_with_grades(all_program_data, num_courses_to_enroll=1))

    ### Users w/ 3 courses, enrollment/grade in each
    (group_indices, indices) = incrementally_split_list(indices, 0.1, user_count)
    for i in group_indices:
        all_user_data[i].update(create_n_enrollments_with_grades(all_program_data, num_courses_to_enroll=3))

    ### Users w/ 2 courses, enrollment in each, grade in one
    (group_indices, indices) = incrementally_split_list(indices, 0.1, user_count)
    for i in group_indices:
        program_data = random_item_from_iterable(all_program_data)
        # user_data = all_user_data[i]
        course_data = program_data['courses'][0]
        # Same course, 2 different course runs
        enrollments = [
            create_enrollment(course_data, 0),
            create_enrollment(course_data, 1)
        ]
        grades = [create_grade(course_data, 1)]
        all_user_data[i]['enrollments'] = enrollments
        all_user_data[i]['grades'] = grades

    ### Users with 2 courses across 2 programs, enrollment/grade in each
    (group_indices, indices) = incrementally_split_list(indices, 0.1, user_count)
    program_index_range = random_iterable_index_range(all_program_data, 2)
    selected_program_data = [all_program_data[i] for i in range(*program_index_range)]
    for i in group_indices:
        user_edx_data = {'enrollments': [], 'grades': []}
        for program_data in selected_program_data:
            new_edx_data = create_edx_data_set(program_data['courses'], num_enrollments=1)
            user_edx_data['enrollments'] += new_edx_data['enrollments']
            user_edx_data['grades'] += new_edx_data['grades']
        all_user_data[i].update(user_edx_data)

    return all_user_data
