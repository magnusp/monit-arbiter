from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application import internet
from twisted.application.service import IServiceMaker
from twisted.web import server
from monitarbiter import MonitArbiter


class Options(usage.Options):
    optParameters = [["port", "p", 8080, "The port number to listen on."]]


class ArbiterServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "monit-arbiter"
    description = "Centralized management of monit daemons"
    options = Options

    def makeService(self, options):
        m = MonitArbiter()
        return internet.TCPServer(int(options["port"]), server.Site(m.app.resource()))


serviceMaker = ArbiterServiceMaker()