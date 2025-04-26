# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824

class Token:
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

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
        return f"{self.var} = {self.exp};"

class Cmd:
    pass

class If(Cmd):
    def __init__(self, condicao: Exp, entao: list[Cmd], senao: list[Cmd]):
        self.condicao = condicao
        self.entao = entao      
        self.senao = senao      

    def __repr__(self):
        return f"If({self.condicao} then={self.entao} else={self.senao})"

class While(Cmd):
    def __init__(self, condicao: Exp, corpo: list[Cmd]):
        self.condicao = condicao
        self.corpo = corpo      

    def __repr__(self):
        return f"While({self.condicao}, {self.corpo})"

class Atrib(Cmd):
    def __init__(self, var: str, exp: Exp):
        self.var = var
        self.exp = exp

    def __repr__(self):
        return f"{self.var} = {self.exp};"

class Return(Cmd):
    def __init__(self, exp: Exp):
        self.exp = exp

    def __repr__(self):
        return f"Return {self.exp};"

class ProgramaCmd:
    def __init__(self, declaracoes: list[Declaracao], comandos: list[Cmd], resultado: Exp):
        self.declaracoes = declaracoes  
        self.comandos = comandos        
        self.resultado = resultado

    def __repr__(self):
        decls = "\n".join(str(d) for d in self.declaracoes)
        cmds  = "\n".join(f"  {c}" for c in self.comandos)
        return f"{decls}\n{{\n{cmds}\n  return {self.resultado};\n}}"

class Lexer:
    def __init__(self, entrada):
        self.entrada = entrada
        self.tamanho = len(entrada)
        self.posicao = 0
        self.linha = 1
        self.coluna = 1

    def olhar_proximo_token(self):
        pos = self.posicao
        linha = self.linha
        col = self.coluna
        token = self.proximo_token()
        self.posicao = pos
        self.linha = linha
        self.coluna = col
        return token

    def proximo_token(self):
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
                while self.posicao < self.tamanho and self.entrada[self.posicao].isalnum():
                    ident += self.entrada[self.posicao]
                    self.posicao += 1
                    self.coluna += 1
                tipo = {
                    "if": "If",
                    "else": "Else",
                    "while": "While",
                    "return": "Return"
                }.get(ident, "Identificador")
                return Token(tipo, ident, inicio_linha, inicio_coluna)

            if char == '=':
                self.posicao += 1
                self.coluna += 1
                if self.posicao < self.tamanho and self.entrada[self.posicao] == '=':
                    self.posicao += 1
                    self.coluna += 1
                    return Token("Igual", "==", inicio_linha, inicio_coluna)
                return Token("Atribuicao", "=", inicio_linha, inicio_coluna)

            tipo_token = {
                '<': "Menor",
                '>': "Maior",
                '{': "ChaveEsq",
                '}': "ChaveDir",
                '(': "ParenEsq",
                ')': "ParenDir",
                '+': "Soma",
                '-': "Sub",
                '*': "Mult",
                '/': "Div",
                ';': "PontoVirgula"
            }.get(char)

            if tipo_token:
                self.posicao += 1
                self.coluna += 1
                return Token(tipo_token, char, inicio_linha, inicio_coluna)

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
            exp = self.analisar_exp_comp()
            if self.lexer.proximo_token().tipo != "ParenDir":
                raise SyntaxError("Parêntese direito esperado")
            return exp
        raise SyntaxError(f"Token inesperado: {tok}")

    def analisar_exp_m(self):
        esq = self.analisar_prim()
        while True:
            tok = self.lexer.olhar_proximo_token()
            if tok and tok.tipo in ["Mult", "Div"]:
                op = self.lexer.proximo_token()
                dir = self.analisar_prim()
                esq = OpBin(op.lexema, esq, dir)
            else:
                break
        return esq

    def analisar_exp_a(self):
        esq = self.analisar_exp_m()
        while True:
            tok = self.lexer.olhar_proximo_token()
            if tok and tok.tipo in ["Soma", "Sub"]:
                op = self.lexer.proximo_token()
                dir = self.analisar_exp_m()
                esq = OpBin(op.lexema, esq, dir)
            else:
                break
        return esq

    def analisar_exp_comp(self):
        esq = self.analisar_exp_a()
        while True:
            tok = self.lexer.olhar_proximo_token()
            if tok and tok.tipo in ["Menor", "Maior", "Igual"]:
                op = self.lexer.proximo_token()
                dir = self.analisar_exp_a()
                esq = OpBin(op.lexema, esq, dir)
            else:
                break
        return esq

class ParserEV(Parser):
    def __init__(self, lexer: Lexer):
        super().__init__(lexer)
        self.tabela_simbolos = set()

    def verificar_variaveis(self, exp: Exp):
        if isinstance(exp, Var):
            if exp.nome not in self.tabela_simbolos:
                raise NameError(f"Variável não declarada: {exp.nome}")
        elif isinstance(exp, OpBin):
            self.verificar_variaveis(exp.op_esq)
            self.verificar_variaveis(exp.op_dir)

    def analisar_declaracao(self):
        var_tok = self.lexer.proximo_token()
        if var_tok.tipo != "Identificador":
            raise SyntaxError("Esperado identificador")
        
        if self.lexer.proximo_token().tipo != "Atribuicao":
            raise SyntaxError("Esperado '='")
        
        exp = self.analisar_exp_comp()
        if self.lexer.proximo_token().tipo != "PontoVirgula":
            raise SyntaxError("Esperado ';'")
        
        self.verificar_variaveis(exp)
        self.tabela_simbolos.add(var_tok.lexema)
        return Declaracao(var_tok.lexema, exp)

    def analisar_comando(self):
        tok = self.lexer.olhar_proximo_token()
        if tok.tipo == "If":
            return self.analisar_if()
        elif tok.tipo == "While":
            return self.analisar_while()
        elif tok.tipo == "Identificador":
            return self.analisar_atrib()
        else:
            raise SyntaxError(f"Comando inválido: {tok}")

    def analisar_if(self):
        self.lexer.proximo_token()  
        cond = self.analisar_exp_comp()
        
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' após condição do if")
        
        entao = []
        while self.lexer.olhar_proximo_token().tipo != "ChaveDir":
            entao.append(self.analisar_comando())
        self.lexer.proximo_token()  
        
        if self.lexer.proximo_token().tipo != "Else":
            raise SyntaxError("Esperado 'else' após bloco 'then'")
        
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' após 'else'")
        
        senao = []
        while self.lexer.olhar_proximo_token().tipo != "ChaveDir":
            senao.append(self.analisar_comando())
        self.lexer.proximo_token()  
        
        return If(cond, entao, senao)

    def analisar_while(self):
        self.lexer.proximo_token()  
        cond = self.analisar_exp_comp()
        
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' após condição do while")
        
        corpo = []
        while self.lexer.olhar_proximo_token().tipo != "ChaveDir":
            corpo.append(self.analisar_comando())
        self.lexer.proximo_token()  
        
        return While(cond, corpo)

    def analisar_atrib(self):
        var_tok = self.lexer.proximo_token()
        if var_tok.tipo != "Identificador":
            raise SyntaxError("Esperado identificador")
        
        if self.lexer.proximo_token().tipo != "Atribuicao":
            raise SyntaxError("Esperado '='")
        
        exp = self.analisar_exp_comp()
        if self.lexer.proximo_token().tipo != "PontoVirgula":
            raise SyntaxError("Esperado ';'")
        
        if var_tok.lexema not in self.tabela_simbolos:
            raise NameError(f"Variável não declarada: {var_tok.lexema}")
        
        return Atrib(var_tok.lexema, exp)

    def analisar_programa(self):
        declaracoes = []
        while self.lexer.olhar_proximo_token().tipo == "Identificador":
            declaracoes.append(self.analisar_declaracao())

        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{'")

        comandos = []
        while self.lexer.olhar_proximo_token().tipo != "Return":
            comandos.append(self.analisar_comando())

        self.lexer.proximo_token()  
        resultado = self.analisar_exp_comp()
        if self.lexer.proximo_token().tipo != "PontoVirgula":
            raise SyntaxError("Esperado ';' após return")
        
        if self.lexer.proximo_token().tipo != "ChaveDir":
            raise SyntaxError("Esperado '}'")
        
        return ProgramaCmd(declaracoes, comandos, resultado)

def interpretar(no, contexto=None):
    if contexto is None:
        contexto = {}

    if isinstance(no, Const):
        return no.valor

    if isinstance(no, Var):
        if no.nome not in contexto:
            raise NameError(f"Variável não definida: {no.nome}")
        return contexto[no.nome]

    if isinstance(no, OpBin):
        esq = interpretar(no.op_esq, contexto)
        dir = interpretar(no.op_dir, contexto)
        if no.operador == '+':
            return esq + dir
        if no.operador == '-':
            return esq - dir
        if no.operador == '*':
            return esq * dir
        if no.operador == '/':
            return esq // dir
        if no.operador == '<':
            return 1 if esq < dir else 0
        if no.operador == '>':
            return 1 if esq > dir else 0
        if no.operador == '==':
            return 1 if esq == dir else 0
        raise ValueError(f"Operador desconhecido: {no.operador}")

    if isinstance(no, Declaracao):
        valor = interpretar(no.exp, contexto)
        contexto[no.var] = valor
        return None

    if isinstance(no, Atrib):
        if no.var not in contexto:
            raise NameError(f"Variável não declarada: {no.var}")
        contexto[no.var] = interpretar(no.exp, contexto)
        return None

    if isinstance(no, If):
        cond = interpretar(no.condicao, contexto)
        bloco = no.entao if cond != 0 else no.senao
        for cmd in bloco:
            res = interpretar(cmd, contexto)
            if res is not None:
                return res
        return None

    if isinstance(no, While):
        while interpretar(no.condicao, contexto) != 0:
            for cmd in no.corpo:
                res = interpretar(cmd, contexto)
                if res is not None:
                    return res
        return None

    if isinstance(no, Return):
        return interpretar(no.exp, contexto)

    if isinstance(no, ProgramaCmd):
        for decl in no.declaracoes:
            interpretar(decl, contexto)

        for cmd in no.comandos:
            res = interpretar(cmd, contexto)
            if res is not None:
                return res

        return interpretar(no.resultado, contexto)

    raise TypeError(f"Tipo de nó não suportado na interpretação: {type(no)}")

def analisar(entrada: str):
    lexer = Lexer(entrada)
    parser = ParserEV(lexer)
    programa = parser.analisar_programa()      
    if lexer.proximo_token().tipo != "EOF":
        raise SyntaxError("Tokens não esperados no final")
    return programa

def tokenizar(entrada: str, incluir_metadados: bool = False):
    """Converte a entrada em uma lista de tokens."""
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
    tipos_validos = (OpBin, Const, Var, Declaracao, ProgramaCmd)
    if not isinstance(arvore, tipos_validos):
        return
    
    def altura(arvore):
        if isinstance(arvore, (Const, Var)):
            return 1
        elif isinstance(arvore, (Declaracao, ProgramaCmd)):
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
        elif isinstance(no, ProgramaCmd):
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
        elif isinstance(arvore, ProgramaCmd):
            preencher_niveis(arvore.resultado, nivel, posicao, largura, matriz, conexoes)
    
    h = altura(arvore)
    largura = 2 ** h
    matriz = [[' ' for _ in range(largura)] for _ in range(h * 2)]
    conexoes = [[' ' for _ in range(largura)] for _ in range(h * 2)]
    
    preencher_niveis(arvore, 0, (0, largura - 1), largura, matriz, conexoes)
    
    for i in range(h * 2):
        linha = ''.join(conexoes[i]) if i % 2 else ''.join(matriz[i])
        print(linha.rstrip())