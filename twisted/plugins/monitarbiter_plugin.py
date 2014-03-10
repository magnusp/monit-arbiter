# -*- coding: utf-8 -*-

__author__ = 'Magnus Persson'
__version__ = "1.0.0"

from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application import internet
from twisted.application.service import IServiceMaker
from twisted.web import server

from monitarbiter import resource
from monitarbiter import _monithosts


class Options(usage.Options):
    optParameters = [["port", "p", 8080, "The port number to listen on."]]

    def __init__(self):
        usage.Options.__init__(self)

    def opt_monithost(self, monithost):
        _monithosts.add(monithost)

    opt_H = opt_monithost


class ArbiterServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "monit-arbiter"
    description = "Centralized management of monit daemons"
    options = Options

    def makeService(self, options):
        if not _monithosts:
            _monithosts.add('http://127.0.0.1:2812')
        factory = server.Site(resource())
        return internet.TCPServer(int(options["port"]), factory)


serviceMaker = ArbiterServiceMaker()