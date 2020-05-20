#!/usr/bin/python3
from setuptools import setup

setup(
    name="aiqdoctests",
    version="1.0.0",
    author="An Awesome Coder",
    author_email="dev@aiqfome.com",
    scripts=["scripts/aiqdoctests"],
    packages=["aiqdoctests"],
    url="https://github.com/aiqfome/aiqDocTests",
    license="LICENSE",
    description="A framework to validate request/response's json and create documentation",
    install_requires=["cerberus", "requests"],
    package_data={"aiqdoctests": [".aiqdoctests.config", "wait"]},
    include_package_data=True,
    zip_safe=False,
)
