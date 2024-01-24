## Gnu Debugger Introduction

Nous commencons avec : gdb-gef
Gef is designed to give us some extended features

https://github.com/hugsy/gef

In order to enter debugger mode, we can set breakpoints. Breakpoints are places in the program where GDB will know to stop execution to allow you to examine the contents of the stack. The most common breakpoint to set is on main, which we can set with `break main`

Now you can step through the function by typing 'nexti' until the program ends. 'nexti' will have you go instruction by intruction through the program, but will not step into function calls such as puts.

Other ways to navigate a program are:

-    'next' - which will take you through one line of code, but will step over function calls such as puts.
-    'step' - which will take you through one line of code, but will step into function calls
-    'stepi' - whch will take you through one instruction at a time, stepping into function calls

Also we can disassemble like the `objdump`
```
(gdb) disassemble main
Dump of assembler code for function main:
   0x080483fb <+0>:	lea    0x4(%esp),%ecx
   0x080483ff <+4>:	and    $0xfffffff0,%esp
   0x08048402 <+7>:	push   -0x4(%ecx)
   0x08048405 <+10>:	push   %ebp
   0x08048406 <+11>:	mov    %esp,%ebp
   0x08048408 <+13>:	push   %ecx
=> 0x08048409 <+14>:	sub    $0x4,%esp
   0x0804840c <+17>:	sub    $0xc,%esp
   0x0804840f <+20>:	push   $0x80484b0
   0x08048414 <+25>:	call   0x80482d0 <puts@plt>
   0x08048419 <+30>:	add    $0x10,%esp
   0x0804841c <+33>:	mov    $0x0,%eax
   0x08048421 <+38>:	mov    -0x4(%ebp),%ecx
   0x08048424 <+41>:	leave
   0x08048425 <+42>:	lea    -0x4(%ecx),%esp
   0x08048428 <+45>:	ret
End of assembler dump.
```
Now if we want to break in a functions like `puts`,  we need just to add the `b *0x80482d0`

```
(gdb) b *0x80482d0
Breakpoint 2 at 0x80482d0


```