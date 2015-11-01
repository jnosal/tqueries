import time
import signal
import contextlib

import tornado.ioloop
import tornado.log

from tqueries.sqla import get_session


logger = tornado.log.app_log


@contextlib.contextmanager
def session_manager():
    session = get_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def register_shutdown_handler(http_server, engine):
    shutdown_handler = lambda sig, frame: shutdown(http_server, engine)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)


def shutdown(server_instance, engine_instance):
    ioloop_instance = tornado.ioloop.IOLoop.instance()
    logger.info(u'Stopping App Gracefully.')

    engine_instance.dispose()
    server_instance.stop()

    def finalize():
        ioloop_instance.stop()
        logger.info(u'App stopped.')

    ioloop_instance.add_timeout(time.time() + 1.5, finalize)
