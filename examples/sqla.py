import time
import signal

from concurrent.futures import ThreadPoolExecutor

import sqlalchemy as sa
from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy import engine_from_config

import tornado.httpserver
import tornado.gen
import tornado.ioloop
import tornado.log
import tornado.options
import tornado.web

from tqueries import sqla
from tqueries.sqla.mixins import SqlalchemyRESTMixin

logger = tornado.log.app_log
tornado.options.define(u"port", default=8888, type=int)
tornado.options.define(u"host", default='', type=str)


# SETUP MODELS

Base = declarative_base()


class SuperModel(Base):
    __tablename__ = u'super_models'
    id = sa.Column(sa.Integer, primary_key=True)
    string_column = sa.Column(sa.String(512))


# Handlers that inherit from SqlalchemyRESTMixin
# have all get, post, etc methods setup to run in executor
# that comes from tornado.web.Application
# User has to override handle_<method>
class MainHandler(SqlalchemyRESTMixin):

    @tornado.gen.coroutine
    def get(self):
        # custom get
        response = yield self._handle(self.handle_get)
        self.set_status(202)
        self.write(response)

    def handle_get(self, session):
        logger.info(u'MainHandler: GET')
        time.sleep(1)
        count = session.query(SuperModel).count()
        time.sleep(1)
        return u"{0}".format(str(count))

    def handle_post(self, session):
        session.add(SuperModel(string_column=u'one'))
        logger.info(u'MainHandler: POST')
        return u"Created!"


class AnotherHandler(SqlalchemyRESTMixin):

    def handle_get(self, session):
        logger.info(u'AnotherHandler: GET')
        return u"Something"

    def handle_post(self, session):
        logger.info(u'AnotherHandler: POST')
        return u"Else"


class CustomApp(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/another', AnotherHandler)
        ]
        tornado.web.Application.__init__(self, handlers, debug=True)
        self._executor = ThreadPoolExecutor(max_workers=20)


def shutdown(server_instance):
    ioloop_instance = tornado.ioloop.IOLoop.instance()
    logger.info(u'Stopping App Gracefully.')

    server_instance.stop()

    def finalize():
        ioloop_instance.stop()
        logger.info(u'App stopped.')

    ioloop_instance.add_timeout(time.time() + 1.5, finalize)


def start_server():
    options = tornado.options.options
    options.parse_command_line()
    settings = {
        u'sqlalchemy.url': u'sqlite:////tmp/test.db'
    }
    engine = engine_from_config(settings, prefix=u'sqlalchemy.', echo=True)
    sqla.initialize_sessionmaker(engine=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    application_instance = CustomApp()
    http_server = tornado.httpserver.HTTPServer(application_instance)
    logger.info(u"Starting App on {0}:{1}.".format(
        options.host, options.port
    ))

    shutdown_handler = lambda sig, frame: shutdown(http_server)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    http_server.listen(options.port, options.host)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == u"__main__":
    start_server()
