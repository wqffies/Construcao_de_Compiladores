.section .bss

.section .text
.globl _start
fib:
push %rbp
sub $8, %rsp
mov %rsp, %rbp
mov $0, %rax
mov %rax, 0(%rbp)
mov 24(%rbp), %rax
push %rax
mov $2, %rax
pop %rbx
xor %rcx, %rcx
cmp %rax, %rbx
setl %cl
mov %rcx, %rax
cmp $0, %rax
jz Lfalso0
mov $1, %rax
mov %rax, 0(%rbp)
jmp Lfim0
Lfalso0:
mov 24(%rbp), %rax
push %rax
mov $1, %rax
pop %rbx
sub %rbx, %rax
push %rax
call fib
add $8, %rsp
push %rax
mov 24(%rbp), %rax
push %rax
mov $2, %rax
pop %rbx
sub %rbx, %rax
push %rax
call fib
add $8, %rsp
pop %rbx
add %rbx, %rax
mov %rax, 0(%rbp)
Lfim0:
mov 0(%rbp), %rax
add $8, %rsp
pop %rbp
ret

_start:
mov $6, %rax
push %rax
call fib
add $8, %rsp
call imprime_num
call sair
.include "runtime.s"
