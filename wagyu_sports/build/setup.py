#!/usr/bin/env python3
"""
Setup script for the Wagyu Sports client.
"""
from setuptools import setup, find_packages

# Use a relative path that works in the package structure
import os
readme_path = os.path.join(os.path.dirname(__file__), "..", "docs", "LICENSE")
try:
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Wagyu Sports - A Python client for sports betting data"

setup(
    name="wagyu_sports",
    version="0.1.0",
    author="Wagyu Sports Team",
    author_email="example@example.com",
    description="A Python client for sports betting data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # URL removed as this is now part of a larger repository
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.15.0",
    ],
)
