import unittest
from atividade6 import tokenizar, analisar, gerarCodigo, gerarProgramaCompleto

class TestCompilador(unittest.TestCase):
    def test_codigo_constante(self):
        entrada = "8"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertEqual(codigo, "  mov $8, %rax")
    
    def test_codigo_soma(self):
        entrada = "(8 + 12)"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        # operando esquerdo primeiro, com indentação
        expected = """  mov $8, %rax
  push %rax
  mov $12, %rax
  pop %rbx
  add %rbx, %rax"""
        self.assertEqual(codigo, expected)

    def test_codigo_subtracao(self):
        entrada = "(8 - 12)"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        # operando esquerdo primeiro, sub %rax,%rbx (rbx = rbx - rax)
        expected = """  mov $8, %rax
  push %rax
  mov $12, %rax
  pop %rbx
  sub %rax, %rbx
  mov %rbx, %rax"""
        self.assertEqual(codigo, expected)

    def test_codigo_divisao(self):
        entrada = "(8 / 12)"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        # operando esquerdo primeiro
        expected = """  mov $8, %rax
  push %rax
  mov $12, %rax
  pop %rbx
  xchg %rax, %rbx
  cqo
  idiv %rbx"""
        self.assertEqual(codigo, expected)

    def test_codigo_multiplicacao(self):
        entrada = "(8 * 12)"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        # operando esquerdo primeiro
        expected = """  mov $8, %rax
  push %rax
  mov $12, %rax
  pop %rbx
  imul %rbx, %rax"""
        self.assertEqual(codigo, expected)

    def test_respeita_precedencia(self):
        entrada = "(3/(6+(40*5)))"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        # ordem correta dos operandos e indentação
        expected = """  mov $3, %rax
  push %rax
  mov $6, %rax
  push %rax
  mov $40, %rax
  push %rax
  mov $5, %rax
  pop %rbx
  imul %rbx, %rax
  pop %rbx
  add %rbx, %rax
  pop %rbx
  xchg %rax, %rbx
  cqo
  idiv %rbx"""
        self.assertEqual(codigo, expected)

    def test_expressao_complexa(self):
        entrada = "((3 + 5) * (10 - 2))"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        # ordem correta e operação de subtração correta
        expected = """  mov $3, %rax
  push %rax
  mov $5, %rax
  pop %rbx
  add %rbx, %rax
  push %rax
  mov $10, %rax
  push %rax
  mov $2, %rax
  pop %rbx
  sub %rax, %rbx
  mov %rbx, %rax
  pop %rbx
  imul %rbx, %rax"""
        self.assertEqual(codigo, expected)

    def test_programa_completo(self):
        """Testa a geração do programa assembly completo"""
        entrada = "(7 + 3)"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo_completo = gerarProgramaCompleto(arvore)
        
        # Verifica se contém os elementos principais
        self.assertIn(".section .text", codigo_completo)
        self.assertIn(".globl _start", codigo_completo)
        self.assertIn("_start:", codigo_completo)
        self.assertIn("call imprime_num", codigo_completo)
        self.assertIn("call sair", codigo_completo)
        self.assertIn(".include \"runtime.s\"", codigo_completo)
        
        # Verifica se contém o código da expressão
        self.assertIn("mov $7, %rax", codigo_completo)
        self.assertIn("mov $3, %rax", codigo_completo)
        self.assertIn("add %rbx, %rax", codigo_completo)

    def test_operacoes_ordem_correta(self):
        """Testa se a ordem dos operandos está correta para subtração e divisão"""
        # 10 - 3 = 7
        tokens = tokenizar("(10 - 3)")
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertIn("mov $10, %rax", codigo)  # Primeiro operando (esquerdo)
        self.assertIn("mov $3, %rax", codigo)   # Segundo operando (direito)
        self.assertIn("sub %rax, %rbx", codigo) # rbx = rbx - rax (10 - 3)
        
        # 20 / 4 = 5
        tokens = tokenizar("(20 / 4)")
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertIn("mov $20, %rax", codigo)  # Primeiro operando (esquerdo)
        self.assertIn("mov $4, %rax", codigo)   # Segundo operando (direito)
        self.assertIn("xchg %rax, %rbx", codigo) # Troca para colocar 20 em RAX

if __name__ == '__main__':
    unittest.main()