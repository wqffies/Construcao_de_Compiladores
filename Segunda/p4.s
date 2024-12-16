  #
  # modelo de saida para o compilador
  #

  .section .text
  .globl _start

_start:
  MOV $7374, %rax
  MOV $657, %rbx
  IMUL %rbx
  MOV %rax, %rbx
  MOV $13121517, %rax
  MOV $256, %rcx
  IMUL %rcx
  ADD %rbx, %rax
  MOV $4294979641, %rbx
  ADD %rbx, %rax

  call imprime_num
  call sair

  .include "runtime.s"
  
