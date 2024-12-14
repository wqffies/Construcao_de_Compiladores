  #
  # modelo de saida para o compilador
  #

  .section .text
  .globl _start

_start:
    MOV $7, %rax       
    MOV $6, %rbx       
    MUL %rbx           
    MOV %rax, %rbx     
    MOV $5, %rax       
    MUL %rbx           
    MOV %rax, %rbx     
    MOV $4, %rax       
    MOV $3, %rcx       
    MUL %rcx           
    MOV %rax, %rcx     
    MOV $2, %rax       
    MUL %rcx           
    MOV %rax, %rcx     
    MOV $1, %rax       
    MUL %rcx           
    MOV %rax, %rcx     
    MOV %rbx, %rax     
    DIV %rcx           

  call imprime_num
  call sair

  .include "runtime.s"
  
