# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824

class Token:
    """Representa um token encontrado no código fonte"""
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo    # Tipo do token (ex: Numero, Identificador)
        self.lexema = lexema  # Valor literal do token
        self.linha = linha    # Número da linha no código
        self.coluna = coluna  # Coluna inicial do token

    def __repr__(self):
        return f'Token({self.tipo}, "{self.lexema}", Linha: {self.linha}, Coluna: {self.coluna})'

class Exp:
    """Classe base para expressões"""
    pass

class Var(Exp):
    """Representa uma variável na AST"""
    def __init__(self, nome: str):
        self.nome = nome
    
    def __repr__(self):
        return self.nome

class Const(Exp):
    """Representa um valor constante na AST"""
    def __init__(self, valor: int):
        self.valor = valor
    
    def __repr__(self):
        return str(self.valor)

class OpBin(Exp):
    """Representa uma operação binária na AST"""
    def __init__(self, operador: str, op_esq: Exp, op_dir: Exp):
        self.operador = operador  # Operador (+, -, *, etc)
        self.op_esq = op_esq      # Operando esquerdo
        self.op_dir = op_dir      # Operando direito
    
    def __repr__(self):
        return f'({self.op_esq} {self.operador} {self.op_dir})'

class Declaracao:
    """Representa uma declaração de variável"""
    def __init__(self, var: str, exp: Exp):
        self.var = var  # Nome da variável
        self.exp = exp  # Expressão de inicialização
    
    def __repr__(self):
        return f"{self.var} = {self.exp};"

class Cmd:
    """Classe base para comandos"""
    pass

class If(Cmd):
    """Representa um comando condicional"""
    def __init__(self, condicao: Exp, entao: list[Cmd], senao: list[Cmd]):
        self.condicao = condicao  # Expressão condicional
        self.entao = entao        # Lista de comandos 'then'
        self.senao = senao        # Lista de comandos 'else'
    
    def __repr__(self):
        return f"If({self.condicao} then={self.entao} else={self.senao})"

class While(Cmd):
    """Representa um loop while"""
    def __init__(self, condicao: Exp, corpo: list[Cmd]):
        self.condicao = condicao  # Expressão de condição
        self.corpo = corpo        # Lista de comandos do loop
    
    def __repr__(self):
        return f"While({self.condicao}, {self.corpo})"

class Atrib(Cmd):
    """Representa uma atribuição de variável"""
    def __init__(self, var: str, exp: Exp):
        self.var = var  # Nome da variável
        self.exp = exp  # Expressão de atribuição
    
    def __repr__(self):
        return f"{self.var} = {self.exp};"

class Return(Cmd):
    """Representa um comando de retorno"""
    def __init__(self, exp: Exp):
        self.exp = exp  # Expressão de retorno
    
    def __repr__(self):
        return f"Return {self.exp};"

class ProgramaCmd:
    """Representa o programa completo"""
    def __init__(self, declaracoes: list[Declaracao], comandos: list[Cmd], resultado: Exp):
        self.declaracoes = declaracoes  # Declarações globais
        self.comandos = comandos        # Lista de comandos
        self.resultado = resultado      # Expressão de retorno final
    
    def __repr__(self):
        decls = "\n".join(str(d) for d in self.declaracoes)
        cmds = "\n".join(f"  {c}" for c in self.comandos)
        return f"{decls}\n{{\n{cmds}\n  return {self.resultado};\n}}"

class Lexer:
    """Responsável por tokenizar o código fonte"""
    def __init__(self, entrada):
        self.entrada = entrada      # String de entrada
        self.tamanho = len(entrada) # Tamanho da entrada
        self.posicao = 0            # Posição atual
        self.linha = 1              # Contador de linhas
        self.coluna = 1             # Contador de colunas

    def olhar_proximo_token(self):
        """Retorna o próximo token sem consumí-lo"""
        # Salva estado atual
        pos = self.posicao
        linha = self.linha
        col = self.coluna
        
        token = self.proximo_token()
        
        # Restaura estado
        self.posicao = pos
        self.linha = linha
        self.coluna = col
        return token

    def proximo_token(self):
        """Retorna o próximo token consumindo a entrada"""
        while self.posicao < self.tamanho:
            char = self.entrada[self.posicao]

            # Ignora espaços e atualiza contadores de posição
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

            # Números
            if char.isdigit():
                num_str = char
                self.posicao += 1
                self.coluna += 1
                while self.posicao < self.tamanho and self.entrada[self.posicao].isdigit():
                    num_str += self.entrada[self.posicao]
                    self.posicao += 1
                    self.coluna += 1
                return Token("Numero", num_str, inicio_linha, inicio_coluna)

            # Identificadores e palavras-chave
            if char.isalpha():
                ident = char
                self.posicao += 1
                self.coluna += 1
                while self.posicao < self.tamanho and self.entrada[self.posicao].isalnum():
                    ident += self.entrada[self.posicao]
                    self.posicao += 1
                    self.coluna += 1
                
                # Verifica se é palavra-chave
                tipo = {
                    "if": "If",
                    "else": "Else",
                    "while": "While",
                    "return": "Return"
                }.get(ident, "Identificador")
                return Token(tipo, ident, inicio_linha, inicio_coluna)

            # Operadores e símbolos
            if char == '=':
                self.posicao += 1
                self.coluna += 1
                # Verifica se é '=='
                if self.posicao < self.tamanho and self.entrada[self.posicao] == '=':
                    self.posicao += 1
                    self.coluna += 1
                    return Token("Igual", "==", inicio_linha, inicio_coluna)
                return Token("Atribuicao", "=", inicio_linha, inicio_coluna)

            # Mapeia caracteres para tokens
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
    """Parser base com métodos para análise de expressões"""
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def analisar_prim(self):
        """Analisa expressões primárias (números, variáveis, parênteses)"""
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
        """Analisa multiplicações e divisões (maior precedência)"""
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
        """Analisa adições e subtrações"""
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
        """Analisa comparações (menor precedência)"""
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
    """Parser estendido com verificação semântica e análise de comandos"""
    def __init__(self, lexer: Lexer):
        super().__init__(lexer)
        self.tabela_simbolos = set()  # Tabela de símbolos para variáveis declaradas

    def verificar_variaveis(self, exp: Exp):
        """Verifica se todas as variáveis usadas estão declaradas"""
        if isinstance(exp, Var):
            if exp.nome not in self.tabela_simbolos:
                raise NameError(f"Variável não declarada: {exp.nome}")
        elif isinstance(exp, OpBin):
            self.verificar_variaveis(exp.op_esq)
            self.verificar_variaveis(exp.op_dir)

    def analisar_declaracao(self):
        """Analisa uma declaração de variável (ex: x = 5;)"""
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
        """Analisa um comando (if, while, atribuição)"""
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
        """Analisa estrutura condicional if-else"""
        self.lexer.proximo_token()  # Consome 'if'
        cond = self.analisar_exp_comp()
        
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' após condição do if")
        
        entao = []
        while self.lexer.olhar_proximo_token().tipo != "ChaveDir":
            entao.append(self.analisar_comando())
        self.lexer.proximo_token()  # Consome '}'
        
        if self.lexer.proximo_token().tipo != "Else":
            raise SyntaxError("Esperado 'else' após bloco 'then'")
        
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' após 'else'")
        
        senao = []
        while self.lexer.olhar_proximo_token().tipo != "ChaveDir":
            senao.append(self.analisar_comando())
        self.lexer.proximo_token()  # Consome '}'
        
        return If(cond, entao, senao)

    def analisar_while(self):
        """Analisa loop while"""
        self.lexer.proximo_token()  # Consome 'while'
        cond = self.analisar_exp_comp()
        
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' após condição do while")
        
        corpo = []
        while self.lexer.olhar_proximo_token().tipo != "ChaveDir":
            corpo.append(self.analisar_comando())
        self.lexer.proximo_token()  # Consome '}'
        
        return While(cond, corpo)

    def analisar_atrib(self):
        """Analisa atribuição de variável (ex: x = 10;)"""
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
        """Analisa o programa completo"""
        declaracoes = []
        while self.lexer.olhar_proximo_token().tipo == "Identificador":
            declaracoes.append(self.analisar_declaracao())

        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{'")

        comandos = []
        while self.lexer.olhar_proximo_token().tipo != "Return":
            comandos.append(self.analisar_comando())

        self.lexer.proximo_token()  # Consome 'return'
        resultado = self.analisar_exp_comp()
        if self.lexer.proximo_token().tipo != "PontoVirgula":
            raise SyntaxError("Esperado ';' após return")
        
        if self.lexer.proximo_token().tipo != "ChaveDir":
            raise SyntaxError("Esperado '}'")
        
        return ProgramaCmd(declaracoes, comandos, resultado)


# Função principal de interpretação de nós da árvore sintática
def interpretar(no, contexto=None):
    if contexto is None:
        contexto = {}

    # Caso o nó seja uma constante, retorna seu valor diretamente
    if isinstance(no, Const):
        return no.valor

    # Caso o nó seja uma variável, busca seu valor no contexto
    if isinstance(no, Var):
        if no.nome not in contexto:
            raise NameError(f"Variável não definida: {no.nome}")
        return contexto[no.nome]

    # Caso o nó seja uma operação binária (ex: +, -, *, /, <, >, ==)
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
            return esq // dir  # divisão inteira
        if no.operador == '<':
            return 1 if esq < dir else 0
        if no.operador == '>':
            return 1 if esq > dir else 0
        if no.operador == '==':
            return 1 if esq == dir else 0
        raise ValueError(f"Operador desconhecido: {no.operador}")

    # Declaração de variável (ex: int x = 5)
    if isinstance(no, Declaracao):
        valor = interpretar(no.exp, contexto)
        contexto[no.var] = valor
        return None

    # Atribuição de valor a uma variável já existente
    if isinstance(no, Atrib):
        if no.var not in contexto:
            raise NameError(f"Variável não declarada: {no.var}")
        contexto[no.var] = interpretar(no.exp, contexto)
        return None

    # Estrutura condicional (if/else)
    if isinstance(no, If):
        cond = interpretar(no.condicao, contexto)
        bloco = no.entao if cond != 0 else no.senao
        for cmd in bloco:
            res = interpretar(cmd, contexto)
            if res is not None:
                return res
        return None

    # Estrutura de repetição (while)
    if isinstance(no, While):
        while interpretar(no.condicao, contexto) != 0:
            for cmd in no.corpo:
                res = interpretar(cmd, contexto)
                if res is not None:
                    return res
        return None

    # Retorno de função
    if isinstance(no, Return):
        return interpretar(no.exp, contexto)

    # Execução do programa principal
    if isinstance(no, ProgramaCmd):
        for decl in no.declaracoes:
            interpretar(decl, contexto)

        for cmd in no.comandos:
            res = interpretar(cmd, contexto)
            if res is not None:
                return res

        return interpretar(no.resultado, contexto)

    raise TypeError(f"Tipo de nó não suportado na interpretação: {type(no)}")

# Analisa o código de entrada, retornando a árvore sintática
def analisar(entrada: str):
    lexer = Lexer(entrada)
    parser = ParserEV(lexer)
    programa = parser.analisar_programa()
    if lexer.proximo_token().tipo != "EOF":
        raise SyntaxError("Tokens não esperados no final")
    return programa

# Converte a entrada em uma lista de tokens (opcionalmente com metadados)
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

# Impressão de árvore sintática centralizada (modo visual em ASCII)
def imprimir_arvore_centralizada(arvore):
    tipos_validos = (OpBin, Const, Var, Declaracao, ProgramaCmd)
    if not isinstance(arvore, tipos_validos):
        return

    # Função para calcular altura da árvore
    def altura(arvore):
        if isinstance(arvore, (Const, Var)):
            return 1
        elif isinstance(arvore, (Declaracao, ProgramaCmd)):
            return 1 + altura(arvore.exp) if isinstance(arvore, Declaracao) else 1 + altura(arvore.resultado)
        elif isinstance(arvore, OpBin):
            return 1 + max(altura(arvore.op_esq), altura(arvore.op_dir))
        return 0

    # Retorna representação textual de um nó
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

    # Preenche os níveis da árvore para exibição
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

    # Imprime a árvore linha por linha
    for i in range(h * 2):
        linha = ''.join(conexoes[i]) if i % 2 else ''.join(matriz[i])
        print(linha.rstrip())