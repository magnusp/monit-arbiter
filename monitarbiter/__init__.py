__author__ = 'Magnus Persson'
__version__ = "1.0.0"

from klein import Klein


class MonitArbiter(object):
    app = Klein()

    @app.route('/')
    def hw(self, request):
        return "Hello"

    @app.route('/2')
    def h2(self, request):
        return "Hello2"
