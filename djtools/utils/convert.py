import importlib


def str_to_class(module_name, class_name):
    try:
        # load the module, will raise ImportError if module cannot be loaded
        m = importlib.import_module(module_name)
        # get the class, will raise AttributeError if class cannot be found
        c = getattr(m, class_name)
    except:
        c = None
    return c

