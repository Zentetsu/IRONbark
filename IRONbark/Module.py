'''
File: Module.py
Created Date: Wednesday, July 3rd 2020, 8:52:00 pm
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
2020-07-23	Zen	Fixing Module creation by JSON file
2020-07-22	Zen	Adding comments and Availability method
2020-07-17	Zen	fix for addListener and delListener
2020-07-13	Zen	Draft finished (not tested yet)
2020-07-08	Zen	Draft (not tested yet)
'''


from .IRONError import *
from SharedMemory import *
import json


class Module:
    """Module class focused on communicate data with other modules
    """
    def __init__(self, name:str=None, file:str=None):
        """Class constructor

        Args:
            name (str, optional): desired name for the module. Defaults to None.
            file (str, optional): path to load JSON file and construct module following is content. Defaults to None.

        Raises:
            IRONMultiInputError: raise an error when value and path are both at None or initilalized
        """
        if name is None and file is None or name is not None and file is not None:
            raise IRONMultiInputError()

        self.sender = {}
        self.listener = {}

        if file is not None:
            self._loadJSON(file)
        else:
            self.name = name

    def _loadJSON(self, file:str):
        """Method to load the module structure from a JSON file

        Args:
            file (str): path of the JSON file
        """
        #TODO need to be tested
        json_file = open(file)
        value = json.load(json_file)
        json_file.close()

        print(value)

        self._checkIntegrity(value)

        self.name = value["name"]

        for s in value["sender"].keys():
            self.addSender(s, value["sender"][s])

        for s in value["listener"]:
            self.addListener(s)

    def dumpJSON(self, file:str):
        """Method to save the module structure into a JSON file

        Args:
            file (str): path to the JSON file
        """
        #TODO need to be tested
        _dict = {"name": self.name, "sender": self.sender, "listener": self.listener}
        json_file = open(file)
        value = json.dump(json_file)
        json_file.close()

    def _checkIntegrity(self, value:dict):
        """Method to chech the integrity of the module structure extract from the JSON file

        Args:
            value (dict): dict that's containt values of the module

        Raises:
            IRONKeyMissing: raise an error when one of the principal key is not into the dict
            IRONSenderListenerEmpty: raise ann error when there(re not listener and sender into the dict)
        """
        if not all([n in value.keys() for n in ["name", "sender", "listener"]]):
            raise IRONKeyMissing

        if not value["sender"] and not value["listener"]:
            raise IRONSenderListenerEmpty

    def _checkNameExistOrNot(self, name:str, exist=True):
        """Method that check if a name is already or not used by a shared memory

        Args:
            name (str): Shared Memory name
            exist (bool, optional): True -> name mst be defined, False -> name must be undefined. Defaults to True.

        Raises:
            IRONNameNotExist: raise an error if name doesn't exist
            IRONNameExist: raise an error if name exist
        """
        if exist:
            if name not in self.listener.keys() and name not in self.sender.keys():
                raise IRONNameNotExist(name)
        else:
            if name in self.listener.keys() or name in self.sender.keys():
                raise IRONNameExist(name)

    def addListener(self, name:str, timeout=1):
        """Method to add a Shared Memory Server

        Args:
            name (str): Shared Memory Name
            timeout (int, optional): mutex timeout. Defaults to 1.
        """
        self._checkNameExistOrNot(name, False)

        self.listener[name] = Server(name, timeout)

    def delListener(self, name:str):
        """Method to remove a Shared Memory Server

        Args:
            name ([type]): Shared Memory name
        """
        self._checkNameExistOrNot(name)

        self.stopModule(name)
        self.listener.pop(name)

    def addSender(self, name:str, value=None, path:str=None, size=10, timeout=1):
        """Method to add a Shared Memory Client

        Args:
            name (str): Shared Memory name
            value ([type], optional): value to share with the other module. Defaults to None.
            path (str, optional): path to load JSON file and share the data inside. Defaults to None.
            size (int, optional):  or str value. Defaults to 10.
            timeout (int, optional): mutex timeout. Defaults to 1.
        """
        self._checkNameExistOrNot(name, False)

        self.sender[name] = Client(name, value, path, size, timeout)

    def delSender(self, name:str):
        """Method to remove a Shared Memory Client

        Args:
            name (str): Shared Memory name
        """
        self._checkNameExistOrNot(name)

        self.stopModule(name)
        self.sender.pop(name)

    def getLSName(self, listener=True, sender=True) -> [list, list]:
        """Method to return al liste that contains name of sender and listener

        Args:
            listener (bool, optional): True -> will add listener names to the list. Defaults to True.
            sender (bool, optional): True -> will ad sender names to the list. Defaults to True.

        Returns:
            [list, list]: list of sender and listener names
        """
        _sender = []
        _listener = []

        if sender:
            _sender = [n for n in self.sender.keys()]

        if listener:
            _listener = [n for n in self.listener.keys()]

        return  _sender, _listener

    def getValue(self, name:str):
        """Method to get value from a sender or a listener

        Args:
            name (str): name of the sender or listener

        Returns:
            [type]: return data
        """
        self._checkNameExistOrNot(name, True)

        if name in self.sender.keys():
            return self.sender[name].getValue()
        else:
            return self.listener[name].getValue()

    def setValue(self, name:str, value):
        """Method to update data

        Args:
            name (str): name of the sender or listener
            value ([type]): new value to assign
        """
        self._checkNameExistOrNot(name, True)

        if name in self.sender.keys():
            self.sender[name].updateValue(value)
        else:
            self.listener[name].updateValue(value)

    def getLSAvailability(self, listener=True, sender=True) -> [list, list]:
        """Method to get the availability of each sender and listener

        Args:
            listener (bool, optional): True -> will add listener availability. Defaults to None.
            sender (bool, optional): True -> will add sender availability. Defaults to None.

        Returns:
            [list, list]: list of the sender and listener availability
        """
        _sender = []
        _listener = []

        if sender:
            _sender = [self.sender[n].getAvailability() for n in self.sender.keys()]

        if listener:
            _listener = [self.listener[n].getAvailability() for n in self.listener.keys()]

        return  _sender, _listener

    def startModule(self, name:str=None):
        """Method to start senders and listeners

        Args:
            name (str, optional): if setted will launch only this one. Defaults to None.
        """
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

    def stopModule(self, name:str=None):
        """Method to stop senders and listeners

        Args:
            name (str, optional): if setted will stop only this one. Defaults to None.
        """
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

    def restartModule(self, name:str=None):
        """Method to restart senders and listeners

        Args:
            name (str, optional): if setted will restart only this one. Defaults to None.
        """
        if name is not None:
            self._checkNameExistOrNot(name)
            if name in self.sender.keys():
                self.sender[name].restart()
            else:
                self.listener[name].restart()

        else:
            for n in self.sender.keys():
                self.sender[n].restart()

            for n in self.listener.keys():
                self.listener[n].reconnect()

    def __repr__(self):
        """Redefined method to print value of the Module Class instance

        Returns:
            str: printable value of Module Class instance
        """
        s = "Name: " + self.name + "\n"\
            + "\tSender: " + list(self.sender.keys()).__repr__() + "\n"\
            + "\tListener: " + list(self.listener.keys()).__repr__()

        return s