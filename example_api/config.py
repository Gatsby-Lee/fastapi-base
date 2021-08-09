import os
import socket

from example_api.__version__ import __version__, __imagetag__

# ==== API Info ====
VERSION = __imagetag__ or __version__
HOSTNAME = socket.gethostname()
HEALTH_INFO = {
    "status": "ready",
    "hostname": HOSTNAME,
    "version": VERSION,
    "__debug__": __debug__,
}

# ==== API PATH ====
# @note: For Google Kubernetes Engine ( GKE )
# Since the current ingress-gce doesn't support url rewrite,
# the path prefix is added to match one in ingress-gcp.
PATH_PREFIX = os.environ.get("PATH_PREFIX", "")

# ==== API Doc ====
DISABLE_APIDOC = os.environ.get("DISABLE_APIDOC", "")
API_DOCS_URL = API_REDOC_URL = API_OPENAPI_URL = None
if DISABLE_APIDOC == "":
    API_DOCS_URL = f"{PATH_PREFIX}/docs"
    API_REDOC_URL = f"{PATH_PREFIX}/redoc"
    API_OPENAPI_URL = f"{PATH_PREFIX}/openapi.json"

ABOUT_SERVICE = {
    "version": VERSION,
    "title": "Example API",
    "docs_url": API_DOCS_URL,
    "redoc_url": API_REDOC_URL,
    "openapi_url": API_OPENAPI_URL,
}
