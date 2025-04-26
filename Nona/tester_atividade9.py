# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824

import unittest
from arvore_sintatica_atividade9 import tokenizar, analisar, interpretar  

class TestCompiladorCmd(unittest.TestCase):
    def test_atribuicao_simples(self):
        src = """
        x = 5;
        {
            return x;
        }
        """
        prog = analisar(src)
        resultado = interpretar(prog)
        self.assertEqual(resultado, 5)

    def test_if_else_true(self):
        src = """
        x = 10;
        resultado = 0;
        {
            if x > 5 {
                resultado = 1;
            } else {
                resultado = 0;
            }
            return resultado;
        }
        """
        prog = analisar(src)
        self.assertEqual(interpretar(prog), 1)

    def test_if_else_false(self):
        src = """
        x = 3;
        resultado = 0;
        {
            if x > 5 {
                resultado = 1;
            } else {
                resultado = 0;
            }
            return resultado;
        }
        """
        prog = analisar(src)
        self.assertEqual(interpretar(prog), 0)

    def test_while_loop(self):
        src = """
        n = 4;
        sum = 0;
        {
            while n > 0 {
                sum = sum + n;
                n = n - 1;
            }
            return sum;
        }
        """
        prog = analisar(src)
        self.assertEqual(interpretar(prog), 10)  # 4 + 3 + 2 + 1 = 10

    def test_combinado(self):
        src = """
        a = 5;
        b = 2;
        result = 0;
        {
            while a > 0 {
                if a == b {
                    result = result + 100;
                } else {
                    result = result + 1;
                }
                a = a - 1;
            }
            return result;
        }
        """
        prog = analisar(src)
        self.assertEqual(interpretar(prog), 104)

    def test_comparacao_retorna_inteiro(self):
        src = """
        {
            return 2 < 3;
        }
        """
        prog = analisar(src)
        self.assertEqual(interpretar(prog), 1)
        src2 = """
        {
            return 5 == 6;
        }
        """
        prog2 = analisar(src2)
        self.assertEqual(interpretar(prog2), 0)

    def test_precedencia_comparacao(self):
        src = """
        {
            return 1 + 2 < 3 + 4;
        }
        """
        prog = analisar(src)
        self.assertEqual(interpretar(prog), 1)

    def test_comparacao_encadeada(self):
        src = """
        {
            return 1 < 2 < 3;
        }
        """
        prog = analisar(src)
        self.assertEqual(interpretar(prog), 1)

    def test_tokenizacao_cmd(self):
        src = "if x == 1 { return x + 1; } else { return x - 1; }"
        tokens = tokenizar(src)
        expected = [
            'if', 'x', '==', '1', '{',
            'return', 'x', '+', '1', ';', '}',
            'else', '{',
            'return', 'x', '-', '1', ';', '}'
        ]
        self.assertEqual(tokens, expected)

    def test_syntax_error_semicolon(self):
        src = """
        x = 10
        {
            return x;
        }
        """
        with self.assertRaises(SyntaxError):
            analisar(src)

    def test_syntax_error_missing_brace(self):
        src = """
        {
            return 5;
        """
        with self.assertRaises(SyntaxError):
            analisar(src)

    def test_name_error_undeclared(self):
        src = """
        {
            x = 1;  # x não foi declarado antes
            return x;
        }
        """
        with self.assertRaises(NameError):
            analisar(src)

    def test_name_error_use_before_decl(self):
        src = """
        y = x + 1;
        x = 2;
        {
            return y;
        }
        """
        with self.assertRaises(NameError):
            analisar(src)

if __name__ == '__main__':
    unittest.main()