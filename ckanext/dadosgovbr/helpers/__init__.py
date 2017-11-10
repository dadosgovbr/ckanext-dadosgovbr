# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)

    # Import all helpers modules
    import os
    for module in os.listdir(os.path.dirname(__file__)):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        __import__(module[:-3], locals(), globals())
    del module
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)
