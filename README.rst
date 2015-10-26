The idea behind this project is to have sqlalchemy specific handlers
that deal with session closing and run behind ThreadPoolExecutor not
blockinc ioloop.


0. Run project:

.. code-block:: bash

    $ python examples/sqla.py


1. Create couple of models

.. code-block:: bash

    $ curl -X POST http://localhost:8888

2. Retrieve (it sleeps for 2 seconds on purpose)

Create couple of models

.. code-block:: bash

    $ curl -X GET http://localhost:8888
