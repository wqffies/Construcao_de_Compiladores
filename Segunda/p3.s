  #
  # modelo de saida para o compilador
  #

  .section .text
  .globl _start

_start:
  MOV $72, %rax
  SUB $101, %rax
  MOV $4, %rbx
  IMUL %rbx
  MOV %rax, %rbx
  MOV $14, %rax
  MOV $77, %rcx
  IMUL %rcx
  ADD %rbx, %rax


  call imprime_num
  call sair

  .include "runtime.s"
  
