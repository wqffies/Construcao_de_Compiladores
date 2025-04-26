# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824

from arvore_sintatica_atividade9 import (tokenizar, analisar, interpretar, Const, Var, OpBin, Declaracao, ProgramaCmd, Atrib, If, While, Return)

def gerarCodigo(arvore, variaveis=None, _lbl=[0]):
    if variaveis is None:
        variaveis = set()

    def new_label(prefix):
        n = _lbl[0]
        _lbl[0] += 1
        return f"L{prefix}{n}"

    if isinstance(arvore, Const):
        return f"mov ${arvore.valor}, %rax\n"

    if isinstance(arvore, Var):
        if arvore.nome not in variaveis:
            raise NameError(f"Variável não declarada: {arvore.nome}")
        return f"mov {arvore.nome}, %rax"

    if isinstance(arvore, OpBin):
        codigo_esq = gerarCodigo(arvore.op_esq, variaveis, _lbl)
        codigo_dir = gerarCodigo(arvore.op_dir, variaveis, _lbl)
        seq = [
            codigo_esq,
            "push %rax",
            codigo_dir,
            "pop %rbx"
        ]
        op = arvore.operador
        if op == '+':
            seq.append("add %rbx, %rax")
        elif op == '-':
            seq.append("sub %rbx, %rax")
            seq.append("neg %rax")  
        elif op == '*':
            seq.append("imul %rbx, %rax")
        elif op == '/':
            seq.append("xchg %rax, %rbx")
            seq.append("cqo")
            seq.append("idiv %rbx")
        elif op in ('==', '<', '>'):
            inst = {'==': 'setz', '<': 'setl', '>': 'setg'}[op]
            seq.extend([
                "xor %rcx, %rcx",
                "cmp %rax, %rbx",
                f"{inst} %cl",
                "mov %rcx, %rax"
            ])
        else:
            raise ValueError(f"Operador desconhecido: {op}")
        return "\n".join(seq) + "\n"

    if isinstance(arvore, Declaracao):
        variaveis.add(arvore.var)
        codigo_exp = gerarCodigo(arvore.exp, variaveis, _lbl)
        return (
            f".lcomm {arvore.var}, 8\n"
            f"{codigo_exp}"
            f"mov %rax, {arvore.var}\n"
        )

    if isinstance(arvore, Atrib):
        if arvore.var not in variaveis:
            raise NameError(f"Variável não declarada: {arvore.var}")
        codigo_exp = gerarCodigo(arvore.exp, variaveis, _lbl)
        return (
            f"{codigo_exp}"
            f"mov %rax, {arvore.var}\n"
        )

    if isinstance(arvore, If):
        Lfalso = new_label("falso")
        Lfim = new_label("fim")
        seq = []
        seq.append(gerarCodigo(arvore.condicao, variaveis, _lbl))
        seq.append("mov %rax, %rax")
        seq.append(f"jz {Lfalso}")
        for cmd in arvore.entao:
            seq.append(gerarCodigo(cmd, variaveis, _lbl).rstrip())
        seq.append(f"jmp {Lfim}")
        seq.append(f"{Lfalso}:")
        for cmd in arvore.senao:
            seq.append(gerarCodigo(cmd, variaveis, _lbl).rstrip())
        seq.append(f"{Lfim}:")
        return "\n".join(seq) + "\n"

    if isinstance(arvore, While):
        Linicio = new_label("inicio")
        Lfim = new_label("fim")
        seq = []
        seq.append(f"{Linicio}:")
        seq.append(gerarCodigo(arvore.condicao, variaveis, _lbl))
        seq.append("mov %rax, %rax")
        seq.append(f"jz {Lfim}")
        for cmd in arvore.corpo:
            seq.append(gerarCodigo(cmd, variaveis, _lbl).rstrip())
        seq.append(f"jmp {Linicio}")
        seq.append(f"{Lfim}:")
        return "\n".join(seq) + "\n"

    if isinstance(arvore, Return):
        codigo_exp = gerarCodigo(arvore.exp, variaveis, _lbl)
        return (
            f"{codigo_exp}"
            "call imprime_num\n"
            "call sair\n"
        )

    if isinstance(arvore, ProgramaCmd):
        codigo_bss = []  
        codigo_text = []  

        for decl in arvore.declaracoes:
            part = gerarCodigo(decl, variaveis, _lbl).splitlines()
            if part[0].startswith(".lcomm"):  
                codigo_bss.append(part[0])
                codigo_text.extend(part[1:])  
            else:
                codigo_text.append(part)

        for cmd in arvore.comandos:
            codigo_text.append(gerarCodigo(cmd, variaveis, _lbl).rstrip())
        codigo_exp = gerarCodigo(arvore.resultado, variaveis, _lbl)
        codigo_text.append(codigo_exp)
        codigo_text.append("call imprime_num")  
        codigo_text.append("call sair")        
        return (
            ".section .bss\n"
            + "\n".join(codigo_bss) + "\n"
            + ".section .text\n"
            ".globl _start\n"
            "_start:\n"
            + "\n".join(codigo_text) + "\n"
            + '.include "runtime.s"\n'
        )

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