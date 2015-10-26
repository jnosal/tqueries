import logging

from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.pool import Pool
from sqlalchemy.orm import scoped_session, sessionmaker


class Meta:
    maker = None


class SessionNotInitializedException(Exception):
    """Session initialization Exeption"""


def initialize_sessionmaker(engine, *args, **kwargs):
    maker = scoped_session(sessionmaker(
        *args, **kwargs
    ))
    maker.configure(bind=engine)
    Meta.maker = maker


def get_session(**kwargs):
    if not Meta.maker:
        msg = u"Please initialize session/maker"
        raise SessionNotInitializedException(msg)

    return Meta.maker(**kwargs)


@event.listens_for(Pool, u"checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    # Setup pessimistic disconnection handling
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute(u"SELECT 1")
    except:
        logging.warning(u"Raising exc.DisconnectionError")
        raise exc.DisconnectionError()
    cursor.close()
