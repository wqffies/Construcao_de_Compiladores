import unittest
from atividade5 import tokenizar, analisar, interpretar, imprimir_arvore_centralizada
from io import StringIO
import sys

class TestCompilador(unittest.TestCase):
    def test_tokenizacao(self):
        entrada = "(8 - (3 + (4 * 5)))"
        tokens_esperados = ['(', '8', '-', '(', '3', '+', '(', '4', '*', '5', ')', ')', ')']
        self.assertEqual(tokenizar(entrada), tokens_esperados)

    def test_analise_sintatica_valida(self):
        entrada = "(8 - (3 + (4 * 5)))"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        self.assertEqual(repr(arvore), "(8 - (3 + (4 * 5)))")

    def test_interpretacao_valida(self):
        entrada = "(8 - (3 + (4 * 5)))"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        self.assertEqual(repr(arvore), "(8 - (3 + (4 * 5)))")
        resultado = interpretar(arvore)
        self.assertEqual(resultado, -15)  # 8 - (3 + 20) = 8 - 23 = -15

    def test_erro_sintaxe_falta_parentese(self):
        entrada = "(8 - 2"
        tokens = tokenizar(entrada)
        with self.assertRaises(SyntaxError):
            arvore = analisar(tokens)

    def test_erro_sintaxe_operador_invalido(self):
        entrada = "(8 % 2)"
        with self.assertRaises(ValueError):
            tokens = tokenizar(entrada)

    def test_erro_sintaxe_tokens_sobrando(self):
        entrada = "(8 - 2) 3"
        tokens = tokenizar(entrada)
        with self.assertRaises(SyntaxError):
            arvore = analisar(tokens)
        
    def test_expressao_invalida(self):
        entrada = "(8 2)"
        tokens = tokenizar(entrada)
        with self.assertRaises(SyntaxError):
            arvore = analisar(tokens)
       
    
    def test_expressao_com_x(self):
        entrada = "(x + 2)"
        with self.assertRaises(ValueError):
            tokens = tokenizar(entrada)

    def test_constante(self):
        entrada = "42"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        self.assertEqual(repr(arvore), "42") # teste da arvore
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 42)

    def test_operacao_complexa(self):
        entrada = "((2 + 3) * (4 - 1))"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        self.assertEqual(repr(arvore), "((2 + 3) * (4 - 1))") # teste da arvore
        resultado = interpretar(arvore)
        self.assertEqual(resultado, 15)  # (5) * (3) = 15

    def test_printar_arvore(self): # teste de print da arvore
        captured_output = StringIO()
        sys.stdout = captured_output 
        entrada = "((2 + 3) * (4 - 1))"
        tokens = tokenizar(entrada)
        arvore = analisar(tokens)
        imprimir_arvore_centralizada(arvore)
        sys.stdout = sys.stdout 
        self.assertEqual(captured_output.getvalue(), "   *\n /   \\\n +   -\n/ \\ / \\\n2 3 4 1\n\n")
    
if __name__ == '__main__':
    unittest.main()