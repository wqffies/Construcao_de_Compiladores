  #
  # modelo de saida para o compilador
  #

  .section .text
  .globl _start

_start:
  ## saida do compilador deve ser inserida aqui
.section .bss
.lcomm x, 8
.lcomm y, 8

.section .text
.globl _start
_start:
mov $10, %rax
push %rax
mov $6, %rax
pop %rbx
sub %rax, %rbx

mov %rax, x
mov x, %rax
push %rax
mov $5, %rax
pop %rbx
add %rbx, %rax

mov %rax, y
mov y, %rax
call imprime_num
call sair
.include "runtime.s"

  call imprime_num
  call sair

  .include "runtime.s"
