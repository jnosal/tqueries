import tornado.concurrent
import tornado.gen
import tornado.web

from tqueries.sqla import get_session


class SqlalchemyRESTMixin(tornado.web.RequestHandler):

    @property
    def executor(self):
        return self.application._executor

    @tornado.concurrent.run_on_executor
    def _handle(self, handler):
        session = get_session()
        try:
            response = handler(session)
        except Exception as e:
            raise
        finally:
            print "LD"
            session.close()
        return response

    @tornado.gen.coroutine
    def get(self):
        response = yield self._handle(self.handle_get)
        self.write(response)
        self.finish()

    def handle_get(self, session):
        raise NotImplementedError

    @tornado.gen.coroutine
    def post(self):
        response = yield self._handle(self.handle_post)
        self.write(response)
        self.finish()

    def handle_post(self, session):
        raise NotImplementedError

    @tornado.gen.coroutine
    def put(self):
        response = yield self._handle(self.handle_put)
        self.write(response)
        self.finish()

    def handle_put(self, session):
        raise NotImplementedError

    @tornado.gen.coroutine
    def delete(self):
        response = yield self._handle(self.handle_delete)
        self.write(response)
        self.finish()

    def handle_delete(self, session):
        raise NotImplementedError

    @tornado.gen.coroutine
    def trace(self):
        response = yield self._handle(self.handle_trace)
        self.write(response)
        self.finish()

    def handle_trace(self, session):
        raise NotImplementedError

    @tornado.gen.coroutine
    def head(self):
        response = yield self._handle(self.handle_head)
        self.write(response)
        self.finish()

    def handle_head(self, session):
        raise NotImplementedError

    @tornado.gen.coroutine
    def connect(self):
        response = yield self._handle(self.handle_connect)
        self.write(response)
        self.finish()

    def handle_connect(self, session):
        raise NotImplementedError

    @tornado.gen.coroutine
    def options(self):
        response = yield self._handle(self.handle_options)
        self.write(response)
        self.finish()

    def handle_options(self, session):
        raise NotImplementedError
