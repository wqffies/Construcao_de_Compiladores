import unittest
from atividade8 import tokenizar, analisar, gerarCodigo, interpretar

class TestCompiladorEV(unittest.TestCase):
    # Testes para declarações de variáveis
    def test_declaracao_variavel_simples(self):
        entrada = "x = 10; = x"
        programa = analisar(entrada)
        self.assertEqual(repr(programa), "x = 10\n= x")
        resultado = interpretar(programa)
        self.assertEqual(resultado, 10)

    def test_multiplas_declaracoes(self):
        entrada = """
        x = 5;
        y = x + 3;
        = y * 2
        """
        programa = analisar(entrada)
        self.assertEqual(repr(programa), "x = 5\ny = (x + 3)\n= (y * 2)")
        resultado = interpretar(programa)
        self.assertEqual(resultado, 16)

    # Testes para expressões com variáveis
    def test_expressao_com_variaveis(self):
        entrada = """
        a = 10;
        b = 20;
        = a + b
        """
        programa = analisar(entrada)
        resultado = interpretar(programa)
        self.assertEqual(resultado, 30)

    def test_expressao_complexa_com_variaveis(self):
        entrada = """
        x = 5;
        y = 3;
        z = x * y + 2;
        = z - (x + y)
        """
        programa = analisar(entrada)
        resultado = interpretar(programa)
        self.assertEqual(resultado, 9)

    # Testes para verificação semântica
    def test_variavel_nao_declarada(self):
        entrada = "= x + 5"  # x não foi declarado
        with self.assertRaises(NameError) as cm:
            analisar(entrada)
        self.assertIn("Variável não declarada", str(cm.exception))

    def test_variavel_usada_antes_declaracao(self):
        entrada = """
        y = x + 5;
        x = 10;
        = y
        """
        with self.assertRaises(NameError) as cm:
            analisar(entrada)
        self.assertIn("Variável não declarada", str(cm.exception))

    # Testes para geração de código
    def test_geracao_codigo_declaracao(self):
        entrada = "x = 10 + 5; = x"
        programa = analisar(entrada)
        codigo = gerarCodigo(programa)
        
        expected_code = """
        .section .bss
        .lcomm x, 8

        .section .text
        .globl _start
        _start:
        mov $10, %rax
        push %rax
        mov $5, %rax
        pop %rbx
        add %rbx, %rax
        mov %rax, x
        mov x, %rax
        call imprime_num
        call sair
        .include "runtime.s\""""
        
        self.assertIn("mov $10, %rax", codigo)
        self.assertIn("mov %rax, x", codigo)
        self.assertIn(".lcomm x, 8", codigo)

    def test_geracao_codigo_expressao_complexa(self):
        entrada = """
        x = 7 + 4 * 12;
        y = x / 3;
        = y + 5
        """
        programa = analisar(entrada)
        codigo = gerarCodigo(programa)
        
        self.assertIn(".lcomm x, 8", codigo)
        self.assertIn(".lcomm y, 8", codigo)
        self.assertIn("mov $12, %rax", codigo)
        self.assertIn("pop %rbx", codigo)
        self.assertIn("imul %rbx, %rax", codigo)
        self.assertIn("idiv %rbx", codigo)

    # Testes para interpretação
    def test_interpretacao_expressao_aninhada_com_variaveis(self):
        entrada = """
        a = 10;
        b = 5;
        c = (a + b) * 2;
        = c - a
        """
        programa = analisar(entrada)
        resultado = interpretar(programa)
        self.assertEqual(resultado, 20)

    def test_interpretacao_multiplas_operacoes(self):
        entrada = """
        x = 100;
        y = x / 10;
        z = y * (x + 5);
        = z - 50
        """
        programa = analisar(entrada)
        resultado = interpretar(programa)
        self.assertEqual(resultado, 1000)

    # Testes para sintaxe inválida
    def test_falta_ponto_virgula(self):
        entrada = "x = 10 = x"  # Falta ;
        with self.assertRaises(SyntaxError):
            analisar(entrada)

    def test_falta_igual_final(self):
        entrada = "x = 10; x + 5"  # Falta = no final
        with self.assertRaises(SyntaxError):
            analisar(entrada)

    # Testes para tokenização
    def test_tokenizacao_declaracao(self):
        entrada = "x = 42; = x"
        tokens = tokenizar(entrada)
        self.assertEqual(tokens, ['x', '=', '42', ';', '=', 'x'])

    def test_tokenizacao_expressao_complexa(self):
        entrada = "x = (a + b) * c; = x"
        tokens = tokenizar(entrada)
        self.assertEqual(tokens, ['x', '=', '(', 'a', '+', 'b', ')', '*', 'c', ';', '=', 'x'])

    # Teste para verificar precedência com variáveis
    def test_precedencia_com_variaveis(self):
        entrada = """
        a = 10;
        b = 2;
        c = 3;
        = a + b * c
        """
        programa = analisar(entrada)
        self.assertEqual(repr(programa.resultado), "(a + (b * c))")
        resultado = interpretar(programa)
        self.assertEqual(resultado, 16)

    # Teste para verificar associatividade
    def test_associatividade_com_variaveis(self):
        entrada = """
        x = 10;
        y = 5;
        z = 2;
        = x - y - z
        """
        programa = analisar(entrada)
        self.assertEqual(repr(programa.resultado), "((x - y) - z)")
        resultado = interpretar(programa)
        self.assertEqual(resultado, 3)
    
    #Teste para verificação de declarações vazias
    def test_declaracao_vazia(self):
        entrada = "x = ; = 10"  # Declaração sem expressão
        with self.assertRaises(SyntaxError):
            analisar(entrada)
    #Testes para múltiplos usos da mesma variável
    def test_multiplos_usos_mesma_variavel(self):
        entrada = """
        x = 5;
        y = x + x * x;
        = y - x
        """
        programa = analisar(entrada)
        resultado = interpretar(programa)
        self.assertEqual(resultado, 25)
    #Teste para verificar ordem das declarações na seção BSS
    def test_ordem_declaracoes_bss(self):
        entrada = """
        b = 2;
        a = 1;
        = a + b
        """
        codigo = gerarCodigo(analisar(entrada))
        self.assertLess(codigo.find(".lcomm b, 8"), codigo.find(".lcomm a, 8"))
    #Teste para programas sem declarações
    def test_programa_sem_declaracoes(self):
        entrada = "= 10 + 20"
        programa = analisar(entrada)
        self.assertEqual(len(programa.declaracoes), 0)
        self.assertEqual(interpretar(programa), 30)
if __name__ == '__main__':
    unittest.main()