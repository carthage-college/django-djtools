# -*- coding: utf-8 -*-

import requests
from django.conf import settings


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
        '{0}profile/{1}/departments/?format=json'.format(
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


def get_peeps(who):
    """Obtain the folks based on who parameter."""
    key = 'workday_{0}_api'.format(who)
    peeps = cache.get(key)

    if not peeps:

        if who == 'facstaff':
            where = 'faculty IS NOT NULL OR staff IS NOT NULL'
        elif who in ['faculty','staff','student']:
            where = '{0} IS NOT NULL'.format(who)
        else:
            where = None

        objects = xsql(sql, key=settings.INFORMIX_DEBUG)

        if objects:
            peeps = []
            for obj in objects:
                row = {
                    'cid': obj[0],
                    'lastname': obj[1],
                    'firstname': obj[2],
                    'email': '{0}@carthage.edu'.format(obj[3]),
                    'username': obj[3],
                }
                peeps.append(row)
            cache.set(key, peeps, timeout=86400)

    return peeps
