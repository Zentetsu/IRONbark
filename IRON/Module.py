'''
File: Module.py
Created Date: Wednesday, July 3rd 2020, 8:52:00 pm
Author: Zentetsu

----

Last Modified: Wed Jul 08 2020
Modified By: Zentetsu

----

Project: SharedMemory
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
2020-07-08	Zen	Draft (not tested yet)
'''


from .IRONError import *
from SharedMemory import *


class Module:
    def __init__(self, name=None, file=None):
        if name is None and file is None or name is not None and file is not None:
            raise IRONMultiInputError()

        if file is not None:
            self._loadJSON(file)
        else:
            self.name = name

        self.listener = {}
        self.sender = {}

    def _loadJSON(self, file):
        #TODO write JSON loader
        pass

    def dumpJSON(self, file):
        #TODO write JSON dumper
        pass

    def _checkIntegrity(self):
        #TODO
        pass

    def _checkNameExistOrNot(self, name, exist=True):
        if exist:
            if name not in self.listener.keys() and name not in self.sender.keys():
                raise IRONNameNotExist(name)
        else:
            if name in self.listener.keys() or name in self.sender.keys():
                raise IRONNameExist(name)

    def addListener(self, name, timeout=1):
        self._checkNameExistOrNot(name, False)

        self.sender[name] = Server(name, timeout)

    def delListener(self, name):
        self._checkNameExistOrNot(name)

        self.listener.pop(name)
        self.stopModule(name)

    def addSender(self, name, value=None, path=None, size=10, timeout=1):
        self._checkNameExistOrNot(name, True)

        self.sender[name] = Client(name, value, path, size, timeout)

    def delSender(self, name):
        self._checkNameExistOrNot(name)

        self.stopModule(name)
        self.sender.pop(name)

    def getLSName(self, listener=True, sender=True):
        _listener = []
        _sender = []
        
        if listener:
            _listener = [n for n in self.listener.keys()]
        
        if sender:
            _sender = [n for n in self.sender.keys()]

        return _listener, _sender

    def getValue(self, name):
        self._checkNameExistOrNot(name, True)

        if name in self.listener.keys():
            return self.listener[name].getValue()
        else:
            return self.sender[name].getValue()

    def setValue(self, name, value):
        self._checkNameExistOrNot(name, True)

        if name in self.listener.keys():
            self.listener[name].updateValue(value)
        else:
            self.sender[name].updateValue(value)

    def startModule(self, name=None):
        #TODO for the moment: autostart
        pass

    def stopModule(self, name=None):
        if name is not None:
            if name in self.listener.keys():
                self.listener[name].stop()
            else:
                self.sender[name].stop()
        else:
            for n in self.listener.keys():
                self.listener[n].stop()

            for n in self.sender.keys():
                self.sender[n].stop()

    def restartModule(self, name=None):
        #TODO
        pass