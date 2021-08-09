# =================================================================
# @note: this config is setup to maximize intermediate cached image
# =================================================================
FROM python:3.7.8-slim AS base
USER root

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

# 1. setup global python env.
# 1.1. Install pkg
RUN pip install --upgrade pip virtualenv
RUN pip install pipx && pipx ensurepath
# 1.2. Setup awscli.
# install awscli on global, it won't be part of virtualenv in the built image
RUN pipx install awscli

# 2. setup up virtual env / codebase
# 2.1 setup up virtual env
WORKDIR /fastapi_base
RUN virtualenv -p python .venv
RUN .venv/bin/pip install pip --upgrade
# 2.2. copy setup.py to check changes in pkgs
COPY setup.py setup.py
# 2.3. Authenticate AWS Code Artifact - if Cached AWS intermediate Image is used, Auth fails.
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
RUN /root/.local/bin/aws codeartifact login --tool pip --domain <from-aws> --repository <from-aws>
# 2.4. Install pkgs
RUN .venv/bin/pip install -e .[testing] --extra-index-url https://pypi.org/simple
# 2.3. copy source code
COPY . /fastapi_base
