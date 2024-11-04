"""
File: IRONError.py
Created Date: Wednesday, October 18th 2023, 4:12:15 pm
Author: Zentetsu

----

Last Modified: Mon Nov 04 2024
Modified By: Zentetsu

----

Project: IRONbark
Copyright (c) 2023-2024 Zentetsu

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
along with this program.  If not, see <http: //www.gnu.org/licenses/>.

----
HISTORY:
2020-07-08	Zen	Creating file
"""  # noqa


class IRONMultiInputError(Exception):
    """Exception raised when both name and file are either None or initialized."""

    def __init__(self, message: str = "name xor file must be None.") -> None:
        """Initialize the exception."""
        super().__init__(message)


class IRONNameExist(Exception):
    """Exception raised when a name already exists."""

    def __init__(self, name: str, message: str = " already exist.") -> None:
        """Initialize the exception."""
        super().__init__(name + message)


class IRONNameNotExist(Exception):
    """Exception raised when a name does not exist."""

    def __init__(self, name: str, message: str = " doesn't exist.") -> None:
        """Initialize the exception."""
        super().__init__(name + message)


class IRONKeyMissing(Exception):
    """Exception raised when a key is missing in the JSON file."""

    def __init__(self, message: str = "Key missing in JSON file.") -> None:
        """Initialize the exception."""
        super().__init__(message)


class IRONSenderListenerEmpty(Exception):
    """Exception raised when both sender and listener are empty."""

    def __init__(self, message: str = "Sender and Listener are empty.") -> None:
        """Initialize the exception."""
        super().__init__(message)
