#!/usr/bin/python3
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aiqDocTests",
    version="1.7.1",
    author="An Awesome Coder",
    author_email="dev@aiqfome.com",
    scripts=["scripts/aiqdoctests"],
    packages=["aiqdoctests"],
    url="https://github.com/aiqfome/aiqDocTests",
    license="Apache License 2.0",
    description="A framework to validate request/response's json and create documentation for REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["cerberus", "requests", "flask_swagger_ui"],
    package_data={"aiqdoctests": [".aiqdoctests.config", "wait"]},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Text Editors :: Documentation",
    ],
)
