from django.conf import settings

from factory.django import DjangoModelFactory
from faker import Factory

import random

faker = Factory.create('en_US')


class TestUserFactory(DjangoModelFactory):
    class Meta:
        # Equivalent to model = 'django.contrib.auth.models.User'
        model = 'auth.User'
        #django_get_or_create = ('username',)

    username = settings.TEST_USER_USERNAME
    password = settings.TEST_USER_PASSWORD
    id = settings.TEST_USER_ID
    last_name = settings.TEST_USER_LASTNAME
    first_name = settings.TEST_USER_FIRSTNAME


class RandomUserFactory(DjangoModelFactory):
    class Meta:
        model = 'auth.User'

    username = faker.user_name()
    email = faker.email()
    password = faker.password(32)
    last_name = faker.last_name()
    first_name = faker.first_name()
    id = random.randint(1500000, 1600000)
