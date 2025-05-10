# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824

import sys
from arvore_sintatica_atividade10 import *
from gerador_assembly import GeradorCodigoFun

# arquivo para passar uma entrada .fun e ter um assembly gerado na saída
def main():
    if len(sys.argv) < 2:
        print("Uso: python arquivo_principal.py <arquivo_fonte.fun>")
        print("    Irá gerar <arquivo_fonte.s>")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    if not arquivo_entrada.endswith('.fun'):
        print("Arquivo deve ter extensão .fun")
        sys.exit(1)
    
    # define nomes dos arquivos de saída
    base_nome = arquivo_entrada[:-4]
    arquivo_assembly = base_nome + '.s'
    
    try:
        # lê o arquivo de entrada
        with open(arquivo_entrada, 'r') as f:
            codigo_fonte = f.read()
        
        # cria o lexer
        lexer = Lexer(codigo_fonte)
        
        # cria o parser
        parser = ParserFun(lexer)
        
        # analisa o programa e constrói a AST
        programa = parser.analisar_programa()

        # vê o resultado a partir da arvore:
        arvore = analisar(codigo_fonte)
        resultado = interpretar(arvore)
        print("Resultado:", resultado)
        
        # cria o gerador de código
        gerador = GeradorCodigoFun(parser.tabela_simbolos)
        
        # gera o código assembly
        gerador.gerar_programa(programa)
        
        # escreve o arquivo assembly
        with open(arquivo_assembly, 'w') as f:
            for instrucao in gerador.codigo:
                f.write(instrucao + '\n')
        
        print(f"✓ Arquivo assembly gerado: {arquivo_assembly}")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado")
        sys.exit(1)
    except Exception as e:
        print(f"Erro durante a compilação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()