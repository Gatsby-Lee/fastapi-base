"""
:author: Gatsby Lee
:since: 2021-04-28
"""
import logging
import time

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from example_api.excepts import (
    OkStatus,
)

LOGGER = logging.getLogger(__name__)

app = APIRouter()


@app.on_event("startup")
async def on_startup() -> None:
    pass


@app.on_event("shutdown")
async def on_shutdown() -> None:
    pass


# @app.get("/website/", response_model=WebsiteQueryResponse)
@app.get("/remote_cache/")
async def get_websites_by_keywords():
    tic = time.perf_counter()
    try:
        toc = time.perf_counter()
        result = "hello"
        return {
            "msg": OkStatus.msg,
            "status_code": OkStatus.status_code,
            "result": result,
            "time": f"{toc - tic:0.4f} sec",
        }
    except Exception as e:
        LOGGER.exception(e)
        return HTTPException(status_code=500, detail="Server Error.")
