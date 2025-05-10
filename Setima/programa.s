  #
  # modelo de saida para o compilador
  #

  .section .text
  .globl _start

_start:
  ## saida do compilador deve ser inserida aqui
mov $10, %rax
push %rax
mov $5, %rax
pop %rbx
add %rbx, %rax

push %rax
mov $3, %rax
pop %rbx
add %rbx, %rax


  call imprime_num
  call sair

  .include "runtime.s"
