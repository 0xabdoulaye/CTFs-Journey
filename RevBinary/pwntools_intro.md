Pwntools for Beginner from rootme
- Pwntools is a CTF framework and exploit development library. Written in Python, it is designed for rapid prototyping and development, and intended to make exploit writing as simple as possible
- The other tool we will be using is pwndbg, which is "a GDB plug-in that makes debugging with GDB suck less, with a focus on features needed by low-level software developers, hardware hackers, reverse-engineers and exploit developers" (pwndbg Github page). If you have ever used gdb for binary exploitation, you know it can be cumbersome. Pwndbg prints out useful information, such as registers and assembly code, with each breakpoint or error, making debugging and dynamic analysis easier. To install it, you can refer to the Github page. All you need to do is download it from Github and run the setup script, and it will automatically attach to gdb.

https://github.com/dizmascyberlabs/IntroToPwntools

- **Checksec 
```
└─# file intro2pwn1 
intro2pwn1: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=854d5bf88e74196ffe8a6aeba2178bc43d413e65, not stripped
                                                                                                                              
┌──(root㉿xXxX)-[/home/…/RevBinary/IntroToPwntools/IntroToPwntools/checksec]
└─# file intro2pwn2 
intro2pwn2: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=6d7e247fd7eb58c0fb79a2dbec119416edff8884, not stripped

└─# checksec --file=intro2pwn1 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified    Fortifiable      FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   69 Symbols        No    0            2intro2pwn1
                                                                                                                              
┌──(root㉿xXxX)-[/home/…/RevBinary/IntroToPwntools/IntroToPwntools/checksec]
└─# checksec --file=intro2pwn2 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified    Fortifiable      FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   65 Symbols        No    0            2intro2pwn2
```

As you can see, these binaries both have the same architecture (i386-32-little), but differ in qualities such as RELRO, Stack canaries , NX, PIE, and RWX. Now, what are these qualities? Allow me to explain. Please note, this room does not require a deep knowledge of these beyond the basics.

- `RELRO` stands for Relocation Read-Only, which makes the global offset table (GOT) read-only after the linker resolves functions to it. The GOT is important for techniques such as the ret-to-libc attack, although this is outside the scope of this room.
- `Stack canaries` are tokens placed after a stack to detect a stack overflow. These were supposedly named after birds that coal miners brought down to mines to detect noxious fumes. Canaries were sensitive to the fumes, and so if they died, then the miners knew they needed to evacuate. On a less morbid note, stack canaries sit beside the stack in memory (where the program variables are stored), and if there is a stack overflow, then the canary will be corrupted. This allows the program to detect a buffer overflow and shut down. You can read more about stack canaries here: https://www.sans.org/blog/stack-canaries-gingerly-sidestepping-the-cage/.
- `NX` is short for non-executable. If this is enabled, then memory segments can be either writable or executable, but not both. This stops potential attackers from injecting their own malicious code (called shellcode) into the program, because something in a writable segment cannot be executed.  On the vulnerable binary, you may have noticed the extra line RWX that indicates that there are segments which can be read, written, and executed. See this Wikipedia article for more details: https://en.wikipedia.org/wiki/Executable_space_protection
- PIE stands for Position Independent Executable. This loads the program dependencies into random locations, so attacks that rely on memory layout are more difficult to conduct. Here is a good blog about this: https://access.redhat.com/blogs/766093/posts/1975793

If you want a good overview of each of the checksec tested qualities, I have found this guide to be useful: https://blog.siphos.be/2011/07/high-level-explanation-on-some-binary-executable-security/

- **Cyclic**
Vulnerable code:
```
void start(){
        char name[24];
        gets(name);
}

```	
This is vulnerable to bufferoverflow because of `gets` function
https://faq.cprogramming.com/cgi-bin/smartfaq.cgi?answer=1049157810&id=1043284351
on gdb you can use `r < file` to run a file
To generate buffer pattern use cyclic
```
>>> from pwn import *
>>> cyclic(100)
b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa'
>>> 
```