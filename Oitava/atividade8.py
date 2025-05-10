# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824

import sys
from arvore_sintatica_atividade8 import tokenizar, analisar, interpretar, imprimir_arvore_centralizada, Const, OpBin, Var, Declaracao, Programa

def gerarCodigo(arvore, variaveis=None):
    """Gera código assembly a partir de uma árvore sintática."""
    if variaveis is None:
        variaveis = set()  # Conjunto para armazenar variáveis declaradas

    # Caso base: Constante numérica
    if isinstance(arvore, Const):
        # Move o valor imediato para o registrador %rax
        return f"mov ${arvore.valor}, %rax"

    # Caso base: Variável
    elif isinstance(arvore, Var):
        # Verifica se a variável foi declarada
        if arvore.nome not in variaveis:
            raise NameError(f"Variável não declarada: {arvore.nome}")
        # Move o valor da variável da memória para %rax
        return f"mov {arvore.nome}, %rax"

    # Operação binária (+, -, *, /)
    elif isinstance(arvore, OpBin):
        # Gera código para os operandos esquerdo e direito
        codigo_esq = gerarCodigo(arvore.op_esq, variaveis)
        codigo_dir = gerarCodigo(arvore.op_dir, variaveis)

        # Estratégia:
        # 1. Calcula o operando esquerdo (resultado em %rax)
        # 2. Salva na pilha (push %rax)
        # 3. Calcula o operando direito (resultado em %rax)
        # 4. Recupera o primeiro operando da pilha para %rbx
        codigo = (
            f"{codigo_esq}\n"  # Calcula operando esquerdo
            f"push %rax\n"      # Salva resultado na pilha
            f"{codigo_dir}\n"   # Calcula operando direito
            f"pop %rbx\n"       # Recupera primeiro operando para %rbx
        )

        # Gera a instrução específica para cada operador
        if arvore.operador == '+':
            # Soma: %rax = %rbx + %rax
            codigo += "add %rbx, %rax\n"
        elif arvore.operador == '-':
            # Subtração CORRIGIDA: %rbx = %rbx - %rax (pois %rbx contém o primeiro operando)
            # Depois movemos o resultado para %rax
            codigo += "sub %rax, %rbx\n"
            codigo += "mov %rbx, %rax\n"
        elif arvore.operador == '*':
            # Multiplicação: %rax = %rbx * %rax
            codigo += "imul %rbx, %rax\n"
        elif arvore.operador == '/':
            # Divisão requer preparação especial:
            # 1. xchg troca %rax e %rbx (dividendo deve estar em %rax)
            # 2. cqo estende %rax para %rdx:%rax (para divisão com sinal)
            # 3. idiv divide %rdx:%rax por %rbx
            codigo += "xchg %rax, %rbx\ncqo\nidiv %rbx\n"
        else:
            raise ValueError(f"Operador desconhecido: {arvore.operador}")

        return codigo

    # Declaração de variável (atribuição)
    elif isinstance(arvore, Declaracao):
        # Adiciona a variável ao conjunto de declaradas
        variaveis.add(arvore.var)
        # Gera código para a expressão de atribuição
        codigo_exp = gerarCodigo(arvore.exp, variaveis)
        # Código assembly:
        # 1. .lcomm aloca espaço na seção .bss
        # 2. Código da expressão (em %rax)
        # 3. Armazena o resultado na variável
        return f".lcomm {arvore.var}, 8\n{codigo_exp}\nmov %rax, {arvore.var}\n"

    # Programa completo (lista de declarações + expressão final)
    elif isinstance(arvore, Programa):
        codigo_bss = ""   # Seção .bss (variáveis não inicializadas)
        codigo_text = ""  # Seção .text (código executável)

        # Processa cada declaração
        for decl in arvore.declaracoes:
            codigo = gerarCodigo(decl, variaveis)
            # Separa as linhas de código
            linhas = codigo.splitlines()
            # A primeira linha é a alocação na seção .bss (se existir)
            bss_linha = linhas[0] if linhas[0].startswith(".lcomm") else ""
            # O restante é código na seção .text
            text_linhas = "\n".join(linhas[1:]) if bss_linha else codigo

            if bss_linha:
                codigo_bss += bss_linha + "\n"
            codigo_text += text_linhas + "\n"

        # Gera código para a expressão resultado
        codigo_resultado = gerarCodigo(arvore.resultado, variaveis)

        # Monta o programa assembly completo
        return (
            ".section .bss\n"      # Seção para variáveis não inicializadas
            f"{codigo_bss}\n"       # Declarações de variáveis
            ".section .text\n"      # Seção de código
            ".globl _start\n"       # Ponto de entrada
            "_start:\n"
            f"{codigo_text}"        # Código das declarações
            f"{codigo_resultado}\n" # Código da expressão final
            "call imprime_num\n"    # Chama rotina para imprimir resultado
            "call sair\n"          # Finaliza o programa
            '.include "runtime.s"'  # Inclui biblioteca de runtime
        )

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
        print("Uso: python atividade8.py arquivo_entrada.ev")
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
        if arquivo_entrada.endswith('.ev'):
            arquivo_saida = arquivo_entrada.replace('.ev', '.s')
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