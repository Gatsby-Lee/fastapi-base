fastapi-base
============

setup local dev
---------------

.. code-block::

    # create virtualenv / install required pkg
    python3 -m venv .venv
    .venv/bin/pip install -e .\[dev\]

    # in case you use private pypi repo in AWS or GCP
    .venv/bin/pip install -e .\[dev\] --extra-index-url https://pypi.org/simple


Running Integration Testing by docker-compose
---------------------------------------------

.. code-block::

    make build-and-test
