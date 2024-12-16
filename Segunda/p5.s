  #
  # modelo de saida para o compilador
  #

  .section .text
  .globl _start

_start:
  MOV $512, %rax
  MOV $65, %rbx
  IMUL %rbx
  MOV %rax, %rbx
  MOV $5657, %rax
  MOV $23, %rcx
  IMUL %rcx
  SUB %rax, %rbx
  MOV %rbx, %rax

  call imprime_num
  call sair

  .include "runtime.s"
  
