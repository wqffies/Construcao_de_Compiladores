class Token:
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    def __eq__(self, outro):
        if isinstance(outro, Token):
            return (self.tipo == outro.tipo and 
                    self.lexema == outro.lexema and 
                    self.linha == outro.linha and 
                    self.coluna == outro.coluna)
        return False

    def __repr__(self):
        return f'Token({self.tipo}, "{self.lexema}", Linha: {self.linha}, Coluna: {self.coluna})'

class Exp:
    pass

class Var(Exp):
    def __init__(self, nome: str):
        self.nome = nome
    
    def __repr__(self):
        return self.nome

class Const(Exp):
    def __init__(self, valor: int):
        self.valor = valor
    
    def __repr__(self):
        return str(self.valor)

class OpBin(Exp):
    def __init__(self, operador: str, op_esq: Exp, op_dir: Exp):
        self.operador = operador
        self.op_esq = op_esq
        self.op_dir = op_dir
    
    def __repr__(self):
        return f'({self.op_esq} {self.operador} {self.op_dir})'

class Declaracao:
    def __init__(self, var: str, exp: Exp):
        self.var = var
        self.exp = exp
    
    def __repr__(self):
        return f"{self.var} = {self.exp}"

class Programa:
    def __init__(self, declaracoes: list[Declaracao], resultado: Exp):
        self.declaracoes = declaracoes
        self.resultado = resultado
    
    def __repr__(self):
        decls = "\n".join(str(d) for d in self.declaracoes)
        return f"{decls}\n= {self.resultado}"

class Lexer:
    def __init__(self, entrada):
        self.entrada = entrada
        self.tamanho = len(entrada)
        self.posicao = 0
        self.linha = 1
        self.coluna = 1

    def olhar_proximo_token(self):
        """Observa o próximo token sem consumir"""
        posicao_atual = self.posicao
        linha_atual = self.linha
        coluna_atual = self.coluna
        
        try:
            proximo = self.proximo_token()
            self.posicao = posicao_atual
            self.linha = linha_atual
            self.coluna = coluna_atual
            return proximo
        except Exception:
            return None

    def proximo_token(self):
        """Retorna o próximo token da entrada ou um token EOF se a entrada terminar."""
        while self.posicao < self.tamanho:
            char = self.entrada[self.posicao]

            if char.isspace():
                if char == '\n':  
                    self.linha += 1
                    self.coluna = 1
                else:
                    self.coluna += 1
                self.posicao += 1
                continue

            inicio_linha = self.linha
            inicio_coluna = self.coluna

            if char.isdigit():
                num_str = char
                self.posicao += 1
                self.coluna += 1
                while self.posicao < self.tamanho and self.entrada[self.posicao].isdigit():
                    num_str += self.entrada[self.posicao]
                    self.posicao += 1
                    self.coluna += 1
                return Token("Numero", num_str, inicio_linha, inicio_coluna)

            if char.isalpha():
                ident = char
                self.posicao += 1
                self.coluna += 1
                while (self.posicao < self.tamanho and 
                      (self.entrada[self.posicao].isalnum() or 
                       self.entrada[self.posicao] == '_')):
                    ident += self.entrada[self.posicao]
                    self.posicao += 1
                    self.coluna += 1
                return Token("Identificador", ident, inicio_linha, inicio_coluna)

            tipo_token = {
                '(': "ParenEsq",
                ')': "ParenDir",
                '+': "Soma",
                '-': "Sub",
                '*': "Mult",
                '/': "Div",
                '=': "Atribuicao",
                ';': "PontoVirgula"
            }.get(char)

            if tipo_token:
                token = Token(tipo_token, char, inicio_linha, inicio_coluna)
                self.posicao += 1
                self.coluna += 1
                return token

            raise ValueError(f"Caractere inválido '{char}' na linha {self.linha}, coluna {self.coluna}")

        return Token("EOF", "", self.linha, self.coluna)

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def analisar_prim(self):
        tok = self.lexer.proximo_token()
        
        if tok.tipo == "Numero":
            return Const(int(tok.lexema))
        elif tok.tipo == "Identificador":
            return Var(tok.lexema)
        elif tok.tipo == "ParenEsq":
            exp = self.analisar_exp_a()
            if self.lexer.proximo_token().tipo != "ParenDir":
                raise SyntaxError("Parêntese não fechado corretamente")
            return exp
        raise SyntaxError(f"Token inesperado: {tok}")

    def analisar_exp_m(self):
        esq = self.analisar_prim()
        tok = self.lexer.olhar_proximo_token()
        
        while tok and tok.tipo in ["Mult", "Div"]:
            op_token = self.lexer.proximo_token()
            dir = self.analisar_prim()
            esq = OpBin(op_token.lexema, esq, dir)
            tok = self.lexer.olhar_proximo_token()
        
        return esq

    def analisar_exp_a(self):
        esq = self.analisar_exp_m()
        tok = self.lexer.olhar_proximo_token()
        
        while tok and tok.tipo in ["Soma", "Sub"]:
            op_token = self.lexer.proximo_token()
            dir = self.analisar_exp_m()
            esq = OpBin(op_token.lexema, esq, dir)
            tok = self.lexer.olhar_proximo_token()
        
        return esq

class ParserEV(Parser):
    def __init__(self, lexer: Lexer):
        super().__init__(lexer)
        self.tabela_simbolos = set()

    def analisar_declaracao(self):
        var_tok = self.lexer.proximo_token()
        if var_tok.tipo != "Identificador":
            raise SyntaxError("Esperado nome de variável antes do '='")
        
        if self.lexer.proximo_token().tipo != "Atribuicao":
            raise SyntaxError("Esperado '=' após nome da variável")
        
        exp = self.analisar_exp_a()
        
        if self.lexer.proximo_token().tipo != "PontoVirgula":
            raise SyntaxError("Esperado ';' após expressão")
        
        # Verifica variáveis na expressão antes de adicionar
        self.verificar_variaveis(exp)
        self.tabela_simbolos.add(var_tok.lexema)
        return Declaracao(var_tok.lexema, exp)

    def analisar_programa(self):
        declaracoes = []
        while True:
            tok = self.lexer.olhar_proximo_token()
            if tok is None or tok.tipo == "EOF":
                break
                
            if tok.tipo == "Identificador":
                declaracoes.append(self.analisar_declaracao())
            elif tok.lexema == "=":
                self.lexer.proximo_token()
                resultado = self.analisar_exp_a()
                # Verifica variáveis no resultado final
                self.verificar_variaveis(resultado)
                return Programa(declaracoes, resultado)
            else:
                raise SyntaxError(f"Esperado declaração ou '=', encontrado {tok}")
        
        raise SyntaxError("Expressão final não encontrada")

    def verificar_variaveis(self, exp):
        if isinstance(exp, Var):
            if exp.nome not in self.tabela_simbolos:
                raise NameError(f"Variável não declarada: {exp.nome}")
        elif isinstance(exp, OpBin):
            self.verificar_variaveis(exp.op_esq)
            self.verificar_variaveis(exp.op_dir)

def interpretar(arvore: Exp, contexto: dict = None):
    if contexto is None:
        contexto = {}
    
    if isinstance(arvore, Const):
        return arvore.valor
    elif isinstance(arvore, Var):
        if arvore.nome not in contexto:
            raise NameError(f"Variável não definida: {arvore.nome}")
        return contexto[arvore.nome]
    elif isinstance(arvore, OpBin):
        esq = interpretar(arvore.op_esq, contexto)
        dir = interpretar(arvore.op_dir, contexto)
        
        if arvore.operador == '+':
            return esq + dir
        elif arvore.operador == '-':
            return esq - dir
        elif arvore.operador == '*':
            return esq * dir
        elif arvore.operador == '/':
            return esq // dir
        else:
            raise ValueError(f"Operador desconhecido: {arvore.operador}")
    elif isinstance(arvore, Declaracao):
        valor = interpretar(arvore.exp, contexto)
        contexto[arvore.var] = valor
        return valor
    elif isinstance(arvore, Programa):
        for decl in arvore.declaracoes:
            interpretar(decl, contexto)
        return interpretar(arvore.resultado, contexto)
    else:
        raise TypeError(f"Tipo de nó desconhecido: {type(arvore)}")

def analisar(entrada: str):
    lexer = Lexer(entrada)
    parser = ParserEV(lexer)
    
    try:
        programa = parser.analisar_programa()
        tok_final = lexer.proximo_token()
        if tok_final.tipo != "EOF":
            raise SyntaxError(f"Tokens não esperados no final: {tok_final}")
        return programa
    except SyntaxError as e:
        raise SyntaxError(f"Erro de sintaxe na linha {parser.lexer.linha}: {e}")
    except NameError as e:
        raise NameError(f"Erro semântico: {e}")

def tokenizar(entrada: str, incluir_metadados: bool = False):
    lexer = Lexer(entrada)
    tokens = []
    
    try:
        while True:
            token = lexer.proximo_token()
            if token.tipo == "EOF":
                break
            tokens.append(token)
    except ValueError as e:
        if incluir_metadados:
            print(f"Erro léxico: {e}")
            return None
        raise
    
    return tokens if incluir_metadados else [token.lexema for token in tokens]

def imprimir_arvore_centralizada(arvore):
    tipos_validos = (OpBin, Const, Var, Declaracao, Programa)
    if not isinstance(arvore, tipos_validos):
        return
    
    def altura(arvore):
        if isinstance(arvore, (Const, Var)):
            return 1
        elif isinstance(arvore, (Declaracao, Programa)):
            return 1 + altura(arvore.exp) if isinstance(arvore, Declaracao) else 1 + altura(arvore.resultado)
        elif isinstance(arvore, OpBin):
            return 1 + max(altura(arvore.op_esq), altura(arvore.op_dir))
        return 0
    
    def valor_no(no):
        if isinstance(no, Const):
            return str(no.valor)
        elif isinstance(no, Var):
            return no.nome
        elif isinstance(no, OpBin):
            return no.operador
        elif isinstance(no, Declaracao):
            return f"{no.var}="
        elif isinstance(no, Programa):
            return "PROG"
        return "?"
    
    def preencher_niveis(arvore, nivel, posicao, largura, matriz, conexoes):
        if arvore is None:
            return
        
        meio = (posicao[0] + posicao[1]) // 2
        matriz[nivel][meio] = valor_no(arvore)
        
        if isinstance(arvore, OpBin):
            esq_meio = (posicao[0] + meio - 1) // 2
            dir_meio = (meio + 1 + posicao[1]) // 2
            conexoes[nivel + 1][esq_meio] = '/'
            conexoes[nivel + 1][dir_meio] = '\\'
            preencher_niveis(arvore.op_esq, nivel + 2, (posicao[0], meio - 1), largura, matriz, conexoes)
            preencher_niveis(arvore.op_dir, nivel + 2, (meio + 1, posicao[1]), largura, matriz, conexoes)
        elif isinstance(arvore, Declaracao):
            dir_meio = (meio + 1 + posicao[1]) // 2
            conexoes[nivel + 1][dir_meio] = '|'
            preencher_niveis(arvore.exp, nivel + 2, (meio, posicao[1]), largura, matriz, conexoes)
        elif isinstance(arvore, Programa):
            preencher_niveis(arvore.resultado, nivel, posicao, largura, matriz, conexoes)
    
    h = altura(arvore)
    largura = 2 ** h
    matriz = [[' ' for _ in range(largura)] for _ in range(h * 2)]
    conexoes = [[' ' for _ in range(largura)] for _ in range(h * 2)]
    
    preencher_niveis(arvore, 0, (0, largura - 1), largura, matriz, conexoes)
    
    for i in range(h * 2):
        linha = ''.join(conexoes[i]) if i % 2 else ''.join(matriz[i])
        print(linha.rstrip())