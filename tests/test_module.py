'''
File: test_module.py
Created Date: Wednesday, July 3rd 2020, 9:08:42 pm
Author: Zentetsu

----

Last Modified: Wed Oct 18 2023
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
'''

# import sys
# sys.path.insert(0, "../")

from IRONbark.Module import Module
import contextlib

def test_creation():
    print("Create Module instance:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test0")
            assert m.getLSName() == ([], [])
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_addSender():
    print("Add Sender to Module:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test1")
            m.addSender("name0", value=10)
            assert m.getValue("name0") == 10
            assert m["name0"][0] == 10
            m.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_addListener():
    print("Add Listener to Module without Sender:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test2")
            m.addListener("name1")
            assert m.getValue("name1") == None
            assert m["name1"][0] == None
            m.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_addListener_2():
    print("Add Listener to Module with Sender:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test3")
            m.addSender("name2", value=10)
            m2 = Module("test3b")
            m2.addListener("name2")
            assert m2.getValue("name2") == 10
            assert m2["name2"][0] == 10
            m.stopModule()
            m2.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_restart():
    print("Restarting Sender from Module:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test4")
            m.addSender("name3", value=10)
            m.restartModule("name3")
            m.stopModule()
        assert True
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_stopStart():
    print("Restarting Sender from Module bis:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test5")
            m.addSender("name4", value=10)
            m.stopModule("name4")
            m.startModule("name4")
            m.stopModule()
        assert True
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_setValue():
    print("Sender edit value:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test7")
            m.addSender("name5", value=10)
            m.setValue("name5", 20)
            assert m.getValue("name5") == 20
            assert m["name5"][0] == 20
            m.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_setValue_2():
    print("Sender edit value bis:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test8a")
            m.addSender("name6", value=10)
            m2 = Module("test8b")
            m2.addListener("name6")
            m.setValue("name6", 20)
            assert m2.getValue("name6") == 20
            assert m2["name6"][0] == 20
            m.stopModule()
            m2.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_setValue_3():
    print("Listener edit value:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test9a")
            m.addSender("name7", value=10)
            m2 = Module("test9b")
            m2.addListener("name7")
            m2.setValue("name7", 20)
            assert m.getValue("name7") == 20
            assert m2["name7"][0] == 20
            m.stopModule()
            m2.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_delSender():
    print("Removing Sender:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test10")
            m.addSender("name8", value=10)
            _s, _ = m.getLSName()
            assert len(_s) == 1
            m.delSender("name8")
            _s, _ = m.getLSName()
            assert len(_s) == 0
            m.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_delListener():
    print("Removing Listener:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test11a")
            m2 = Module("test11b")
            m.addSender("name9", value=10)
            m2.addListener("name9")
            _, _l = m2.getLSName()
            assert len(_l) == 1
            m2.delListener("name9")
            _, _l = m2.getLSName()
            assert len(_l) == 0
            m.stopModule()
            m2.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_():
    print("Stopping Modules:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test12a")
            m2 = Module("test12b")
            m.addSender("name10", value=10)
            m2.addListener("name10")
            m.stopModule("name10")
            m.stopModule()
            m2.stopModule()
        assert True
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_availability():
    print("Testing availability:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test13")
            m.addSender("name11", value=10)
            assert m.getLSAvailability(sender=True) == ([True], [])
            m.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_availability_2():
    print("Testing availability bis:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module("test14a")
            m2 = Module("test14b")
            m.addSender("name12", value=10)
            m2.addListener("name12")
            assert m.getLSAvailability(sender=True) == ([True], [])
            assert m2.getLSAvailability(listener=True) == ([], [True])
            m.stopModule()
            m2.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_JSON():
    print("Creating Module from JSON file:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module(file="test.json")
            assert m.getValue("sender1") == {'test': [10, 30, True], 'test2': ['a', 1.2]}
            m.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False

def test_JSON_2():
    print("Creating Module from JSON file bis:", end=" ")
    try:
        with contextlib.redirect_stdout(None):
            m = Module(file="test.json")
            print(m["sender1"].getValue())
            m2 = Module(file="test2.json")
            assert m2.getValue("sender1") == {'test': [10, 30, True], 'test2': ['a', 1.2]}
            m.stopModule()
            m2.stopModule()
        print("SUCCESSED")
    except:
        print("FAILED")
        assert False


print("-"*10)
test_creation()
test_addSender()
test_addListener()
test_addListener_2()
test_restart()
test_stopStart()
test_setValue()
test_setValue_2()
test_setValue_3()
test_delSender()
test_delListener()
test_()
test_availability()
test_availability_2()
test_JSON()
test_JSON_2()
print("-"*10)