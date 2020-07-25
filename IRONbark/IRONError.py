'''
File: iRONError.py
Created Date: Wednesday, July 3rd 2020, 8:54:23 pm
Author: Zentetsu

----

Last Modified: Sun Jul 26 2020
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
'''


class IRONMultiInputError(Exception):
    def __init__(self, message="name xor file must be None."):
        self.message = message
        super().__init__(self.message)

class IRONNameExist(Exception):
    def __init__(self, name, message=" already exist."):
        self.message = name + message
        super().__init__(self.message)

class IRONNameNotExist(Exception):
    def __init__(self, name, message=" doesn't exist."):
        self.message = name + message
        super().__init__(self.message)

class IRONKeyMissing(Exception):
    def __init__(self, message="Key missing in JSON file."):
        self.message = message
        super().__init__(self.message)

class IRONSenderListenerEmpty(Exception):
    def __init__(self, message="Sender and Listener are empty."):
        self.message = message
        super().__init__(self.message)