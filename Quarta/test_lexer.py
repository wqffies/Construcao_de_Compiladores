import unittest
from lexer import Lexer, Token

class TestLexer(unittest.TestCase):

    def test_simples(self):
        """Testa uma expressão simples."""
        lexer = Lexer("(3 + 5)")
        esperado = [
            Token("ParenEsq", "(", 1, 1),
            Token("Numero", "3", 1, 2),
            Token("Soma", "+", 1, 4),
            Token("Numero", "5", 1, 6),
            Token("ParenDir", ")", 1, 7),
            Token("EOF", "", 1, 8)
        ]
        self._comparar_tokens(lexer, esperado)

    def test_expressao_aninhada(self):
        """Testa expressões aninhadas."""
        lexer = Lexer("(3 + (4 * (11 - 7)))")
        esperado = [
            Token("ParenEsq", "(", 1, 1),
            Token("Numero", "3", 1, 2),
            Token("Soma", "+", 1, 4),
            Token("ParenEsq", "(", 1, 6),
            Token("Numero", "4", 1, 7),
            Token("Mult", "*", 1, 9),
            Token("ParenEsq", "(", 1, 11),
            Token("Numero", "11", 1, 12),
            Token("Sub", "-", 1, 15),
            Token("Numero", "7", 1, 17),
            Token("ParenDir", ")", 1, 18),
            Token("ParenDir", ")", 1, 19),
            Token("ParenDir", ")", 1, 20),
            Token("EOF", "", 1, 21)
        ]
        self._comparar_tokens(lexer, esperado)

    def test_multiplas_linhas(self):
        """Testa expressões quebradas em múltiplas linhas."""
        lexer = Lexer("(3 + 2)\n(5 * 7)")
        esperado = [
            Token("ParenEsq", "(", 1, 1),
            Token("Numero", "3", 1, 2),
            Token("Soma", "+", 1, 4),
            Token("Numero", "2", 1, 6),
            Token("ParenDir", ")", 1, 7),
            Token("ParenEsq", "(", 2, 1),
            Token("Numero", "5", 2, 2),
            Token("Mult", "*", 2, 4),
            Token("Numero", "7", 2, 6),
            Token("ParenDir", ")", 2, 7),
            Token("EOF", "", 2, 8)
        ]
        self._comparar_tokens(lexer, esperado)

    def test_espacos_em_branco(self):
        """Testa se espaços extras são ignorados."""
        lexer = Lexer("   (  5   *    8 ) ")
        esperado = [
            Token("ParenEsq", "(", 1, 4),
            Token("Numero", "5", 1, 7),
            Token("Mult", "*", 1, 11),
            Token("Numero", "8", 1, 16),
            Token("ParenDir", ")", 1, 18),
            Token("EOF", "", 1, 20)
        ]
        self._comparar_tokens(lexer, esperado)

    def test_somente_numeros(self):
        """Testa um número isolado."""
        lexer = Lexer("42")
        esperado = [
            Token("Numero", "42", 1, 1),
            Token("EOF", "", 1, 3)
        ]
        self._comparar_tokens(lexer, esperado)

    def test_entrada_vazia(self):
        """Testa entrada vazia, esperando apenas o token EOF."""
        lexer = Lexer("")
        esperado = [Token("EOF", "", 1, 1)]
        self._comparar_tokens(lexer, esperado)
    def operadores_sem_espacos(self):
        """Testa reconhecimento de operadores sem espaços entre números e operadores."""
        lexer = Lexer("3+4*2-6/3")
        esperado = [
            Token("Numero", "3", 1, 1),
            Token("Soma", "+", 1, 2),
            Token("Numero", "4", 1, 3),
            Token("Mult", "*", 1, 4),
            Token("Numero", "2", 1, 5),
            Token("Sub", "-", 1, 6),
            Token("Numero", "6", 1, 7),
            Token("Div", "/", 1, 8),
            Token("Numero", "3", 1, 9),
            Token("EOF", "", 1, 10)
        ]
        self._comparar_tokens(lexer, esperado)
    def multilinha_com_espacos_e_tabs(self):
        """Testa expressões em múltiplas linhas com espaços e tabs."""
        lexer = Lexer("  (\n\t42 + 1\n)")
        esperado = [
            Token("ParenEsq", "(", 1, 3),
            Token("Numero", "42", 2, 2),
            Token("Soma", "+", 2, 5),
            Token("Numero", "1", 2, 7),
            Token("ParenDir", ")", 3, 1),
            Token("EOF", "", 3, 2)
        ]
        self._comparar_tokens(lexer, esperado)

    def test_caractere_invalido(self):
        """Testa erro ao encontrar um caractere inválido."""
        lexer = Lexer("(4 & 5)")
        with self.assertRaises(ValueError) as contexto:
            self._comparar_tokens(lexer, [])
        self.assertIn("Símbolo inválido '&'", str(contexto.exception))

    def _comparar_tokens(self, lexer, esperado):
        """Verifica se os tokens retornados correspondem ao esperado."""
        tokens = []
        while True:
            token = lexer.proximo_token()
            tokens.append(token)
            if token.tipo == "EOF":
                break
        self.assertEqual(tokens, esperado)
    

if __name__ == "__main__":
    unittest.main()