# -*- coding: utf-8 -*-
from twisted.internet.error import ConnectionRefusedError

__author__ = 'Magnus Persson'
__version__ = "1.0.0"

import os
import treq

from klein import route, resource
from twisted.web import static
from twisted.internet import defer

from lxml import objectify
import json

_monithosts = set()


class objectJSONEncoder(json.JSONEncoder):
    """A specialized JSON encoder that can handle simple lxml objectify types
    >>> from lxml import objectify
    >>> obj = objectify.fromstring("<Book><price>1.50</price><author>W. Shakespeare</author></Book>")
    >>> objectJSONEncoder().encode(obj)
    '{"price": 1.5, "author": "W. Shakespeare"}'
    """

    def default(self, o):
        if isinstance(o, objectify.IntElement):
            return int(o)
        if isinstance(o, objectify.NumberElement) or isinstance(o, objectify.FloatElement):
            return float(o)
        if isinstance(o, objectify.ObjectifiedDataElement):
            return str(o)
        if hasattr(o, '__dict__'):
            #For objects with a __dict__, return the encoding of the __dict__
            return o.__dict__
        return json.JSONEncoder.default(self, o)


def get_assets_path(*path):
    base = os.sep.join([os.path.dirname(os.path.abspath(__file__)), 'assets'])
    return os.path.join(base, *path)


@route('/meta')
@defer.inlineCallbacks
def slask(request):
    monits = []
    for host in list(_monithosts):
        try:
            monitrequest = yield treq.get('%s/_status?format=xml' % host, auth=('admin', 'monit'), timeout=0.5)
        except ConnectionRefusedError as err:
            continue
        body = yield treq.content(monitrequest)

        monits.append(objectify.fromstring(body))
    defer.returnValue(objectJSONEncoder().encode(monits))


@route('/assets', branch=True)
def assets(request):
    return static.File(get_assets_path())


@route('/')
def bootstrap(request):
    f = static.File(get_assets_path('html'))
    f.indexNames = ['bootstrap.html']
    return f

