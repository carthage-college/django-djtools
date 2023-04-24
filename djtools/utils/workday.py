# -*- coding: utf-8 -*-

import requests
from django.conf import settings
from django.core.cache import cache


HEADERS = {'Authorization': 'Token {0}'.format(settings.REST_FRAMEWORK_TOKEN)}


def department_detail(did):
    """Fetch a department from the API based on department ID."""
    dept = []
    response = requests.get(
        '{0}department/{1}/?format=json'.format(
            settings.DIRECTORY_API_URL,
            did,
        ),
        headers=HEADERS,
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
        headers=HEADERS,
    )
    if response.json():
        for dept in response.json():
            if choices:
                depts.append((str(dept['id']), dept['name']))
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
        headers=HEADERS,
    )
    if response.json():
        for dept in response.json()[0]['departments']:
            did = dept.split('/')[-2]
            department = department_detail(did)
            if department:
                if choices:
                    depts.append((department['id'], department['name']))
                else:
                    depts.append(department)
    return depts


def get_managers(manager, cid=False):
    """Obtain all managers."""
    peeps = []
    response = requests.get(
        '{0}profile/{1}/?format=json'.format(
            settings.DIRECTORY_API_URL,
            manager,
        ),
        headers=HEADERS,
    )
    if response.json():
        for person in response.json():
            if cid:
                if cid == person['id']:
                    return person
                else:
                    peeps = []
            else:
                peeps.append(person)
    return peeps


def get_peep(cid):
    """Obtain the profile based on ID."""
    key = 'workday_{0}_api'.format(cid)
    peep = cache.get(key)
    if not peep:
        earl = '{0}profile/{1}/detail/?format=json'.format(
            settings.DIRECTORY_API_URL,
            cid,
        )
        response = requests.get(earl, headers=HEADERS)
        if response.json():
            peep = response.json()
            cache.set(key, peep, timeout=86400)
    return peep


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
        response = requests.get(earl, headers=HEADERS)
        if response.json():
            for peep in response.json():
                name = '{0}, {1}'.format(peep['last_name'], peep['first_name'])
                if choices:
                    peeps.append((peep['id'], name))
                else:
                    peeps.append(peep)
            cache.set(key, peeps, timeout=86400)

    return peeps
