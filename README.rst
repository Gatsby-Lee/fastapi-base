fastapi-base
============

Setup local dev
---------------

.. code-block:: bash

    # create virtualenv / install required pkg
    python3 -m venv .venv
    .venv/bin/pip install -e .\[dev\]

    # in case you use private pypi repo in AWS or GCP
    .venv/bin/pip install -e .\[dev\] --extra-index-url https://pypi.org/simple


Run tests by docker-compose
---------------------------

.. code-block:: bash

    make build-and-test


HTTP Example API: Build / Run Image for Local testing
--------------------------------------------------

.. code-block:: bash

    docker compose -f ci-cd/development/docker-compose.example_api.yaml up \
        --remove-orphans --build --force-recreate

    # Check API docs
    http://127.0.0.1:8080/example/docs


HTTP Example API: Run without Container
-----------------------------------------------------

.. code-block:: bash

    export PATH_PREFIX="/example"
    uvicorn example_api.main:app --reload --port=8080

    # Check API docs
    http://127.0.0.1:8080/example/docs
