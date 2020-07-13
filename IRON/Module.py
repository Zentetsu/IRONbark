'''
File: Module.py
Created Date: Wednesday, July 3rd 2020, 8:52:00 pm
Author: Zentetsu

----

Last Modified: Mon Jul 13 2020
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
2020-07-13	Zen	Draft finished (not tested yet)
2020-07-08	Zen	Draft (not tested yet)
'''


from .IRONError import *
from SharedMemory import *
import json


class Module:
    def __init__(self, name=None, file=None):
        if name is None and file is None or name is not None and file is not None:
            raise IRONMultiInputError()

        if file is not None:
            self._loadJSON(file)
        else:
            self.name = name
            self.sender = {}
            self.listener = {}

    def _loadJSON(self, file):
        json_file = open(file)
        value = json.load(json_file)
        json_file.close()

        self._checkIntegrity(value)

        self.name = value["name"]
        self.sender = value["sender"]
        self.listener = value["listener"]

    def dumpJSON(self, file):
        _dict = {"name": self.name, "sender": self.sender, "listener": self.listener}
        json_file = open(file)
        value = json.dump(json_file)
        json_file.close()

    def _checkIntegrity(self, value: dict):
        if not all([n in value.key() for n in ["name", "sender", "listener"]]):
            raise IRONKeyMissing

        if not value["sender"] and not value["listener"]:
            raise IRONSenderListenerEmpty

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
        _sender = []
        _listener = []

        if sender:
            _sender = [n for n in self.sender.keys()]

        if listener:
            _listener = [n for n in self.listener.keys()]

        return  _sender, _listener

    def getValue(self, name):
        self._checkNameExistOrNot(name, True)

        if name in self.sender.keys():
            return self.sender[name].getValue()
        else:
            return self.listener[name].getValue()

    def setValue(self, name, value):
        self._checkNameExistOrNot(name, True)

        if name in self.sender.keys():
            self.sender[name].updateValue(value)
        else:
            self.listener[name].updateValue(value)

    def startModule(self, name=None):
        if name is not None:
            self._checkNameExistOrNot(name)
            if name in self.sender.keys():
                self.sender[name].start()
            else:
                self.listener[name].start()
        else:
            for n in self.sender.keys():
                self.sender[n].start()

            for n in self.listener.keys():
                self.listener[n].connect()

    def stopModule(self, name=None):
        if name is not None:
            if name in self.sender.keys():
                self.sender[name].stop()
            else:
                self.listener[name].stop()
        else:
            for n in self.sender.keys():
                self.sender[n].stop()

            for n in self.listener.keys():
                self.listener[n].stop()

    def restartModule(self, name=None):
        if name is not None:
            self._checkNameExistOrNot(name)
            self.listener[name].restart()

        else:
            for n in self.sender.keys():
                self.sender[n].restart()

            for n in self.listener.keys():
                self.listener[n].reconnect()

    def __repr__(self):
        s = "Name: " + self.name + "\n" + "Sender: " + self.sender.__repr__() + "\n" + "Listener: " + self.listener.__repr__()

        return s