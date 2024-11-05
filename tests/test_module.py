"""
File: test_module.py
Created Date: Wednesday, July 3rd 2020, 9:08:42 pm
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
2020-10-14	Zen	Updating test
2020-10-13	Zen	Updating test
2020-07-23	Zen	Adding test for JSON file
2020-07-08	Zen	Creating file
2023-10-18  Zen Updating test
2024-10-30	Zen	Fuxning test and error output
2024-11-04	Zen	Updating docstring + unittest
2024-11-05	Zen	Avoid infinite loop when FAIL
"""  # noqa

# import sys

# sys.path.insert(0, "../")

from IRONbark.Module import Module
import unittest


class TestIRONBark(unittest.TestCase):
    """Test IRONBark module."""

    def test_creation(self) -> None:
        """Test Module creation."""
        try:
            m = Module("test__0", silent=True)
            self.assertTrue(m.getLSName() == ([], []))
        except:
            self.assertTrue(False)

    def test_addSender(self) -> None:
        """Test adding a Sender to a Module."""
        try:
            m = Module("test_1", silent=True)
            m.addSender("name_0", value=10)
            self.assertTrue(m.getValue("name_0") == 10)
            self.assertTrue(m["name_0"][0] == 10)
            m.stopModule()
        except:
            m.stopModule()
            self.assertTrue(False)

    def test_addListener(self) -> None:
        """Test adding a Listener to a Module without Sender."""
        try:
            m = Module("test_2", silent=True)
            m.addListener("name_1")
            self.assertTrue(m.getValue("name_1") is None)
            self.assertTrue(m["name_1"][0] is None)
            m.stopModule()
        except:
            m.stopModule()
            self.assertTrue(False)

    def test_addListener_2(self) -> None:
        """Test adding a Listener to a Module with Sender."""
        try:
            m = Module("test_3", silent=True)
            m.addSender("name_2", value=10)
            m2 = Module("test_3b", silent=True)
            m2.addListener("name_2")
            self.assertTrue(m2.getValue("name_2") == 10)
            self.assertTrue(m2["name_2"][0] == 10)
            m.stopModule()
            m2.stopModule()
        except:
            m.stopModule()
            m2.stopModule()
            self.assertTrue(False)

    def test_restart(self) -> None:
        """Test restarting a Module."""
        try:
            m = Module("test_4", silent=True)
            m.addSender("name_3", value=10)
            m.restartModule("name_3")
            m.stopModule()
            self.assertTrue(True)
        except:
            m.stopModule()
            self.assertTrue(False)

    def test_stopStart(self) -> None:
        """Test stopping and starting a Module."""
        try:
            m = Module("test_5", silent=True)
            m.addSender("name_4", value=10)
            m.stopModule("name_4")
            m.startModule("name_4")
            m.stopModule()
            self.assertTrue(True)
        except:
            m.stopModule()
            self.assertTrue(False)

    def test_setValue(self) -> None:
        """Test setting a value to a Sender."""
        try:
            m = Module("test_7", silent=True)
            m.addSender("name_5", value=10)
            m.setValue("name_5", 20)
            self.assertTrue(m.getValue("name_5") == 20)
            self.assertTrue(m["name_5"][0] == 20)
            m.stopModule()
        except:
            m.stopModule()
            self.assertTrue(False)

    def test_setValue_2(self) -> None:
        """Test setting a value to a Sender from another Module."""
        try:
            m = Module("test_8a", silent=True)
            m.addSender("name_6", value=10)
            m2 = Module("test_8b", silent=True)
            m2.addListener("name_6")
            m.setValue("name_6", 20)
            self.assertTrue(m2.getValue("name_6") == 20)
            self.assertTrue(m2["name_6"][0] == 20)
            m.stopModule()
            m2.stopModule()
        except:
            m.stopModule()
            m2.stopModule()
            self.assertTrue(False)

    def test_setValue_3(self) -> None:
        """Test setting a value to a Sender from another Module."""
        try:
            m = Module("test_9a", silent=True)
            m.addSender("name_7", value=10)
            m2 = Module("test_9b", silent=True)
            m2.addListener("name_7")
            m2.setValue("name_7", 20)
            self.assertTrue(m.getValue("name_7") == 20)
            self.assertTrue(m2["name_7"][0] == 20)
            m.stopModule()
            m2.stopModule()
        except:
            m.stopModule()
            m2.stopModule()
            self.assertTrue(False)

    def test_delSender(self) -> None:
        """Test removing a Sender from a Module."""
        try:
            m = Module("test_10", silent=True)
            m.addSender("name_8", value=10)
            _s, _ = m.getLSName()
            self.assertTrue(len(_s) == 1)
            m.delSender("name_8")
            _s, _ = m.getLSName()
            self.assertTrue(len(_s) == 0)
            m.stopModule()
        except:
            m.stopModule()
            self.assertTrue(False)

    def test_delListener(self) -> None:
        """Test removing a Listener from a Module."""
        try:
            m = Module("test_11a", silent=True)
            m2 = Module("test_11b", silent=True)
            m.addSender("name_9", value=10)
            m2.addListener("name_9")
            _, _l = m2.getLSName()
            self.assertTrue(len(_l) == 1)
            m2.delListener("name_9")
            _, _l = m2.getLSName()
            self.assertTrue(len(_l) == 0)
            m.stopModule()
            m2.stopModule()
        except:
            m.stopModule()
            m2.stopModule()
            self.assertTrue(False)

    def test_(self) -> None:
        """Test stopping a Module."""
        try:
            m = Module("test_12a", silent=True)
            m2 = Module("test_12b", silent=True)
            m.addSender("name_10", value=10)
            m2.addListener("name_10")
            m.stopModule("name_10")
            m.stopModule()
            m2.stopModule()
            self.assertTrue(True)
        except:
            m.stopModule()
            m2.stopModule()
            self.assertTrue(False)

    def test_availability(self) -> None:
        """Test availability of a Module."""
        try:
            m = Module("test_13", silent=True)
            m.addSender("name_11", value=10)
            self.assertTrue(m.getLSAvailability(sender=True) == ([True], []))
            m.stopModule()
        except:
            m.stopModule()
            self.assertTrue(False)

    def test_availability_2(self) -> None:
        """Test availability of a Module bis."""
        try:
            m = Module("test_14a", silent=True)
            m2 = Module("test_14b", silent=True)
            m.addSender("name_12", value=10)
            m2.addListener("name_12")
            self.assertTrue(m.getLSAvailability(sender=True) == ([True], []))
            self.assertTrue(m2.getLSAvailability(listener=True) == ([], [True]))
            m.stopModule()
            m2.stopModule()
        except:
            m.stopModule()
            m2.stopModule()
            self.assertTrue(False)

    def test_JSON(self) -> None:
        """Test creating a Module from a JSON file."""
        try:
            m = Module(file="tests/test.json", silent=True)
            self.assertTrue(m.getValue("sender_1") == {"test": [10, 30, True], "test2": ["a", 1.2]})
            m.stopModule()
        except:
            m.stopModule()
            self.assertTrue(False)

    def test_JSON_2(self) -> None:
        """Test creating a Module from a JSON file bis."""
        try:
            m = Module(file="tests/test.json", silent=True)
            m2 = Module(file="tests/test2.json", silent=True)
            self.assertTrue(m2.getValue("sender_1") == {"test": [10, 30, True], "test2": ["a", 1.2]})
            m.stopModule()
            m2.stopModule()
        except:
            m.stopModule()
            m2.stopModule()
            self.assertTrue(False)

    def test_communication_server(self) -> None:
        """Test communication server side."""
        try:
            m = Module(file="tests/test3_S.json", silent=True)
            m.stopModule()
        except:
            m.stopModule()
            self.assertTrue(False)

    def test_communication_client(self) -> None:
        """Test communication client side."""
        try:
            m = Module(file="tests/test3_L.json", silent=True)
            m.stopModule()
        except:
            m.stopModule()
            self.assertTrue(False)

    def test_communication(self) -> None:
        """Test communication between server and client."""
        try:
            m1 = Module(file="tests/test3_S.json", silent=True)
            m2 = Module(file="tests/test3_L.json", silent=True)
            self.assertTrue(m1.getValue("sender_1") == m2.getValue("sender_1"))
            m1.setValue("sender_1", {"test": [1, 1, False], "test2": ["a", 1.2]})
            self.assertTrue(m1.getValue("sender_1") == m2.getValue("sender_1"))
            m2.stopModule()
            m1.stopModule()
        except:
            m2.stopModule()
            m1.stopModule()
            self.assertTrue(False)

    def test_communication_advanced(self) -> None:
        """Test communication between server and client advanced."""
        try:
            import time

            m1 = Module(file="tests/test3_S.json", silent=True)
            m2 = Module(file="tests/test3_L.json", silent=True)
            self.assertTrue(m1.getValue("sender_1") == m2.getValue("sender_1"))
            m1.stopModule()
            self.assertTrue(m2.getValue("sender_1") is None)
            time.sleep(0.5)
            m1.restartModule("sender_1")
            time.sleep(0.5)
            self.assertTrue(m1.getValue("sender_1") == m2.getValue("sender_1"))
            m1.stopModule()
            m2.stopModule()
        except:
            m1.stopModule()
            m2.stopModule()
            self.assertTrue(False)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIRONBark)
    testResult = unittest.TextTestRunner(verbosity=2).run(suite)
