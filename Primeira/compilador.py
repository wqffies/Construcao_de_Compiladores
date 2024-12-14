#Equipe:
# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127

import sys

def read_program(file_path):
    #Lê o conteúdo do arquivo
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Erro: O arquivo {file_path} não foi encontrado")
        sys.exit(1)

def validate_program(content):
    #Valida que o conteúdo do programa é uma constante inteira
    if not content.isdigit():
        sys.exit(1)
    return int(content)

def generate_assembly(value):
    #Gera o código assembly para o modelo
    return f"""  mov ${value}, %rax"""

def wrap_with_modelo(assembly_code):
    #Envolve o código assembly com o modelo
    modelo = """\
  .section .text
  .globl _start

_start:
{code}
  call imprime_num
  call sair

  .include "runtime.s"
"""
    return modelo.format(code=assembly_code)

def write_assembly(output_path, assembly_code):
    #Escreve o código assembly em um arquivo
    with open(output_path, 'w') as file:
        file.write(assembly_code)

def main(input_file, output_file):
    #Ler o arquivo de entrada
    content = read_program(input_file)
    
    #Validar o programa
    value = validate_program(content)
    
    #Gerar o código assembly
    assembly_code = generate_assembly(value)
    
    #Envolver o código no modelo
    final_code = wrap_with_modelo(assembly_code)
    
    #Escrever o código assembly no arquivo de saída
    write_assembly(output_file, final_code)
    print(f"Código assembly gerado em {output_file}.")

if __name__ == "__main__":
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)