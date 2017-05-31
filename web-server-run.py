# -- coding: utf-8 --
import os
import sys
import signal
import time
import subprocess

import node
from tornado import ioloop
from tornado.options import options

from web.common.init import *
from web.common.loader import load_url_handlers
from web.logger import logger
from web.settings import *

class iApplication(web.Application):
    def __init__(self):
        settings = {
            'static': os.path.join(os.path.dirname(__file__), "web/static"),
            'template_path': os.path.join(os.path.dirname(__file__), "web/templates"),
        }
    
        handlers = [
            (r"^/$", MainHandler),
            (r"^/signin", MainHandler),
            (r"^/static/(.*)", web.StaticFileHandler, dict(path=settings['static'])),
        ]
        
        apps = load_url_handlers()
        handlers.extend(apps)
        # custom http error handler
        handlers.append((r"/.*", PageNotFound))
        web.Application.__init__(self, handlers, **settings)


class MainHandler(WiseHandler):
    def get(self):
        self.render("pages-signin.html")

class Watcher:
    def __init__(self):
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except (KeyboardInterrupt, SystemExit):
            # I put the capital B in KeyBoardInterrupt so I can
            # tell when the Watcher gets the SIGINT
            print "Server exit at %s." % time.ctime()
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass

if __name__ == '__main__':
    port = SERVER_API_PORT
    
    options.parse_command_line()
    # subprocess.Popen('ps -ef|grep celery|grep -v grep|cut -c 9-15|xargs kill -9', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    node.main()

    app = iApplication()
    app.listen(port, xheaders=True)
    logger.info("Start server on %d OK." % port)
    
    try:
        ioloop = ioloop.IOLoop.instance()
        ioloop.start()
    except (KeyboardInterrupt, SystemExit):
        ioloop.close()

