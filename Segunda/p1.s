  #
  # modelo de saida para o compilador
  #

  .section .text
  .globl _start

_start:
  MOV $8, %rax
  MOV $11, %rbx
  MUL %rbx
  MOV %rax, %rbx
  MOV $12, %rax
  MOV $9, %rcx
  MUL %rcx
  SUB %rax, %rbx
  MOV $112, %rax
  SUB $19, %rax
  ADD %rbx, %rax

  call imprime_num
  call sair

  .include "runtime.s"
  
