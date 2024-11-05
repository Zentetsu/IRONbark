"""
File: Module.py
Created Date: Wednesday, July 3rd 2020, 8:52:00 pm
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
2021-11-25	Zen	Updating lib to work with new SharedMeory version
2021-11-24	Zen	Updating lib to work with new SharedMeory version
2020-11-06	Zen	Fix calling wrong method
2020-10-14	Zen	Updating dumpJSON method
2020-10-14	Zen	Adding getter to access to Module data
2020-07-23	Zen	Fixing Module creation by JSON file
2020-07-22	Zen	Adding comments and Availability method
2020-07-17	Zen	fix for addListener and delListener
2020-07-13	Zen	Draft finished (not tested yet)
2020-07-08	Zen	Draft (not tested yet)
2023-08-27	Zen	Checking numpy compatibility
2023-10-18	Zen	Changing default memory size
2024-11-04	Zen	Adding remote communication, silent mode + Updating docstring
2024-11-04	Zen	Adding memory size to the Module
2024-11-05	Zen	Correcting remote connection when sender drops
"""  # noqa

from .IRONError import IRONMultiInputError, IRONNameNotExist, IRONNameExist, IRONKeyMissing, IRONSenderListenerEmpty
from SharedMemory import SharedMemory
import threading
import asyncio
import struct
import numpy
import json
import time


class Module:
    """Module class focused on communicate data with other modules."""

    def __init__(self, name: str = None, file: str = None, silent: bool = False, size: int = None) -> None:
        """Class constructor.

        Args:
            name (str, optional): desired name for the module. Defaults to None.
            file (str, optional): path to load JSON file and construct module following is content. Defaults to None.
            silent (bool, optional): True -> will not print any error, False -> will print error. Defaults to False.
            size (int, optional): size of the shared memory. Defaults to None.

        Raises:
            IRONMultiInputError: raise an error when value and path are both at None or initilalized

        """
        if name is None and file is None or name is not None and file is not None:
            raise IRONMultiInputError()

        self.sender = {}
        self.listener = {}
        self.remote_sender = [(None, None), None, None, True]
        self.remote_listener = {}
        self.data_remote_sender = None
        self.data_remote_listener = False
        self.new_data = True
        self.silent = silent
        self.size = size

        if file is not None:
            self._loadJSON(file)
        else:
            self.name = name

    def dumpJSON(self, file: str) -> None:
        """Save the module structure into a JSON file.

        Args:
            file (str): path to the JSON file

        """
        _dict = {"name": self.name, "sender": {}, "listener": []}

        for k in self.sender.keys():
            if isinstance(self.sender[k].getValue(), numpy.ndarray):
                _dict["sender"][k] = self.sender[k].getValue().tolist()
            else:
                _dict["sender"][k] = self.sender[k].getValue()

        for k in self.listener.keys():
            _dict["listener"].append(k)

        json_file = open(file, "w+")
        json.dump(_dict, json_file)
        json_file.close()

    def addListener(self, name: str) -> None:
        """Add a Shared Memory Server.

        Args:
            name (str): Shared Memory Name

        """
        self._checkNameExistOrNot(name, False)

        if name in self.remote_listener:
            self.remote_listener[name][1] = threading.Thread(
                target=self.__createSocketListener,
                args=(self.remote_listener[name][0], name),
            )
            self.remote_listener[name][1].start()

        self.listener[name] = SharedMemory(name, client=False, silent=self.silent)

    def delListener(self, name: str) -> None:
        """Remove a Shared Memory Server.

        Args:
            name ([type]): Shared Memory name

        """
        self._checkNameExistOrNot(name)

        self.stopModule(name)
        self.listener.pop(name)

    def addSender(self, name: str, value: any = None, path: str = None) -> None:
        """Add a Shared Memory Client.

        Args:
            name (str): Shared Memory name
            value ([type], optional): value to share with the other module. Defaults to None.
            path (str, optional): path to load JSON file and share the data inside. Defaults to None.

        """
        self._checkNameExistOrNot(name, False)

        if self.remote_sender[0] != (None, None):
            self.remote_sender[2] = threading.Thread(target=self.__createSocketSender, args=(self.remote_sender[0],))
            self.remote_sender[2].start()
            self.__updateData(value)

        self.sender[name] = SharedMemory(name, value, path, self.size, client=True, silent=self.silent)

    def delSender(self, name: str) -> None:
        """Remove a Shared Memory Client.

        Args:
            name (str): Shared Memory name

        """
        self._checkNameExistOrNot(name)

        self.stopModule(name)
        self.sender.pop(name)

    def getLSName(self, listener: bool = True, sender: bool = True) -> list:
        """Return a list that contains name of sender and listener.

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

        return _sender, _listener

    def getValue(self, name: str) -> any:
        """Get value from a sender or a listener.

        Args:
            name (str): name of the sender or listener

        Returns:
            [type]: return data

        """
        self._checkNameExistOrNot(name, True)

        if name in self.sender.keys():
            return self.sender[name].getValue()
        else:
            if name in self.remote_listener:
                stop_it = 5
                asyncio.run(self.__askData())
                while self.requested and stop_it > 0:
                    time.sleep(0.1)
                    stop_it -= 1

                if self.requested and stop_it == 0:
                    return None

                return self.data_remote_listener
            else:
                return self.listener[name].getValue()

    def setValue(self, name: str, value: any) -> None:
        """Update data.

        Args:
            name (str): name of the sender or listener
            value ([type]): new value to assign

        """
        self._checkNameExistOrNot(name, True)

        if name in self.sender.keys():
            self.sender[name].setValue(value)

            asyncio.run(self.__newData())
            self.__updateData(value)
        else:
            self.listener[name].setValue(value)

    def getLSAvailability(self, listener: bool = False, sender: bool = False) -> list:
        """Get the availability of each sender and listener.

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

        return _sender, _listener

    def startModule(self, name: str = None) -> None:
        """Start senders and listeners.

        Args:
            name (str, optional): if setted will launch only this one. Defaults to None.

        """
        if name is not None:
            self._checkNameExistOrNot(name)
            if name in self.sender.keys():
                self.sender[name].restart()
                self.startRemote(True)
            else:
                self.listener[name].restart()
                self.startRemote(False, name)
        else:
            for n in self.sender.keys():
                self.sender[n].restart()
                self.startRemote(True)

            for n in self.listener.keys():
                self.listener[n].restart()
                self.startRemote(False, n)

    def stopModule(self, name: str = None) -> None:
        """Stop senders and listeners.

        Args:
            name (str, optional): if setted will stop only this one. Defaults to None.

        """
        if name is not None:
            if name in self.sender.keys():
                self.sender[name].close()
                self.stopRemote(True)
            else:
                self.listener[name].close()
                self.stopRemote(False, name)
        else:
            for n in self.sender.keys():
                self.sender[n].close()
                self.stopRemote(True)

            for n in self.listener.keys():
                self.listener[n].close()
                self.stopRemote(False, n)

    def startRemote(self, sender: bool, name: str = "") -> None:
        """Start remote communication.

        Args:
            sender (bool): True -> will start remote sender, False -> will start remote listener
            name (str, optional): name of the listener. Defaults to "".

        """
        if not sender and name in self.remote_listener and not self.remote_listener[name][2]:
            self.remote_listener[name][1] = threading.Thread(
                target=self.__createSocketListener,
                args=(self.remote_listener[name][0], name),
            )
            self.remote_listener[name][2] = True
            self.remote_listener[name][1].start()
        elif sender and not self.remote_sender[3]:
            self.remote_sender[2] = threading.Thread(target=self.__createSocketSender, args=(self.remote_sender[0],))
            self.remote_sender[3] = True
            self.remote_sender[2].start()
            self.__updateData(self.sender[list(self.sender.keys())[0]].getValue())
            asyncio.run(self.__newData())

    def stopRemote(self, sender: bool, name: str = "") -> None:
        """Stop remote communication.

        Args:
            sender (bool): True -> will stop remote sender, False -> will stop remote listener
            name (str, optional): name of the listener. Defaults to "".

        """
        if not sender and name in self.remote_listener and self.remote_listener[name][1] is not None and self.remote_listener[name][2]:
            asyncio.run(self.__stopSocket(False, name))
            self.remote_listener[name][1].join()
        elif sender and self.remote_sender[2] is not None and self.remote_sender[3]:
            asyncio.run(self.__stopSocket(True))
            self.remote_sender[2].join()

    def restartModule(self, name: str = None) -> None:
        """Restart senders and listeners.

        Args:
            name (str, optional): if setted will restart only this one. Defaults to None.

        """
        self.startModule(name)

    def _loadJSON(self, file: str) -> None:
        """Load the module structure from a JSON file.

        Args:
            file (str): path of the JSON file

        """
        # TODO need to be tested
        json_file = open(file)
        value = json.load(json_file)
        json_file.close()

        self._checkIntegrity(value)

        self.name = value["name"]

        for s in value["sender"]:
            self.addSender(s, value["sender"][s])

        for s in value["listener"]:
            if value["listener"][s] != []:
                self.remote_listener[s] = [value["listener"][s], None, True]

            self.addListener(s)

    def _checkNameExistOrNot(self, name: str, exist: bool = True) -> None:
        """Check if a name is already or not used by a shared memory.

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

    def _checkIntegrity(self, value: dict) -> None:
        """Chech the integrity of the module structure extract from the JSON file.

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

        if "remote" in value:
            self.remote_sender[0] = (value["remote"]["ip"], value["remote"]["port"])

    def __getitem__(self, key: any) -> any:
        """Get item value from Module.

        Args:
            key (str): key

        Returns:
            [type]: return data

        """
        if type(key) is not str:
            raise TypeError("Key should a str.")

        self._checkNameExistOrNot(key, True)

        if key in self.sender.keys():
            return self.sender[key]
        else:
            return self.listener[key]

    def __repr__(self) -> str:
        """Redefine Print value of the Module Class instance.

        Returns:
            str: printable value of Module Class instance

        """
        s = "Name: " + self.name + "\n" + "\tSender: " + list(self.sender.keys()).__repr__() + "\n" + "\tListener: " + list(self.listener.keys()).__repr__()

        return s

    def __createSocketSender(self, remote: tuple) -> None:
        """Create a socket for remote communication.

        Args:
            remote (tuple): ip and port of the remote communication

        """

        async def __handleSocket(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            data = None

            while self.remote_sender[3]:
                try:
                    try:
                        request = await asyncio.wait_for(reader.readexactly(3), timeout=1.0)
                    except asyncio.TimeoutError:
                        continue

                    if self.new_data:
                        data = self.data_remote_sender
                        self.new_data = False

                    request = request.decode()
                    if request == "ASK":
                        data_enc = json.dumps(data).encode()
                        data_length = struct.pack(">I", len(data_enc))

                        writer.write("ACK".encode() + data_length + "END".encode())
                        writer.write("PKG".encode() + data_enc)
                        await writer.drain()
                        request = ""
                except asyncio.IncompleteReadError:
                    break

            writer.close()
            await writer.wait_closed()

        async def __startServer(ip: str, port: str) -> None:
            server = await asyncio.start_server(__handleSocket, ip, port)
            try:
                await server.serve_forever()
            except asyncio.CancelledError:
                server.close()
                await server.wait_closed()

        async def __initComm() -> None:
            self.remote_sender[1] = asyncio.create_task(__startServer(remote[0], remote[1]))

            while not self.remote_sender[1].done():
                await asyncio.sleep(0.1)

        asyncio.run(__initComm())

    def __createSocketListener(self, remote: tuple, name: str) -> None:
        """Create a socket for remote communication.

        Args:
            remote (tuple): ip and port of the remote communication
            name (str): name of the listener

        """

        async def receiveDataDel(reader: asyncio.StreamReader, delimiter: bytes = b"END") -> bytes:
            data = b""
            while True:
                chunk = await reader.readexactly(1)
                if not chunk:
                    return b""

                data += chunk
                if data.endswith(delimiter):
                    return data[: -len(delimiter)]

        async def receiveDataSize(reader: asyncio.StreamReader, size: int = 0) -> bytes:
            data = await reader.readexactly(size)
            return data

        async def __handleSocket(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, name: str) -> None:
            size = 0
            send = False
            data = None
            while self.remote_listener[name][2]:
                try:
                    if self.requested:
                        if not send:
                            writer.write("ASK".encode())
                            await writer.drain()
                            send = True

                        if send:
                            try:
                                start_frame = await asyncio.wait_for(reader.readexactly(3), timeout=1.0)
                            except asyncio.TimeoutError:
                                break

                            start_frame = start_frame.decode()

                            if start_frame == "ACK" and (request := await receiveDataDel(reader)) != b"":
                                size = struct.unpack(">I", request)[0]

                            if start_frame == "PKG" and (request := await receiveDataSize(reader, size)) != b"":
                                data = json.loads(request.decode())
                                self.data_remote_listener = data
                                size = 0
                                send = False
                                self.requested = False
                except asyncio.IncompleteReadError:
                    break

            self.data_remote_listener = None

        async def __startClient(ip: str, port: str, name: str) -> None:
            while self.remote_listener[name][2]:
                try:
                    reader, writer = await asyncio.open_connection(ip, port)
                    await __handleSocket(reader, writer, name)
                except ConnectionRefusedError:
                    time.sleep(0.1)

        asyncio.run(__startClient(remote[0], remote[1], name))

    async def __askData(self) -> None:
        self.requested = True

    async def __newData(self) -> None:
        self.new_data = True

    async def __stopSocket(self, sender: bool = False, name: str = "") -> None:
        if sender and self.remote_sender[1]:
            self.remote_sender[1].cancel()
            self.remote_sender[3] = False
        elif name != "":
            self.remote_listener[name][2] = False

    def __updateData(self, value: any) -> None:
        self.data_remote_sender = value
