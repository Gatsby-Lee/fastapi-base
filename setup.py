# Always prefer setuptools over distutils
from setuptools import setup, find_packages


requires = [
    # required
    "pip >= 21",
    # Public PyPi
    "fastapi>=0.68.0,<1.0.0",
    "pydantic>=1.8.2,<2.0.0",
    "uvicorn",
]


tests_require = [
    "pytest",
    "pytest-mock",
    "pytest-asyncio",  # to test async module
    "requests",  # to test fastapi
]


dev_require = tests_require + [
    "pylint",
    "black",
]


setup(
    name="fastapi-base",
    version="1.0",
    description="FastAPI Base",
    url="<your-codebase-link>",
    author="Gatsby Lee",
    packages=find_packages(exclude=["tests*", "playground", "ci-cd"]),
    python_requires=">=3.6",
    install_requires=requires,
    extras_require={"dev": dev_require, "testing": tests_require},
)
