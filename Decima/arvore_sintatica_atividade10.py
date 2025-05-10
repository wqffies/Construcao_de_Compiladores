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

class FunCall(Exp):
    """Representa uma chamada de função na AST"""
    def __init__(self, nome: str, params: list[Exp]):
        self.nome = nome
        self.params = params
    
    def __repr__(self):
        return f"{self.nome}({', '.join(map(str, self.params))})"

class Declaracao:
    """Classe base para declarações"""
    pass

class VarDecl(Declaracao):
    """Representa uma declaração de variável"""
    def __init__(self, var: str, exp: Exp):
        self.var = var  # Nome da variável
        self.exp = exp  # Expressão de inicialização
    
    def __repr__(self):
        return f"var {self.var} = {self.exp};"

class FunDecl(Declaracao):
    """Representa uma declaração de função"""
    def __init__(self, nome: str, params: list[str], corpo: list, resultado: Exp):
        self.nome = nome
        self.params = params
        self.corpo = corpo
        self.resultado = resultado
    
    def __repr__(self):
        params_str = ", ".join(self.params)
        corpo_str = "\n    ".join(map(str, self.corpo))
        return f"fun {self.nome}({params_str}) {{\n    {corpo_str}\n    return {self.resultado};\n}}"

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
        entao_str = "\n        ".join(map(str, self.entao))
        senao_str = "\n        ".join(map(str, self.senao))
        return f"if ({self.condicao}) {{\n        {entao_str}\n    }} else {{\n        {senao_str}\n    }}"

class While(Cmd):
    """Representa um loop while"""
    def __init__(self, condicao: Exp, corpo: list[Cmd]):
        self.condicao = condicao  # Expressão de condição
        self.corpo = corpo        # Lista de comandos do loop
    
    def __repr__(self):
        corpo_str = "\n        ".join(map(str, self.corpo))
        return f"while ({self.condicao}) {{\n        {corpo_str}\n    }}"

class Atrib(Cmd):
    """Representa uma atribuição de variável"""
    def __init__(self, var: str, exp: Exp):
        self.var = var  # Nome da variável
        self.exp = exp  # Expressão de atribuição
    
    def __repr__(self):
        return f"{self.var} = {self.exp};"

class ProgramaFun:
    """Representa o programa completo na linguagem Fun"""
    def __init__(self, declaracoes: list[Declaracao], main_comandos: list[Cmd], main_resultado: Exp):
        self.declaracoes = declaracoes    # Declarações globais (vars e funcs)
        self.main_comandos = main_comandos  # Comandos dentro do bloco main
        self.main_resultado = main_resultado  # Expressão de retorno do main
    
    def __repr__(self):
        decls_str = "\n".join(map(str, self.declaracoes))
        cmds_str = "\n    ".join(map(str, self.main_comandos))
        return f"{decls_str}\nmain {{\n    {cmds_str}\n    return {self.main_resultado};\n}}"

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
                    "return": "Return",
                    "fun": "Fun",
                    "var": "Var",
                    "main": "Main"
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
            
            if char == ',':
                self.posicao += 1
                self.coluna += 1
                return Token("Virgula", ",", inicio_linha, inicio_coluna)
            
            # Tratamento de <= e >=
            if char == '<':
                self.posicao += 1
                self.coluna += 1
                if self.posicao < self.tamanho and self.entrada[self.posicao] == '=':
                    self.posicao += 1
                    self.coluna += 1
                    return Token("MenorIgual", "<=", inicio_linha, inicio_coluna)
                return Token("Menor", "<", inicio_linha, inicio_coluna)

            if char == '>':
                self.posicao += 1
                self.coluna += 1
                if self.posicao < self.tamanho and self.entrada[self.posicao] == '=':
                    self.posicao += 1
                    self.coluna += 1
                    return Token("MaiorIgual", ">=", inicio_linha, inicio_coluna)
                return Token("Maior", ">", inicio_linha, inicio_coluna)

            # Mapeia caracteres para tokens
            tipo_token = {
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

class TabelaSimbolos:
    """Gerencia os símbolos (variáveis e funções) do programa"""
    def __init__(self):
        self.global_scope = {}  # Escopo global
        self.local_scopes = []  # Pilha de escopos locais
        self.current_function = None  # Função atual sendo processada
    
    def entrar_funcao(self, func_info):
        """Entra em um novo escopo de função"""
        self.local_scopes.append({})
        self.current_function = func_info
    
    def sair_funcao(self):
        """Sai do escopo de função atual"""
        self.local_scopes.pop()
        self.current_function = None
    
    def declarar_global(self, nome, info):
        """Declara um símbolo no escopo global"""
        if nome in self.global_scope:
            raise ValueError(f"Símbolo '{nome}' já declarado no escopo global")
        self.global_scope[nome] = info
    
    def declarar_local(self, nome, info):
        """Declara um símbolo no escopo local atual"""
        if not self.local_scopes:
            raise ValueError("Não há escopo local ativo")
        
        if nome in self.local_scopes[-1]:
            raise ValueError(f"Símbolo '{nome}' já declarado no escopo local")
        
        self.local_scopes[-1][nome] = info
    
    def buscar(self, nome):
        """Busca um símbolo, primeiro no escopo local, depois no global"""
        # Busca nos escopos locais (do mais interno para o mais externo)
        for scope in reversed(self.local_scopes):
            if nome in scope:
                return scope[nome]
        
        # Se não encontrou, busca no escopo global
        if nome in self.global_scope:
            return self.global_scope[nome]
        
        return None

class ParserFun:
    """Parser para a linguagem Fun com funções"""
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.tabela_simbolos = TabelaSimbolos()

    def analisar_prim(self):
        """Analisa expressões primárias (números, variáveis, parênteses, chamadas de função)"""
        tok = self.lexer.proximo_token()
        
        if tok.tipo == "Numero":
            return Const(int(tok.lexema))
        elif tok.tipo == "Identificador":
            # Verifica se é chamada de função
            if self.lexer.olhar_proximo_token().tipo == "ParenEsq":
                self.lexer.proximo_token() # Consome o '('
                params = self.analisar_lista_parametros_chamada()
                if self.lexer.proximo_token().tipo != "ParenDir":
                    raise SyntaxError("Esperado ')' após lista de parâmetros")
                return FunCall(tok.lexema, params)
            else:
                return Var(tok.lexema)
        elif tok.tipo == "ParenEsq":
            exp = self.analisar_exp_comp()
            if self.lexer.proximo_token().tipo != "ParenDir":
                raise SyntaxError("Parêntese direito esperado")
            return exp
        else:
            raise SyntaxError(f"Token inesperado: {tok}")
    
    def analisar_lista_parametros_chamada(self):
        """Analisa a lista de parâmetros em uma chamada de função"""
        params = []
        if self.lexer.olhar_proximo_token().tipo != "ParenDir":
            params.append(self.analisar_exp_comp())
            while self.lexer.olhar_proximo_token().tipo == "Virgula":
                self.lexer.proximo_token() # Consome a ','
                params.append(self.analisar_exp_comp())
        return params

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
            if tok and tok.tipo in ["Menor", "Maior", "Igual", "MenorIgual", "MaiorIgual"]:
                op = self.lexer.proximo_token()
                dir = self.analisar_exp_a()
                esq = OpBin(op.lexema, esq, dir)
            else:
                break
        return esq
    
    def analisar_vardecl(self):
        """Analisa declaração de variável"""
        self.lexer.proximo_token()  # Consome 'var'
        var_tok = self.lexer.proximo_token()
        if var_tok.tipo != "Identificador":
            raise SyntaxError("Esperado identificador após 'var'")
        
        if self.lexer.proximo_token().tipo != "Atribuicao":
            raise SyntaxError("Esperado '=' na declaração de variável")
        
        exp = self.analisar_exp_comp()
        if self.lexer.proximo_token().tipo != "PontoVirgula":
            raise SyntaxError("Esperado ';' no final da declaração de variável")
        
        # Declara na tabela de símbolos
        if self.tabela_simbolos.current_function is None:
            # Variável global
            self.tabela_simbolos.declarar_global(var_tok.lexema, {'tipo': 'variavel_global'})
        
        return VarDecl(var_tok.lexema, exp)

    def analisar_fundecl(self):
        """Analisa declaração de função"""
        self.lexer.proximo_token()  # Consome 'fun'
        nome_tok = self.lexer.proximo_token()
        if nome_tok.tipo != "Identificador":
            raise SyntaxError("Esperado nome da função após 'fun'")
        
        if self.lexer.proximo_token().tipo != "ParenEsq":
            raise SyntaxError("Esperado '(' após nome da função")
        
        params = self.analisar_lista_parametros_funcao()
        if self.lexer.proximo_token().tipo != "ParenDir":
            raise SyntaxError("Esperado ')' após lista de parâmetros")
        
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' no início do corpo da função")
        
        corpo = []
        # Analisa declarações e comandos até o 'return'
        while self.lexer.olhar_proximo_token().tipo != "Return":
            if self.lexer.olhar_proximo_token().tipo == "Var":
                corpo.append(self.analisar_vardecl())
            else:
                corpo.append(self.analisar_comando())
        
        self.lexer.proximo_token()  # Consome 'return'
        resultado = self.analisar_exp_comp()
        if self.lexer.proximo_token().tipo != "PontoVirgula":
            raise SyntaxError("Esperado ';' após expressão de retorno")
        
        if self.lexer.proximo_token().tipo != "ChaveDir":
            raise SyntaxError("Esperado '}' no final do corpo da função")
        
        # Registra função na tabela de símbolos
        self.tabela_simbolos.declarar_global(nome_tok.lexema, {'tipo': 'funcao', 'params': params})
        
        return FunDecl(nome_tok.lexema, params, corpo, resultado)

    def analisar_lista_parametros_funcao(self):
        """Analisa a lista de parâmetros formais na declaração de função"""
        params = []
        if self.lexer.olhar_proximo_token().tipo == "Identificador":
            params.append(self.lexer.proximo_token().lexema)
            while self.lexer.olhar_proximo_token().tipo == "Virgula":
                self.lexer.proximo_token() # Consome a ','
                if self.lexer.olhar_proximo_token().tipo != "Identificador":
                    raise SyntaxError("Esperado identificador após vírgula na lista de parâmetros")
                params.append(self.lexer.proximo_token().lexema)
        return params
    
    def analisar_comando(self):
        """Analisa um comando (if, while, atribuição, chamada)"""
        tok = self.lexer.olhar_proximo_token()
        if tok.tipo == "If":
            return self.analisar_if()
        elif tok.tipo == "While":
            return self.analisar_while()
        elif tok.tipo == "Return":
            raise SyntaxError("'return' não é um comando válido aqui")
        elif tok.tipo == "Identificador":
            ident_tok = self.lexer.proximo_token()  # Consome o identificador
            next_tok = self.lexer.olhar_proximo_token()
            if next_tok.tipo == "Atribuicao":
                # Já consumimos o identificador, agora a atribuição será analisada
                self.lexer.proximo_token() # Consome o '='
                exp = self.analisar_exp_comp()
                if self.lexer.proximo_token().tipo != "PontoVirgula":
                    raise SyntaxError("Esperado ';' no final da atribuição")
                return Atrib(ident_tok.lexema, exp)
            elif next_tok.tipo == "ParenEsq":
                # Já consumimos o identificador, agora a chamada de função
                return self.analisar_chamada_funcao_como_comando(ident_tok.lexema)
            else:
                raise SyntaxError("Comando inválido: identificador não seguido de atribuição ou chamada de função")
        else:
            raise SyntaxError(f"Comando inesperado: {tok}")

    def analisar_chamada_funcao_como_comando(self, nome_func):
        """Analisa uma chamada de função como um comando (ex: soma();)"""
        self.lexer.proximo_token() # Consome o '('
        params = self.analisar_lista_parametros_chamada()
        if self.lexer.proximo_token().tipo != "ParenDir":
            raise SyntaxError("Esperado ')' após a lista de parâmetros da chamada de função")
        if self.lexer.proximo_token().tipo != "PontoVirgula":
            raise SyntaxError("Esperado ';' após a chamada de função como comando")
        return FunCall(nome_func, params) # Retorna um FunCall como um comando
    
    def analisar_if(self):
        """Analisa comando if"""
        self.lexer.proximo_token()  # Consome 'if'
        condicao = self.analisar_exp_comp()
        
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' após condição do 'if'")
        
        entao_cmds = []
        while self.lexer.olhar_proximo_token().tipo != "ChaveDir":
            entao_cmds.append(self.analisar_comando())
        self.lexer.proximo_token() # Consome '}'
        
        if self.lexer.proximo_token().tipo != "Else":
            raise SyntaxError("Esperado 'else' após bloco 'then'")
        
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' após 'else'")
        senao_cmds = []
        while self.lexer.olhar_proximo_token().tipo != "ChaveDir":
            senao_cmds.append(self.analisar_comando())
        self.lexer.proximo_token() # Consome '}'
        
        return If(condicao, entao_cmds, senao_cmds)

    def analisar_while(self):
        """Analisa comando while"""
        self.lexer.proximo_token()  # Consome 'while'
        condicao = self.analisar_exp_comp()
        
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' no início do corpo do 'while'")
        
        corpo = []
        while self.lexer.olhar_proximo_token().tipo != "ChaveDir":
            corpo.append(self.analisar_comando())
        self.lexer.proximo_token() # Consome '}'
        
        return While(condicao, corpo)
    
    def analisar_programa(self):
        """Analisa o programa completo"""
        declaracoes = []
        # Analisa declarações de variáveis e funções
        while self.lexer.olhar_proximo_token().tipo in ["Var", "Fun"]:
            if self.lexer.olhar_proximo_token().tipo == "Var":
                declaracoes.append(self.analisar_vardecl())
            else:
                declaracoes.append(self.analisar_fundecl())
        
        # Analisa o bloco main
        if self.lexer.proximo_token().tipo != "Main":
            raise SyntaxError("Esperado 'main' antes do bloco principal")
        if self.lexer.proximo_token().tipo != "ChaveEsq":
            raise SyntaxError("Esperado '{' após 'main'")
        
        comandos = []
        # Dentro do bloco main, só esperamos comandos, e não declarações.
        while self.lexer.olhar_proximo_token().tipo != "Return":
            comandos.append(self.analisar_comando())
        
        self.lexer.proximo_token()  # Consome 'return'
        resultado = self.analisar_exp_comp()
        if self.lexer.proximo_token().tipo != "PontoVirgula":
            raise SyntaxError("Esperado ';' após expressão de retorno do main")
        
        if self.lexer.proximo_token().tipo != "ChaveDir":
            raise SyntaxError("Esperado '}' no final do bloco principal")
        
        return ProgramaFun(declaracoes, comandos, resultado)

# Funções auxiliares para análise e interpretação

def analisar(entrada: str):
    """Analisa o código de entrada, retornando a árvore sintática"""
    lexer = Lexer(entrada)
    parser = ParserFun(lexer)
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

# Interpretação para a linguagem Fun (para testes)
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
        elif no.operador == '-':
            return esq - dir
        elif no.operador == '*':
            return esq * dir
        elif no.operador == '/':
            return esq // dir  # divisão inteira
        elif no.operador == '<':
            return 1 if esq < dir else 0
        elif no.operador == '>':
            return 1 if esq > dir else 0
        elif no.operador == '==':
            return 1 if esq == dir else 0
        elif no.operador == '<=':
            return 1 if esq <= dir else 0
        elif no.operador == '>=':
            return 1 if esq >= dir else 0
        raise ValueError(f"Operador desconhecido: {no.operador}")

    if isinstance(no, VarDecl):
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

    if isinstance(no, FunCall):
        # Interpreta chamada de função (se definida no contexto)
        func = contexto.get(no.nome)
        if func and isinstance(func, FunDecl):
            # Chama a função
            ctx_func = contexto.copy()
            for i, param in enumerate(func.params):
                if i < len(no.params):
                    ctx_func[param] = interpretar(no.params[i], contexto)
                else:
                    raise ValueError(f"Parâmetro {param} não fornecido na chamada de {no.nome}")
            
            # Executa corpo da função
            for cmd in func.corpo:
                if isinstance(cmd, VarDecl):
                    interpretar(cmd, ctx_func)
                else:
                    resultado = interpretar(cmd, ctx_func)
                    if resultado is not None:
                        return resultado
            
            # Retorna resultado
            return interpretar(func.resultado, ctx_func)
        else:
            raise NameError(f"Função não definida: {no.nome}")

    if isinstance(no, FunDecl):
        # Registra função no contexto
        contexto[no.nome] = no
        return None

    if isinstance(no, ProgramaFun):
        # Inicializa contexto com declarações globais
        for decl in no.declaracoes:
            if isinstance(decl, FunDecl):
                contexto[decl.nome] = decl
            else:
                interpretar(decl, contexto)

        # Executa comandos do main
        for cmd in no.main_comandos:
            res = interpretar(cmd, contexto)
            if res is not None:
                return res

        # Retorna resultado do main
        return interpretar(no.main_resultado, contexto)

    raise TypeError(f"Tipo de nó não suportado na interpretação: {type(no)}")

# Impressão de árvore sintática para debugging
def imprimir_arvore_simplificada(arvore, nivel=0):
    """Imprime a árvore sintática de forma simplificada"""
    indent = "  " * nivel
    
    if isinstance(arvore, ProgramaFun):
        print(f"{indent}PROGRAMA:")
        print(f"{indent}  Declarações:")
        for decl in arvore.declaracoes:
            imprimir_arvore_simplificada(decl, nivel + 2)
        print(f"{indent}  Main:")
        for cmd in arvore.main_comandos:
            imprimir_arvore_simplificada(cmd, nivel + 2)
        print(f"{indent}  Return:")
        imprimir_arvore_simplificada(arvore.main_resultado, nivel + 2)
    
    elif isinstance(arvore, FunDecl):
        print(f"{indent}FUNÇÃO {arvore.nome}({', '.join(arvore.params)}):")
        print(f"{indent}  Corpo:")
        for item in arvore.corpo:
            imprimir_arvore_simplificada(item, nivel + 2)
        print(f"{indent}  Return:")
        imprimir_arvore_simplificada(arvore.resultado, nivel + 2)
    
    elif isinstance(arvore, VarDecl):
        print(f"{indent}VAR {arvore.var} =")
        imprimir_arvore_simplificada(arvore.exp, nivel + 1)
    
    elif isinstance(arvore, If):
        print(f"{indent}IF:")
        print(f"{indent}  Condição:")
        imprimir_arvore_simplificada(arvore.condicao, nivel + 2)
        print(f"{indent}  Then:")
        for cmd in arvore.entao:
            imprimir_arvore_simplificada(cmd, nivel + 2)
        print(f"{indent}  Else:")
        for cmd in arvore.senao:
            imprimir_arvore_simplificada(cmd, nivel + 2)
    
    elif isinstance(arvore, While):
        print(f"{indent}WHILE:")
        print(f"{indent}  Condição:")
        imprimir_arvore_simplificada(arvore.condicao, nivel + 2)
        print(f"{indent}  Corpo:")
        for cmd in arvore.corpo:
            imprimir_arvore_simplificada(cmd, nivel + 2)
    
    elif isinstance(arvore, Atrib):
        print(f"{indent}ATRIBUIÇÃO {arvore.var} =")
        imprimir_arvore_simplificada(arvore.exp, nivel + 1)
    
    elif isinstance(arvore, FunCall):
        print(f"{indent}CHAMADA {arvore.nome}:")
        for i, param in enumerate(arvore.params):
            print(f"{indent}  Param {i+1}:")
            imprimir_arvore_simplificada(param, nivel + 2)
    
    elif isinstance(arvore, OpBin):
        print(f"{indent}OP {arvore.operador}:")
        print(f"{indent}  Esquerda:")
        imprimir_arvore_simplificada(arvore.op_esq, nivel + 2)
        print(f"{indent}  Direita:")
        imprimir_arvore_simplificada(arvore.op_dir, nivel + 2)
    
    elif isinstance(arvore, Var):
        print(f"{indent}VAR: {arvore.nome}")
    
    elif isinstance(arvore, Const):
        print(f"{indent}CONST: {arvore.valor}")
    
    else:
        print(f"{indent}[Desconhecido: {type(arvore)}]")
