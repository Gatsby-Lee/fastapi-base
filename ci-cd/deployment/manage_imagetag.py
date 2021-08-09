import argparse
import importlib
import logging
import os
import subprocess
import sys

from datetime import datetime
from typing import Optional, Tuple

LOGGER = logging.getLogger(__name__)
DEFAULT_HASH_LENGTH = 7


def get_git_revision_hash(length: Optional[str] = None) -> str:
    length = length or DEFAULT_HASH_LENGTH
    r_value = subprocess.check_output(["git", "rev-parse", "HEAD"])
    return r_value.decode().strip()[:length]


def get_gerrit_commit_hash(length: Optional[str] = None) -> str:
    length = length or DEFAULT_HASH_LENGTH
    try:
        os.environ.get("GERRIT_PATCHSET_REVISION", None)[:length]
    except Exception:
        return None


def create_image_tag(service_name: str) -> Tuple[str, str]:

    # @note: docker image tage
    # A tag name must be valid ASCII and may contain lowercase and uppercase letters, digits, underscores, periods and dashes.
    # A tag name may not start with a period or a dash and may contain a maximum of 128 characters.

    # 1. get service version
    service_path = f"{service_name}"
    LOGGER.info("start creating image tag for service_path=%s", service_path)
    version_module_path = "%s.__version__" % service_name
    try:
        version_module = importlib.import_module(version_module_path)
        service_version = version_module.__version__
        LOGGER.info("Fetched service-version: %s", service_version)
    except ModuleNotFoundError as e:
        LOGGER.error("Failed to import %s", version_module_path)
        raise e from None
    # 2. get commit hash
    commit_hash = get_gerrit_commit_hash() or get_git_revision_hash()
    LOGGER.info("Fetched commit hash: %s", commit_hash)
    # 3. create date
    today_date = datetime.utcnow().strftime("%y_%m%d_%H%M%S")
    # 4. crete metadata
    metadata_str = "-".join([today_date, commit_hash])
    image_tag = f"v{service_version}-{metadata_str}"
    return (str(service_version), image_tag)


def get_image_tag(service_name: str) -> str:

    # @note: docker image tage
    # A tag name must be valid ASCII and may contain lowercase and uppercase letters, digits, underscores, periods and dashes.
    # A tag name may not start with a period or a dash and may contain a maximum of 128 characters.

    # 1. get service version
    service_path = f"{service_name}"
    LOGGER.info("start creating image tag for service_path=%s", service_path)
    version_module_path = "%s.__version__" % service_name
    try:
        version_module = importlib.import_module(version_module_path)
        image_tag = version_module.__imagetag__
        LOGGER.info("Fetched imagetag: %s", image_tag)
        return image_tag
    except ModuleNotFoundError as e:
        LOGGER.error("Failed to import %s", version_module_path)
        raise e from None


def update_service_version(service_name: str, service_version: str, image_tag: str):
    version_module_path = "%s/__version__.py" % service_name
    with open(version_module_path, "w") as fw:
        # fw.write("# UTC Timezone: <YY>.<MMDD>.<HHMMSS>\n")
        fw.write('__version__ = "%s"\n' % service_version)
        fw.write('__imagetag__ = "%s"\n' % image_tag)


def _parse_args():
    parser = argparse.ArgumentParser()

    cmd_subparser = parser.add_subparsers(dest="cmd", required=True)
    create_image_tag_parser = cmd_subparser.add_parser("create-image-tag")
    create_image_tag_parser.add_argument("--service", required=True)

    get_image_tag_parser = cmd_subparser.add_parser("get-image-tag")
    get_image_tag_parser.add_argument("--service", required=True)

    return parser.parse_args()


def main():
    args = _parse_args()

    try:
        if args.cmd == "create-image-tag":
            service_version, image_tag = create_image_tag(args.service)
            print(image_tag)
            # if args.update_service_version:
            update_service_version(args.service, service_version, image_tag)
        elif args.cmd == "get-image-tag":
            print(get_image_tag(args.service))
    except Exception as e:
        LOGGER.error(e)
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
