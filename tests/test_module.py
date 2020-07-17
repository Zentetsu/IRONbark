'''
File: test_module.py
Created Date: Wednesday, July 3rd 2020, 9:08:42 pm
Author: Zentetsu

----

Last Modified: Fri Jul 17 2020
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
2020-07-08	Zen	Creating file
'''


# from context import Module
from IRON.Module import Module

def test_error_None():
    m = Module("test0")
    print(m)
    assert m.getLSName() == ([], [])

def test_add_sender():
    m = Module("test1")
    m.addSender("name", value=10)
    print(m)
    assert m.getValue("name") == 10
    m.stopModule()

def test_add_listener():
    m = Module("test2")
    try:
        m.addListener("name")
        print(m)
        m.stopModule()
        assert False
    except:
        assert True

def test_add_listener2():
    m = Module("test3a")
    m.addSender("name", value=10)
    print(m)
    m2 = Module("test3b")
    m2.addListener("name")
    print(m2)
    assert m2.getValue("name") == 10
    m.stopModule()
    m2.stopModule()

def test_restart():
    m = Module("test4")
    m.addSender("name", value=10)
    print(m)
    try:
        m.restartModule("name")
        m.stopModule()
        assert True
    except:
        assert False

def test_stop_start():
    m = Module("test5")
    m.addSender("name", value=10)
    print(m)
    try:
        m.stopModule("name")
        m.startModule("name")
        m.stopModule()
        assert True
    except:
        assert False

def test_stop_start2():
    m = Module("test6")
    m.addSender("name", value=10)
    print(m)
    try:
        m.stopModule()
        m.startModule()
        m.stopModule()
        assert True
    except:
        assert False

def test_setValue():
    m = Module("test7")
    m.addSender("name", value=10)
    print(m)
    m.setValue("name", 20)
    print(m)
    assert m.getValue("name") == 20
    m.stopModule()

def test_setValue2():
    m = Module("test8a")
    m.addSender("name", value=10)
    print(m)
    m2 = Module("test8b")
    m2.addListener("name")
    print(m2)
    m.setValue("name", 20)
    print(m)
    print(m2)
    assert m2.getValue("name") == 20
    m.stopModule()
    m2.stopModule()

def test_setValue3():
    m = Module("test9a")
    m.addSender("name", value=10)
    print(m)
    m2 = Module("test9b")
    m2.addListener("name")
    print(m2)
    m2.setValue("name", 20)
    print(m)
    print(m2)
    assert m.getValue("name") == 20
    m.stopModule()
    m2.stopModule()

def test_del_sender():
    m = Module("test10")
    m.addSender("name", value=10)
    print(m)
    _s, _ = m.getLSName()
    assert len(_s) == 1
    m.delSender("name")
    print(m)
    _s, _ = m.getLSName()
    assert len(_s) == 0
    m.stopModule()

def test_del_listener():
    m = Module("test11a")
    m2 = Module("test11b")
    m.addSender("name", value=10)
    m2.addListener("name")
    print(m)
    print(m2)
    _, _l = m2.getLSName()
    assert len(_l) == 1
    m2.delListener("name")
    print(m2)
    _, _l = m2.getLSName()
    assert len(_l) == 0
    m.stopModule()
    m2.stopModule()

test_error_None()
print("----------------")
test_add_sender()
print("----------------")
test_add_listener()
print("----------------")
test_add_listener2()
print("----------------")
test_restart()
print("----------------")
test_stop_start()
print("----------------")
test_stop_start2()
print("----------------")
test_setValue()
print("----------------")
test_setValue2()
print("----------------")
test_setValue3()
print("----------------")
test_del_sender()
print("----------------")
test_del_listener()
print("----------------")