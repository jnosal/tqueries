from contextlib import contextmanager

from tqueries.sqla import get_session


@contextmanager
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
