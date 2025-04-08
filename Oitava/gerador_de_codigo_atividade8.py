# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824
from arvore_sintatica_atividade8 import tokenizar, analisar, interpretar, imprimir_arvore_centralizada, Const, OpBin, Var, Declaracao, Programa

def gerarCodigo(arvore, variaveis=None):
    if variaveis is None:
        variaveis = set()

    if isinstance(arvore, Const):
        # Gera código para constante
        return f"mov ${arvore.valor}, %rax"

    elif isinstance(arvore, Var):
        if arvore.nome not in variaveis:
            raise NameError(f"Variável não declarada: {arvore.nome}")
        return f"mov {arvore.nome}, %rax"

    elif isinstance(arvore, OpBin):
        # Gera código para expressão binária
        codigo_esq = gerarCodigo(arvore.op_esq, variaveis)
        codigo_dir = gerarCodigo(arvore.op_dir, variaveis)

        codigo = (
            f"{codigo_esq}\n"
            f"push %rax\n"
            f"{codigo_dir}\n"
            f"pop %rbx\n"
        )

        if arvore.operador == '+':
            codigo += "add %rbx, %rax\n"
        elif arvore.operador == '-':
            codigo += "sub %rbx, %rax\n"
        elif arvore.operador == '*':
            codigo += "imul %rbx, %rax\n"
        elif arvore.operador == '/':
            codigo += "xchg %rax, %rbx\ncqo\nidiv %rbx\n"
        else:
            raise ValueError(f"Operador desconhecido: {arvore.operador}")

        return codigo

    elif isinstance(arvore, Declaracao):
        # Adiciona variável ao conjunto de declaradas
        variaveis.add(arvore.var)
        codigo_exp = gerarCodigo(arvore.exp, variaveis)
        return f".lcomm {arvore.var}, 8\n{codigo_exp}\nmov %rax, {arvore.var}\n"

    elif isinstance(arvore, Programa):
        # Gera código para o programa completo
        codigo_bss = ""
        codigo_text = ""

        for decl in arvore.declaracoes:
            codigo = gerarCodigo(decl, variaveis)
            # Se houver declaração, ela gera parte de .bss e .text ao mesmo tempo
            linhas = codigo.splitlines()
            bss_linha = linhas[0] if linhas[0].startswith(".lcomm") else ""
            text_linhas = "\n".join(linhas[1:]) if bss_linha else codigo

            if bss_linha:
                codigo_bss += bss_linha + "\n"
            codigo_text += text_linhas + "\n"

        codigo_resultado = gerarCodigo(arvore.resultado, variaveis)

        return (
            ".section .bss\n"
            f"{codigo_bss}\n"
            ".section .text\n"
            ".globl _start\n"
            "_start:\n"
            f"{codigo_text}"
            f"{codigo_resultado}\n"
            "call imprime_num\n"
            "call sair\n"
            '.include "runtime.s"'
        )

    else:
        raise ValueError(f"Tipo de nó desconhecido: {type(arvore)}")


if __name__ == "__main__":    
    programa_ev = """
    x = (7 + 4) * 12;
    y = x * 3 + 11;
    = (x * y) + (x * 11) + (y * 13)
    """ 
    # Análise do programa EV
    arvore_ev = analisar(programa_ev)
        
    print("\nÁrvore Sintática (AST):")
    imprimir_arvore_centralizada(arvore_ev)
        
    print("\nCódigo Assembly Gerado:")
    codigo_ev = gerarCodigo(arvore_ev)
    print(codigo_ev)
        
 