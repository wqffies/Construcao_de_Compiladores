# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824

import unittest
from arvore_sintatica_atividade10 import tokenizar, analisar, interpretar  

class TestesCompiladorFun(unittest.TestCase):
    # Teste básico: retorno de constante
    def test_retorno_constante(self):
        codigo = """
        main {
            return 42;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 42)

    # Teste de variável global
    def test_variavel_global_simples(self):
        codigo = """
        var x = 10;
        main {
            return x;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 10)

    # Teste de função simples
    def test_funcao_simples(self):
        codigo = """
        fun constante() {
            return 7;
        }
        
        main {
            return constante();
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 7)

    # Teste de função com parâmetro
    def test_funcao_com_parametro(self):
        codigo = """
        fun dobro(x) {
            return x * 2;
        }
        
        main {
            return dobro(5);
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 10)

    # Teste de expressão aritmética
    def test_expressao_aritmetica(self):
        codigo = """
        main {
            return 2 + 3 * 4;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 14)

    # Teste de if-else básico
    def test_if_else_basico(self):
        codigo = """
        var x = 5;
        var result = 0;
        main {
            if x > 3 {
                result = 1;
            } else {
                result = 0;
            }
            return result;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 1)

    # Teste de while simples
    def test_while_simples(self):
        codigo = """
        var i = 0;
        var soma = 0;
        main {
            while i < 5 {
                soma = soma + 1;
                i = i + 1;
            }
            return soma;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 5)

    # Teste de função recursiva - fatorial
    def test_fatorial_recursivo(self):
        codigo = """
        fun fatorial(n) {
            var result = 1;
            if n == 0 {
                result = 1;
            } else {
                result = n * fatorial(n - 1);
            }
            return result;
        }
        
        main {
            return fatorial(4);
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 24)

    # Teste de variável local em função
    def test_variavel_local(self):
        codigo = """
        fun teste() {
            var local = 8;
            return local;
        }
        
        main {
            return teste();
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 8)

    # Teste de comparação retornando booleano
    def test_comparacao_booleana(self):
        codigo = """
        main {
            return 5 < 10;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 1)  # True = 1

    # Teste de múltiplos parâmetros
    def test_multiplos_parametros(self):
        codigo = """
        fun soma(a, b, c) {
            return a + b + c;
        }
        
        main {
            return soma(1, 2, 3);
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 6)

    # Teste de atribuição em main
    def test_atribuicao_main(self):
        codigo = """
        var x = 5;
        main {
            x = x + 3;
            return x;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 8)

    # Teste de expressão com parênteses
    def test_expressao_parenteses(self):
        codigo = """
        main {
            return (2 + 3) * (4 - 1);
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 15)

    # Teste de divisão
    def test_divisao(self):
        codigo = """
        main {
            return 10 / 2;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 5)

    # Teste de comparação de igualdade
    def test_comparacao_igualdade(self):
        codigo = """
        main {
            return 5 == 5;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 1)

    # Teste de função chamando função
    def test_funcao_chama_funcao(self):
        codigo = """
        fun adicionaUm(x) {
            return x + 1;
        }
        
        fun adicionaDois(x) {
            return adicionaUm(adicionaUm(x));
        }
        
        main {
            return adicionaDois(3);
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 5)

    # Teste de soma acumulativa
    def test_soma_acumulativa(self):
        codigo = """
        var total = 0;
        var i = 1;
        main {
            while i <= 10 {
                total = total + i;
                i = i + 1;
            }
            return total;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 55)  # Soma de 1 a 10

    # Teste de operadores relacionais
    def test_operadores_relacionais(self):
        codigo = """
        var result = 0;
        main {
            if 3 < 5 {
                if 7 > 2 {
                    result = 1;
                } else {
                    result = 2;
                }
            } else {
                result = 0;
            }
            return result;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 1)

    # Teste de subtração
    def test_subtracao(self):
        codigo = """
        main {
            return 10 - 7;
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 3)

    # Teste de função com while
    def test_funcao_com_while(self):
        codigo = """
        fun contaAte(n) {
            var i = 0;
            while i < n {
                i = i + 1;
            }
            return i;
        }
        
        main {
            return contaAte(7);
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 7)

    # Teste de Fibonacci iterativo
    def test_fibonacci_iterativo(self):
        codigo = """
        fun fibonacci(n) {
            var a = 0;
            var b = 1;
            var temp = 0;
            var i = 0;
            var result = 0;
            
            if n == 0 {
                result = 0;
            } else {
                while i < n - 1 {
                    temp = a + b;
                    a = b;
                    b = temp;
                    i = i + 1;
                }
                result = b;
            }
            return result;
        }
        main {
            return fibonacci(6);
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 8)  # F(6) = 8

    # Teste de máximo entre dois números
    def test_maximo_dois_numeros(self):
        codigo = """
        fun max(a, b) {
            var result = 0;
            if a > b {
                result = a;
            } else {
                result = b;
            }
            return result;
        }

        main {
            return max(15, 23);
        }
        """
        prog = analisar(codigo)
        self.assertEqual(interpretar(prog), 23)


    # ========= TESTES DE ERRO ADICIONADOS:===========
    
    # Teste de erro: Falta de main
    def test_erro_falta_main(self):
        codigo = """
        var x = 10;
        """
        with self.assertRaises(Exception):
            prog = analisar(codigo)
            interpretar(prog)
    
    # Teste de erro: Múltiplos main
    def test_erro_multiplos_main(self):
        codigo = """
        main {
            return 1;
        }
        main {
            return 2;
        }
        """
        with self.assertRaises(Exception):
            prog = analisar(codigo)
            interpretar(prog)
    
    # Teste de erro: Variável não declarada
    def test_erro_variavel_nao_declarada(self):
        codigo = """
        main {
            return variavel_nao_declarada;
        }
        """
        with self.assertRaises(Exception):
            prog = analisar(codigo)
            interpretar(prog)
    
    # Teste de erro: Função não declarada
    def test_erro_funcao_nao_declarada(self):
        codigo = """
        main {
            return funcao_nao_existente(5);
        }
        """
        with self.assertRaises(Exception):
            prog = analisar(codigo)
            interpretar(prog)
    
    # Teste de erro: Número errado de argumentos
    def test_erro_numero_argumentos(self):
        codigo = """
        fun soma(a, b) {
            return a + b;
        }
        main {
            return soma(1);
        }
        """
        with self.assertRaises(Exception):
            prog = analisar(codigo)
            interpretar(prog)
    
    # Teste de erro: Declaração de variável duplicada
    def test_erro_variavel_duplicada(self):
        codigo = """
        var x = 10;
        var x = 20;
        main {
            return x;
        }
        """
        with self.assertRaises(Exception):
            prog = analisar(codigo)
            interpretar(prog)
    
    # Teste de erro: Função duplicada
    def test_erro_funcao_duplicada(self):
        codigo = """
        fun duplicada(x) {
            return x;
        }
        fun duplicada(y) {
            return y;
        }
        main {
            return duplicada(1);
        }
        """
        with self.assertRaises(Exception):
            prog = analisar(codigo)
            interpretar(prog)
    
    # Teste de erro: Return fora de função
    def test_erro_return_fora_funcao(self):
        codigo = """
        var x = 10;
        return x;
        main {
            return 1;
        }
        """
        with self.assertRaises(Exception):
            analisar(codigo)
    
    # Teste de erro: Expressão vazia em return
    def test_erro_return_vazio(self):
        codigo = """
        main {
            return;
        }
        """
        with self.assertRaises(Exception):
            analisar(codigo)
    
    # Teste de erro: Sintaxe inválida em while
    def test_erro_while_sem_corpo(self):
        codigo = """
        main {
            while 1 == 1
            return 0;
        }
        """
        with self.assertRaises(Exception):
            analisar(codigo)
    
    # Teste de erro: Parênteses desbalanceados
    def test_erro_parenteses_desbalanceados(self):
        codigo = """
        main {
            return ((5 + 3);
        }
        """
        with self.assertRaises(Exception):
            analisar(codigo)
    
    # Teste de erro: Operador inválido
    def test_erro_operador_invalido(self):
        codigo = """
        main {
            return 5 +++ 3;
        }
        """
        with self.assertRaises(Exception):
            analisar(codigo)
    
    # Teste de erro: If sem else (estrutura incompleta)
    def test_erro_if_sem_else(self):
        codigo = """
        main {
            if (1 == 1) { return 1; }
            return 0;
        }
        """
        with self.assertRaises(Exception):
            analisar(codigo)
    
    # Teste de erro: Caractere inválido
    def test_erro_caractere_invalido(self):
        codigo = """
        main {
            return 5 # 3;
        }
        """
        with self.assertRaises(Exception):
            analisar(codigo)

    # Teste de erro: Declaração de variável na main
    def test_erro_declaracao_variavel_main(self):
        codigo = """
        main {
            var x = 6;
            return x;
        }
        """
        with self.assertRaises(Exception):
            analisar(codigo)

if __name__ == '__main__':
    unittest.main()