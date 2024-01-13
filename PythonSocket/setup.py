# -*- coding: utf-8 -*-
# Copyright (C) 2023 AnimatedWordCloud Project
# https://github.com/konbraphat51/AnimatedWordCloud
#
# Licensed under the MIT License.
"""
Setup script
"""
from setuptools import find_packages, setup
from pathlib import Path

# get README.md
readme = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")



setup(
    name="UnityConnector",
    version="0.0.1",
    description=" bidirectional TCP communication with Unity, the game engine",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="konbraphat51",
    author_email="konbraphat51@gmail.com",
    url="https://github.com/konbraphat51/UnityPythonConnectionClass",
    packages=find_packages(exclude=["tests", "Docs"]),
    test_suite="tests",
    python_requires=">=3.8",
    package_data={"AnimatedWordCloud": ["Assets/**"]},
    include_package_data=True,
    install_requires=[
    ],
    license="Boost Software License (BSL1.0)",
    zip_safe=False,
    keywords=[
        "Unity",
        "TCP",
        "C#"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
    ],
    entry_points={
        # "console_scripts": [
        # ],
    },
    project_urls={
        "GitHub Repository": "https://github.com/konbraphat51/UnityPythonConnectionClass"
    },
)