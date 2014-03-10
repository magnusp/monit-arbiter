# -*- coding: utf-8 -*-

__author__ = 'Magnus Persson'
__version__ = "1.0.0"

import os
import treq

from klein import route, resource
from twisted.web import static
from twisted.python import log
from twisted.internet import defer
from lxml import objectify

_monithosts = set(['http://10.0.1.16:2812'])


def get_assets_path(*path):
    base = os.sep.join([os.path.dirname(os.path.abspath(__file__)), 'assets'])
    return os.path.join(base, *path)


@route('/meta')
@defer.inlineCallbacks
def slask(request):
    stuff = []
    try:
        requests = yield defer.DeferredList(
            [treq.get('%s/_status?format=xml' % host, auth=('admin', 'monit')) for host in list(_monithosts)])
        bodies = yield defer.DeferredList([treq.content(r) for success, r in requests])
        for success, body in bodies:
            root = objectify.fromstring(body)
            stuff.append(root.server.localhostname.text)
        defer.returnValue("\n".join(stuff))
    except Exception as err:
        log.msg(err)
        defer.returnValue('Error')


@route('/assets', branch=True)
def assets(request):
    return static.File(get_assets_path())


@route('/')
def bootstrap(request):
    f = static.File(get_assets_path('html'))
    f.indexNames = ['bootstrap.html']
    return f

