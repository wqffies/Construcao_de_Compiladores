# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824
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
            codigo += "sub %rbx, %rax\n"
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
if __name__ == "__main__":
    # exemplo de impressão do programa
    entrada = "(3 / (6 + (40 * 5)))"
    tokens = tokenizar(entrada)
    arvore = analisar(tokens)

    print("Árvore Sintática (AST):")
    imprimir_arvore_centralizada(arvore)

    codigo = gerarCodigo(arvore)
    print("Codigo resultante:",codigo)