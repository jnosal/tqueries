import tornado.concurrent
import tornado.gen
import tornado.web

from tqueries.sqla import get_session


class SqlalchemyRESTMixin(tornado.web.RequestHandler):

    @property
    def executor(self):
        return self.application._executor

    def _handle(self, handler):
        session = get_session()
        response = handler(session)
        session.close()
        self.write(response)
        self.finish()

    @tornado.concurrent.run_on_executor
    def get(self):
        self._handle(self.handle_get)

    def handle_get(self, session):
        raise NotImplementedError

    @tornado.concurrent.run_on_executor
    def post(self):
        self._handle(self.handle_post)

    def handle_post(self, session):
        raise NotImplementedError

    @tornado.concurrent.run_on_executor
    def put(self):
        self._handle(self.handle_put)

    def handle_put(self, session):
        raise NotImplementedError

    @tornado.concurrent.run_on_executor
    def delete(self):
        self._handle(self.handle_delete)

    def handle_delete(self, session):
        raise NotImplementedError

    @tornado.concurrent.run_on_executor
    def trace(self):
        self._handle(self.handle_trace)

    def handle_trace(self, session):
        raise NotImplementedError
