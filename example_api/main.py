"""
:author: Gatsby Lee
:since: 2021-04-10
"""
import logging

from fastapi import FastAPI

from shared_lib.config import (
    get_default_log_format,
    get_default_log_level,
)
from example_api.config import (
    ABOUT_SERVICE,
    HEALTH_INFO,
    PATH_PREFIX,
)
from example_api.routers.router_selfex_cache_v1 import app as selfex_cache_v1


LOGGER = logging.getLogger(__name__)


# https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(
    title=ABOUT_SERVICE["title"],
    version=ABOUT_SERVICE["version"],
    docs_url=ABOUT_SERVICE["docs_url"],
    redoc_url=ABOUT_SERVICE["redoc_url"],
    openapi_url=ABOUT_SERVICE["openapi_url"],
)
app.include_router(
    selfex_cache_v1, prefix=f"{PATH_PREFIX}/v1", tags=["Self Expire Cache"]
)


@app.on_event("startup")
def main_startup_event():
    # setup logging
    log_handlers = None
    log_format = get_default_log_format()
    log_level = get_default_log_level()
    # setting a new list of handlers remove the default stderr handler
    logging.basicConfig(format=log_format, level=log_level, handlers=log_handlers)
    LOGGER.info("About Service: %s", ABOUT_SERVICE)


# This is for k8s health check.
@app.get("/", include_in_schema=False)
@app.get("/healthz", include_in_schema=False)
async def check_readiness():
    # Since all backend connection is checked while app starts up,
    # no need to do extra check.
    return HEALTH_INFO
