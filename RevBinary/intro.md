## Debut du commencement

- Binary Exploitation

First off what's a binary?

A binary is compiled code. When a programmer writes code in a language like C, the C code isn't what gets actually ran. It is compiled into a binary and the binary is run. Binary exploitation is the process of actually exploiting a binary, but what does that mean?
In a lot of code, you will find bugs. Think of a bug as a mistake in code that will allow for unintended functionality. As an attacker we can leverage this bug to attack the binary, and actually force it to do what we want by getting code execution. That means we actually have the binary execute code that we say, and can essentially hack the code.

- Reverse Engineering

What is reverse engineering?

Reverse engineering is the process of figuring out how something works. It is a critical part of binary exploitation, since most of the time you are just handed a binary without any clue as to what it does. You have to figure out how it works, so you can attack it.s

- Objective

Most of the time, your objective is to obtain code execution on a box and pop a shell. If you have a different objective, it will usually be stated on the top line of the writeup. In almost every instance where your objective isn't to pop a shell, it's to some get ctf flag associated with this challenge, from the binary.

- Why CTF Challenges?

The reason why I went with ctf challenges for teaching binary exploitation / reverse engineering, is because most challenges only contains a small subset of exploitation knowledge. With that I can split it up into different subjects like buffer overflow into calling shellcode and fast bin exploitation, so it can be covered like a somewhat normal course.

## Assembly

**Registers**
Registers are essentialy places that the processor can store memory
```
rbp: Base Pointer, points to the bottom of the current stack frame
rsp: Stack Pointer, points to the top of the current stack frame
rip: Instruction Pointer, points to the instruction to be executed

General Purpose Registers
These can be used for a variety of different things
rax:
rbx:
rcx:
rdx:
rsi:
rdi:
r8:
r9:
r10:
r11:
r12:
r13:
r14:
r15:

```
In x64 linux arguments to a function are passed via registers. The first few args are passed by these registers:
```
rdi:    First Argument
rsi:    Second Argument
rdx:    Third Argument
rcx:    Fourth Argument
r8:     Fifth Argument
r9:     Sixth Argument
```
With the x86 elf architecture, arguments are passed on the stack. Also one thing as you may know, in C function can return a value. In x64, this value is passed in the rax register. In x86 this value is passed in the eax register.

**Words**
You might hear the term word throughout this. A word is just two bytes of data. A dword is four bytes of data. A qword is eight bytes of data.

**Stacks**
Now one of the most common memory regions you will be dealing with is the stack. It is where local variables in the code are stored.
For instance, in this code the variable x is stored in the stack:
```
#include <stdio.h>

void main(void)
{
    int x = 5;
    puts("hi");
}

```
Specifically we can see it is stored on the stack at `rbp-0x4`.
```
[0x00001050]> pdf@main
            ; DATA XREF from entry0 @ 0x1064
┌ 33: int main (int argc, char **argv, char **envp);
│           ; var int64_t var_4h @ rbp-0x4
│           0x00001139      55             push rbp
│           0x0000113a      4889e5         mov rbp, rsp
│           0x0000113d      4883ec10       sub rsp, 0x10
│           0x00001141      c745fc050000.  mov dword [var_4h], 5
│           0x00001148      488d05b50e00.  lea rax, [0x00002004]       ; "hi"
│           0x0000114f      4889c7         mov rdi, rax                ; const char *s
│           0x00001152      e8d9feffff     call sym.imp.puts           ; int puts(const char *s)
│           0x00001157      90             nop
│           0x00001158      c9             leave
└           0x00001159      c3             ret

```
Now values on the stack are moved on by either pushing them onto the stack, or popping them off. That is the only way to add or remove values from the stack (it is a LIFO data structure). However we can reference values on the stack.

The exact bounds of the stack is recorded by two registers, rbp and rsp. The base pointer rbp points to the bottom of the stack. The stack pointer rsp points to the top of the stack.

## Instructions
- mov :
The move instruction just moves data from one register to another. For instance:
`mov rax, rdx`
This will just move the data from the `rdx` register to the `rax` register.

- dereference

If you ever see brackets like [], they are meant to dereference, which deals with pointers. A pointer is a value that points to a particular memory address (it is a memory address). Dereferencing a pointer means to treat a pointer like the value it points to. For instance:
`mov rax, [rdx]` 
Will move the value pointed to by `rdx` into the `rax` register. On the flipside:
`mov [rax], rdx`
Will move the value of the `rdx` register into whatever memory is pointed to by the `rax` register. The actual value of the `rax` register does not change.

- Lea
The `lea` instruction calculates the address of the second operand, and moves that address in the first. For instance:
`lea rdi, [rbx+0x10]`
This will move the address `rbx+0x10` into the `rdi` register.

- add
This just adds the two values together, and stores the sum in the first argument. For instance:
That will set `rax` equal to `rax + rdx`

- sub
This value will subtract the second operand from the first one, and store the difference in the first argument. For instance:
`sub rsp, 0x10`
This will set the `rsp` register equal to `rsp - 0x10`

- xor
This will perform the binary operation xor on the two arguments it is given, and stores the result in the first operation:
`xor rdx, rax`
that will set the `rdx` register equal to `rdx ^ rax`
The and and or operations essentially do the same thing, except with the and or or binary operators.

- push 
The `push` instruction will grow the stack by either 8 bytes (for x64, 4 for x86), then push the contents of a register onto the new stack space. For instance:
`push rax`
This will grow the stack by 8 bytes, and the contents of the rax register will be on top of the stack.

- pop 
The `pop` instruction will pop the top 8 bytes (for x64, 4 for x86) off of the stack and into the argument. Then it will shrink the stack. For instance:
`pop rax`
The top 8 bytes of the stack will end up in the `rax` register.

- jmp
The `jmp` instruction will jump to an instruction address. It is used to redirect code execution. For instance:
`jmp 0x602010`
That instruction will cause the code execution to jump to `0x602010`, and execute whatever instruction is there.

- call & ret

This is similar to the `jmp` instruction. The difference is it will push the values of rbp and rip onto the stack, then jump to whatever address it is given. This is used for calling functions. After the function is finished, a `ret` instruction is called which uses the pushed values of `rbp` and `rip` (saved base and instruction pointers) it can continue execution right where it left off

- cmp
The cmp instruction is similar to that of the sub instruction. Except it doesn't store the result in the first argument. It checks if the result is less than zero, greater than zero, or equal to zero. Depending on the value it will set the flags accordingly.

- jnz / jz
This jump if not zero and jump if zero (jnz/jz) instructions are pretty similar to the jump instruction. The difference is they will only execute the jump depending on the status of the zero flag. For jz it will only jump if the zero flag is set. The opposite is true for jnz.