from optparse import OptionParser
import sys, os

from django.core.serializers import serialize

#set up command-line options

parser = OptionParser()
parser.add_option("-s", "--settings", help="project settings file e.g. djforms.settings", dest="settings")
parser.add_option("-a", "--app", help="name of the application in your project e.g. djforms.core.models", dest="app_mod")
parser.add_option("-m", "--model_name", help="name of the model you want to export e.g. Page", dest="model_name")

if __name__ == '__main__':
    (options, args) = parser.parse_args()
    os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
    mod = __import__(options.app_mod, {}, {}, ['models'])
    model_name = options.model_name
    cls = getattr(mod, model_name)
    filename = model_name.lower() + ".json"
    file = open(filename, "w")
    file.write(serialize("json", cls.objects.all()))

