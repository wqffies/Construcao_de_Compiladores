import unittest
from atividade6 import tokenizar, analisar, interpretar, gerarCodigo
from io import StringIO
import sys

class TestCompilador(unittest.TestCase):
    def test_codigo_constante(self):
        entrada = "8"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertEqual(codigo, f"mov $8, %rax")
    
    def test_codigo_soma(self):
        entrada = "(8 + 12)"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertEqual(codigo, f"mov $8, %rax\npush %rax\nmov $12, %rax\npop %rbx\nadd %rbx, %rax\n")

    def test_codigo_subtracao(self):
        entrada = "(8 - 12)"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertEqual(codigo, f"mov $8, %rax\npush %rax\nmov $12, %rax\npop %rbx\nsub %rbx, %rax\n")
    def test_codigo_divisao(self):
        entrada = "(8 / 12)"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertEqual(codigo, f"mov $8, %rax\npush %rax\nmov $12, %rax\npop %rbx\nxchg %rax, %rbx\ncqo\nidiv %rbx\n")
    def test_codigo_multiplicacao(self):
        entrada = "(8 * 12)"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertEqual(codigo, f"mov $8, %rax\npush %rax\nmov $12, %rax\npop %rbx\nimul %rbx, %rax\n")
    def test_respeita_precedencia(self):
        entrada = "(3/(6+(40*5)))"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertEqual(codigo, f"mov $3, %rax\npush %rax\nmov $6, %rax\npush %rax\nmov $40, %rax\npush %rax\nmov $5, %rax\npop %rbx\nimul %rbx, %rax\n\npop %rbx\nadd %rbx, %rax\n\npop %rbx\nxchg %rax, %rbx\ncqo\nidiv %rbx\n")
if __name__ == '__main__':
    unittest.main()