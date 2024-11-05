"""
File: setup.py
Created Date: Friday, July 5th 2020, 10:11:51 pm
Author: Zentetsu

----

Last Modified: Tue Nov 05 2024
Modified By: Zentetsu

----

Project: IRONbark
Copyright (c) 2020 Zentetsu

----

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

----

HISTORY:
2020-07-08	Zen	Creating file
"""  # noqa

from setuptools import setup, find_packages

setup(
    name="IRONbark",
    version="1.2.2",
    author="Zentetsu",
    packages=find_packages(exclude=["tests*"]),
    license="GPLv3",
    description="Inter Process Communication",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["SharedMemory", "numpy"],
    url="https://github.com/Zentetsu/IRONbark",
    python_requires=">=3.10",
)
