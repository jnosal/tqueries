The idea behind this project is to have sqlalchemy specific handlers
that deal with session closing and run behind ThreadPoolExecutor, not
blocking ioloop along the way.


Initialize sessionmaker and take a look at tqueries.mixins.SqlalchemyRESTMixin
and You're good to go :)


.. code-block:: python
    :emphasize-lines: 2

    engine = engine_from_config(settings, prefix=u'sqlalchemy.', echo=True)
    sqla.initialize_sessionmaker(engine=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

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
