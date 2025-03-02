#!/usr/bin/env python3
"""
Setup script for the Python Odds API client.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python_odds_api",
    version="0.1.0",
    author="Odds API Client Team",
    author_email="example@example.com",
    description="A Python client for The Odds API v4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/python_odds_api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.15.0",
    ],
)
