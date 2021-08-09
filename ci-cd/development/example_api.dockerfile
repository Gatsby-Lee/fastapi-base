# =================================================================
# @note: this config is setup to maximize intermediate cached image
# =================================================================
FROM python:3.7.8-slim AS base
USER root

# 1. setup global python env.
# 1.1. Install pkg
RUN pip install --upgrade pip virtualenv

# 2. setup up virtual env / codebase
# 2.1 setup up virtual env
WORKDIR /fastapi_base
RUN virtualenv -p python .venv
RUN .venv/bin/pip install pip --upgrade
# 2.2. Authenticate AWS Code Artifact
COPY setup.py setup.py
# 2.3. Authenticate AWS Code Artifact
RUN .venv/bin/pip install -e .[testing]
# 2.3. copy source code
COPY . /fastapi_base

# `--no-access-log` can be used to hide access log
ENTRYPOINT [".venv/bin/uvicorn", "example_api.main:app", \
    "--host", "0.0.0.0", \
    "--port", "8080" \
    ]
