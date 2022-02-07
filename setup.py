#!/usr/bin/python3

from distutils.core import setup

setup(
    name="tklamq",
    version="0.10",
    author="Jeremy Davis",
    author_email="jeremy@turnkeylinux.org",
    url="https://github.com/turnkeylinux/tklamq",
    packages=["tklamq_lib"],
    scripts=["tklamq_consume.py", "tklamq_declare.py", "tklamq_publish.py"]
)
