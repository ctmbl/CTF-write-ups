from pwn import *

def puntil(proc, b):
    print(proc.recvuntil(b).strip().decode())