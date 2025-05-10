# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824

import sys
from arvore_sintatica_atividade7 import tokenizar, analisar, interpretar, imprimir_arvore_centralizada, Const, OpBin

def gerarCodigo(arvore):
    if isinstance(arvore, Const):
        # Caso base
        return f"mov ${arvore.valor}, %rax"
    elif isinstance(arvore, OpBin):
        codigo_esq = gerarCodigo(arvore.op_esq)  # Gera código para o operando esquerdo
        codigo_dir = gerarCodigo(arvore.op_dir)  # Gera código para o operando direito
        
        # Combina os códigos
        codigo = (
            f"{codigo_esq}\n"  
            f"push %rax\n"     # Salva o resultado do operando esquerdo na pilha
            f"{codigo_dir}\n"  
            f"pop %rbx\n"      # Recupera o resultado do operando esquerdo da pilha
        )
        
        # Adiciona a operação correspondente
        if arvore.operador == '+':
            codigo += "add %rbx, %rax\n"
        elif arvore.operador == '-':
            codigo += "sub %rax, %rbx\n"
            codigo += "mov %rbx, %rax\n"
        elif arvore.operador == '*':
            codigo += "imul %rbx, %rax\n"
        elif arvore.operador == '/':
            codigo += (
                "xchg %rax, %rbx\n"  # Troca RAX e RBX (agora RAX = esquerdo, RBX = direito)
                "cqo\n"              # Estende o sinal de RAX para RDX:RAX
                "idiv %rbx\n"        # Divide RDX:RAX por RBX, resultado em RAX
            )
        else:
            raise ValueError(f"Operador desconhecido: {arvore.operador}")
        
        return codigo
    else:
        raise ValueError(f"Tipo de nó desconhecido: {type(arvore)}")


def gerarProgramaCompleto(arvore):
    """Gera o programa assembly completo seguindo o modelo fornecido"""
    codigo_expressao = gerarCodigo(arvore)
    
    # CORRIGIDO: Formatação do cabeçalho sem espaços extras
    programa = f"""  #
  # modelo de saida para o compilador
  #

  .section .text
  .globl _start

_start:
  ## saida do compilador deve ser inserida aqui
{codigo_expressao}

  call imprime_num
  call sair

  .include "runtime.s"
"""
    return programa

def main():
    # Verifica se foi fornecido o arquivo de entrada
    if len(sys.argv) < 2:
        print("Uso: python atividade8.py arquivo_entrada.ec")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    
    try:
        # Lê o arquivo de entrada
        with open(arquivo_entrada, 'r') as f:
            entrada = f.read().strip()
        
        print(f"Expressão lida do arquivo: {entrada}")
        
        # Processa a expressão
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        
        print("\nÁrvore Sintática (AST):")
        imprimir_arvore_centralizada(arvore)
        
        # Gera o código assembly completo
        codigo_completo = gerarProgramaCompleto(arvore)
        
        # Determina o nome do arquivo de saída
        if arquivo_entrada.endswith('.ec'):
            arquivo_saida = arquivo_entrada.replace('.ec', '.s')
        else:
            arquivo_saida = arquivo_entrada + '.s'
        
        # Grava o arquivo de saída
        with open(arquivo_saida, 'w') as f:
            f.write(codigo_completo)
        
        print(f"\nCódigo assembly gerado com sucesso!")
        print(f"Arquivo de saída: {arquivo_saida}")
        
        print("\n--- Código Gerado ---")
        print(codigo_completo)
        
        # Também calcula e exibe o resultado para verificação
        resultado = interpretar(arvore)
        print(f"\n--- Resultado da Expressão ---")
        print(f"{entrada} = {resultado}")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()