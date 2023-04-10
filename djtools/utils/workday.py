# -*- coding: utf-8 -*-

import requests
from django.conf import settings
from django.core.cache import cache


def department_detail(did):
    """Fetch a department from the API based on department ID."""
    dept = []
    response = requests.get(
        '{0}department/{1}/?format=json'.format(
            settings.DIRECTORY_API_URL,
            did,
        ),
        headers={'Authorization': settings.REST_FRAMEWORK_TOKEN},
    )
    if response.json():
        dept = response.json()[0]
    return dept


def department_all(choices=False):
    """Obtain all departments and return a choices structure for forms."""
    if choices:
        depts = [('','---select---')]
    else:
        depts = []
    response = requests.get(
        '{0}department/?format=json'.format(
            settings.DIRECTORY_API_URL,
        ),
        headers={'Authorization': settings.REST_FRAMEWORK_TOKEN},
    )
    if response.json():
        for dept in response.json():
            if choices:
                depts.append((dept['id'], dept['name']))
            else:
                depts.append(dept)
    return depts


def department_person(cid, choices=False):
    """Returns all departments to which a person belongs."""
    if choices:
        depts = [('','---select---')]
    else:
        depts = []
    response = requests.get(
        '{0}profile/{1}/detail/?format=json'.format(
            settings.DIRECTORY_API_URL,
            cid,
        ),
        headers={'Authorization': settings.REST_FRAMEWORK_TOKEN},
    )
    if response.json():
        for dept in response.json()[0]['departments']:
            department = department_detail(dept['id'])
            if department:
                if choices:
                    depts.append((dept.id, dept.name))
                else:
                    depts.append(department)
    return depts


def get_peeps(who=None, choices=False):
    """Obtain the folks based on who parameter."""
    key = 'workday_{0}{1}_api'.format(who, choices)
    peeps = cache.get(key)
    if not peeps:
        peeps = []
        if choices:
            peeps.append(('','---select---'))
        if who:
            earl = '{0}profile/{1}/who/?format=json'.format(
                settings.DIRECTORY_API_URL,
                who,
            )
        else:
            earl = '{0}profile/?format=json'.format(
                settings.DIRECTORY_API_URL,
            )
        response = requests.get(
            earl,
            headers={'Authorization': settings.REST_FRAMEWORK_TOKEN},
        )
        if response.json():
            for peep in response.json():
                name = '{0}, {1}'.format(peep['last_name'], peep['first_name'])
                if choices:
                    peeps.append((peep.id, name))
                else:
                    peeps.append(peep)
                peeps.append(row)
            cache.set(key, peeps, timeout=86400)

    return peeps
