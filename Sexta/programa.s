  #
  # modelo de saida para o compilador
  #

  .section .text
  .globl _start

_start:
  ## saida do compilador deve ser inserida aqui
  mov $3, %rax
  push %rax
  mov $6, %rax
  push %rax
  mov $40, %rax
  push %rax
  mov $5, %rax
  pop %rbx
  imul %rbx, %rax
  pop %rbx
  add %rbx, %rax
  pop %rbx
  xchg %rax, %rbx
  cqo
  idiv %rbx

  call imprime_num
  call sair

  .include "runtime.s"
