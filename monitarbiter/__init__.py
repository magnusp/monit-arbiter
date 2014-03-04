__author__ = 'Magnus Persson'
__version__ = "1.0.0"

import os

from klein import Klein
from twisted.web import static

from monitarbiter import assets


def get_assets_path(*path):
    return os.path.join(os.path.dirname(assets.__file__), *path)


class MonitArbiter(object):
    app = Klein()
    sessions = set()

    @app.route('/assets', branch=True)
    def assets(self, request):
        return static.File(get_assets_path())

    @app.route('/')
    def bootstrap(self, request):
        f = static.File(get_assets_path('html'))
        f.indexNames = ['bootstrap.html']
        return f
        #return static.File(get_assets_path('html\\bootstrap.html'))