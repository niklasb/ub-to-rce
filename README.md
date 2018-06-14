# Exploit-Demo zum Vortrag "Von UB zu RCE"

## Starten

```
LD_LIBRARY_PATH="$(pwd)" socat tcp4-l:4444,bind=127.0.0.1,reuseaddr,fork exec:./animals
```

Wenn es crasht unter Arch Linux versuchen, libc und ELF loader muessen
einigermassen zusammenpassen.

Mit

```
nc localhost 4444
```

verbinden.


## Debugging

Ich habe https://github.com/niklasb/gdbinit benutzt. `./setup.sh` installiert
eine Reihe von GDB scripts. Danach dann mit

```
gdb -ex peda -ex 'tcp 4444 ./animals' -ex c
```

starten.


## Exploit

Exploit benutzt https://github.com/niklasb/ctf-tools/tree/master/pwnlib:

```
git clone https://github.com/niklasb/ctf-tools
ln -s ctf-tools/pwnlib .
./pwn.py --dbg
```
