# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824
from arvore_sintatica_atividade8 import tokenizar, analisar, interpretar, imprimir_arvore_centralizada, Const, OpBin, Var, Declaracao, Programa

def gerarCodigo(arvore):
    variaveis = set()
    codigo_bss = ""
    
    def gerar(no):
        nonlocal codigo_bss, variaveis
        
        if isinstance(no, Const):
            return f"mov ${no.valor}, %rax"
        elif isinstance(no, Var):
            if no.nome not in variaveis:
                raise NameError(f"Variável não declarada: {no.nome}")
            return f"mov {no.nome}, %rax"
        elif isinstance(no, OpBin):
            codigo_esq = gerar(no.op_esq)
            codigo_dir = gerar(no.op_dir)
            
            codigo = (
                f"{codigo_esq}\n"
                f"push %rax\n"
                f"{codigo_dir}\n"
                f"pop %rbx\n"
            )
            
            if no.operador == '+':
                codigo += "add %rbx, %rax\n"
            elif no.operador == '-':
                codigo += "sub %rbx, %rax\n"
            elif no.operador == '*':
                if isinstance(no.op_dir, Const):
                    return f"{codigo_esq}\nimul ${no.op_dir.valor}, %rax\n"
                elif isinstance(no.op_esq, Const):
                    return f"{codigo_dir}\nimul ${no.op_esq.valor}, %rax\n"
                codigo += "imul %rbx, %rax\n"
            elif no.operador == '/':
                codigo += "xchg %rax, %rbx\ncqo\nidiv %rbx\n"
            else:
                raise ValueError(f"Operador desconhecido: {no.operador}")
            
            return codigo
        elif isinstance(no, Declaracao):
            variaveis.add(no.var)
            codigo_exp = gerar(no.exp)
            codigo_bss += f".lcomm {no.var}, 8\n"
            return f"{codigo_exp}\nmov %rax, {no.var}\n"
        else:
            raise ValueError(f"Tipo de nó desconhecido: {type(no)}")
    
    # Processa o programa principal
    if isinstance(arvore, Programa):
        codigo_decls = []
        for decl in arvore.declaracoes:
            codigo_decls.append(gerar(decl))
        
        codigo_exp_final = gerar(arvore.resultado)
        
        return (
            f".section .bss\n"
            f"{codigo_bss}\n"
            f".section .text\n"
            f".globl _start\n"
            f"_start:\n"
            f"{''.join(codigo_decls)}\n"
            f"{codigo_exp_final}\n"
            f"call imprime_num\n"
            f"call sair\n"
            f'.include "runtime.s"'
        )
    else:
        return gerar(arvore)

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
        
 