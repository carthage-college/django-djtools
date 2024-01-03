import django
import requests

django.setup()

from django.conf import settings

cid=666
earl = '{0}/student/{1}/detail/'.format(settings.DIRECTORY_API_URL, cid)
HEADERS = {'Authorization': 'Token {0}'.format(settings.REST_FRAMEWORK_TOKEN)}
response = requests.get(earl, headers=HEADERS)
profile = response.json()
print(profile)
profile = profile[0]
majors = ', '.join(
    list(filter(None, [
        profile.get('Primary_Major', ''),
        profile.get('Second_Major', ''),
        profile.get('Third_Major', ''),
    ]))
)
print(majors)
minors = ', '.join(
    list(filter(None,[
        profile.get('Minor_One', ''),
        profile.get('Minor_Two', ''),
        profile.get('Minor_Three', ''),
    ]))
)
print(minors)
