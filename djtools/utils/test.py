from django.conf import settings
from django.contrib.auth.models import User


def create_test_user():

    # create the auth user
    user = User.objects.create_user(
        settings.TEST_USER_USERNAME,
        settings.TEST_USER_EMAIL,
        settings.TEST_USER_PASSWORD,
        id = settings.TEST_USER_ID,
        last_name = settings.TEST_USER_LASTNAME,
        first_name = settings.TEST_USER_FIRSTNAME
    )

    return user
