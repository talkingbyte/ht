import sys
from urllib import urlencode

base_url = sys.argv[0]

def fetch(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(base_url, urlencode(kwargs))
