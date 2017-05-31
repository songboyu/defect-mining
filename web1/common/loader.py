# -- coding: utf-8--
import web.settings
from web import mining
APPS = web.settings.APPS

def load_url_handlers():
    return mining.url_handlers


