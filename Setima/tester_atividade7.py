import unittest
from atividade7 import tokenizar, analisar, gerarCodigo, interpretar

class TestCompiladorSemParenteses(unittest.TestCase):
    def test_expressao_soma_sem_parenteses(self):
        entrada = "8 + 12"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertEqual(codigo, f"mov $8, %rax\npush %rax\nmov $12, %rax\npop %rbx\nadd %rbx, %rax\n")

    def test_expressao_multipla_soma(self):
        entrada = "10 + 5 + 3"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertEqual(codigo, f"mov $10, %rax\npush %rax\nmov $5, %rax\npop %rbx\nadd %rbx, %rax\n\npush %rax\nmov $3, %rax\npop %rbx\nadd %rbx, %rax\n")

    def test_expressao_associatividade_esquerda_soma(self):
        entrada = "10 - 5 - 3"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        expected = """mov $10, %rax
push %rax
mov $5, %rax
pop %rbx
sub %rax, %rbx
mov %rbx, %rax

push %rax
mov $3, %rax
pop %rbx
sub %rax, %rbx
mov %rbx, %rax\n"""
        self.assertEqual(codigo, expected)

    def test_expressao_associatividade_esquerda_multiplicacao(self):
        entrada = "2 * 3 * 4"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        codigo = gerarCodigo(arvore)
        self.assertEqual(codigo, f"mov $2, %rax\npush %rax\nmov $3, %rax\npop %rbx\nimul %rbx, %rax\n\npush %rax\nmov $4, %rax\npop %rbx\nimul %rbx, %rax\n")

    def test_interpretacao_simples_soma(self):
        entrada = "5 + 3"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(5 + 3)")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 8)

    def test_interpretacao_simples_subtracao(self):
        entrada = "10 - 7"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(10 - 7)")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 3)

    def test_interpretacao_simples_multiplicacao(self):
        entrada = "6 * 4"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(6 * 4)")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 24)

    def test_interpretacao_simples_divisao(self):
        entrada = "20 / 5"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(20 / 5)")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 4)

    def test_interpretacao_precedencia_soma_multiplicacao(self):
        entrada = "3 + 4 * 2"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(3 + (4 * 2))")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 11)

    def test_interpretacao_precedencia_subtracao_divisao(self):
        entrada = "10 - 6 / 2"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(10 - (6 / 2))")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 7)

    def test_interpretacao_expressao_complexa_1(self):
        entrada = "2 * 3 + 4 * 5"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "((2 * 3) + (4 * 5))")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 26)

    def test_interpretacao_expressao_complexa_2(self):
        entrada = "10 + 5 * 2 - 3 / 1"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "((10 + (5 * 2)) - (3 / 1))")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 17)

    def test_interpretacao_associatividade_soma(self):
        entrada = "5 + 3 + 2"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "((5 + 3) + 2)")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 10)

    def test_interpretacao_associatividade_subtracao(self):
        entrada = "20 - 5 - 3"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "((20 - 5) - 3)")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 12)

    def test_interpretacao_expressao_aninhada_1(self):
        entrada = "8 - (3 + (4 * 5))"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(8 - (3 + (4 * 5)))")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, -15)

    def test_interpretacao_expressao_aninhada_2(self):
        entrada = "(10 + (5 * 2)) / (3 - 1)"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "((10 + (5 * 2)) / (3 - 1))")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 10)

    def test_interpretacao_expressao_aninhada_3(self):
        entrada = "((2 + 3) * (4 - 1)) / 3"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(((2 + 3) * (4 - 1)) / 3)")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 5)

    def test_interpretacao_expressao_negativa(self):
        entrada = "5 * (3 - 8)"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(5 * (3 - 8))")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, -25)

    def test_interpretacao_expressao_zero(self):
        entrada = "10 - (5 + 5)"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(10 - (5 + 5))")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 0)

    def test_interpretacao_numeros_grandes(self):
        entrada = "100 * 200 + 50"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "((100 * 200) + 50)")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 20050)

    def test_interpretacao_divisao_fracionaria(self):
        entrada = "7 / 2"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(7 / 2)")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 3)

    def test_interpretacao_expressao_multipla_1(self):
        entrada = "2 * 3 + 4 * 5 - 6 / 2"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "(((2 * 3) + (4 * 5)) - (6 / 2))")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 23)

    def test_interpretacao_expressao_multipla_2(self):
        entrada = "10 / 2 * 3 + 4 - 1"
        arvore = analisar(entrada)
        self.assertEqual(repr(arvore), "((((10 / 2) * 3) + 4) - 1)")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 18)

    def test_interpretacao_precedencia_divisao(self):
        entrada = "20 - 10 / 2"
        arvore = analisar(entrada)
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 15)

    def test_interpretacao_expressao_precedencia_multiplicacao_divisao(self):
        entrada = "24 / 4 * 3 + 2"
        arvore = analisar(entrada)
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 20)

if __name__ == '__main__':
    unittest.main()