# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824

from arvore_sintatica_atividade9 import (tokenizar, analisar, interpretar, Const, Var, OpBin, Declaracao, ProgramaCmd, Atrib, If, While, Return)

label_counter = 0

def new_label(prefix):
    global label_counter
    label = f"{prefix}{label_counter}"
    label_counter += 1
    return label

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
        elif arvore.operador == '==':
            codigo += (
                "xor %rcx, %rcx\n"
                "cmp %rax, %rbx\n"
                "setz %cl\n"
                "mov %rcx, %rax\n"
            )
        elif arvore.operador == '<':
            codigo += (
                "xor %rcx, %rcx\n"
                "cmp %rax, %rbx\n"
                "setl %cl\n"
                "mov %rcx, %rax\n"
            )
        elif arvore.operador == '>':
            codigo += (
                "xor %rcx, %rcx\n"
                "cmp %rax, %rbx\n"
                "setg %cl\n"
                "mov %rcx, %rax\n"
            )
        else:
            raise ValueError(f"Operador desconhecido: {arvore.operador}")

        return codigo

    elif isinstance(arvore, Declaracao):
        # Adiciona variável ao conjunto de declaradas
        variaveis.add(arvore.var)
        codigo_exp = gerarCodigo(arvore.exp, variaveis)
        return f".lcomm {arvore.var}, 8\n{codigo_exp}\nmov %rax, {arvore.var}\n"

    elif isinstance(arvore, Atrib):
        if arvore.var not in variaveis:
            raise NameError(f"Variável não declarada: {arvore.var}")
        codigo_exp = gerarCodigo(arvore.exp, variaveis)
        return f"{codigo_exp}\nmov %rax, {arvore.var}\n"

    elif isinstance(arvore, If):
        false_label = new_label("Lfalso")
        end_label = new_label("Lfim")
        codigo_cond = gerarCodigo(arvore.condicao, variaveis)
        codigo_entao = "\n".join(gerarCodigo(cmd, variaveis) for cmd in arvore.entao)
        codigo_senao = "\n".join(gerarCodigo(cmd, variaveis) for cmd in arvore.senao) if arvore.senao else ""

        return (
            f"{codigo_cond}\n"
            f"cmp $0, %rax\n"
            f"jz {false_label}\n"
            f"{codigo_entao}\n"
            f"jmp {end_label}\n"
            f"{false_label}:\n"
            f"{codigo_senao}\n"
            f"{end_label}:\n"
        )

    elif isinstance(arvore, While):
        start_label = new_label("Linicio")
        end_label = new_label("Lfim")
        codigo_cond = gerarCodigo(arvore.condicao, variaveis)
        codigo_corpo = "\n".join(gerarCodigo(cmd, variaveis) for cmd in arvore.corpo)

        return (
            f"{start_label}:\n"
            f"{codigo_cond}\n"
            f"cmp $0, %rax\n"
            f"jz {end_label}\n"
            f"{codigo_corpo}\n"
            f"jmp {start_label}\n"
            f"{end_label}:\n"
        )

    elif isinstance(arvore, Return):
        return gerarCodigo(arvore.exp, variaveis)

    elif isinstance(arvore, ProgramaCmd):
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

        # Gera código para os comandos
        for cmd in arvore.comandos:
            codigo_text += gerarCodigo(cmd, variaveis) + "\n"

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
    programa_cmd = """
    x = 5;
    y = 2;
    {
        if x > y {
            y = y + 10;
        } else {
            while y < x {
                y = y + 1;
            }
        }
        return x;
    }
    """

    arvore_cmd = analisar(programa_cmd)
    print("\nCódigo Gerado:")
    print(gerarCodigo(arvore_cmd))