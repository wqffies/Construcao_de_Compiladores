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
            # Restaura o estado anterior
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

            # Ignorar espaços em branco e atualizar posição
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

            # Números: lê até encontrar um caractere não numérico
            if char.isdigit():
                num_str = char
                self.posicao += 1
                self.coluna += 1
                while self.posicao < self.tamanho and self.entrada[self.posicao].isdigit():
                    num_str += self.entrada[self.posicao]
                    self.posicao += 1
                    self.coluna += 1
                return Token("Numero", num_str, inicio_linha, inicio_coluna)

            # Parênteses e operadores
            tipo_token = {
                '(': "ParenEsq",
                ')': "ParenDir",
                '+': "Soma",
                '-': "Sub",
                '*': "Mult",
                '/': "Div"
            }.get(char)

            if tipo_token:
                token = Token(tipo_token, char, inicio_linha, inicio_coluna)
                self.posicao += 1
                self.coluna += 1
                return token

            # Erro léxico
            raise ValueError(f"Símbolo inválido '{char}' na linha {self.linha}, coluna {self.coluna}")

        # Retorna um token EOF ao final da entrada
        return Token("EOF", "", self.linha, self.coluna)

class Exp:
    pass

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

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def analisar_prim(self):
        """Análise de expressões primárias (números ou expressões entre parênteses)"""
        tok = self.lexer.proximo_token()
        
        if tok.tipo == "Numero":
            return Const(int(tok.lexema))
        
        if tok.tipo == "ParenEsq":
            # Recursão para expressão aditiva dentro dos parênteses
            exp = self.analisar_exp_a()
            
            # Verifica fechamento de parênteses
            tok_fecha = self.lexer.proximo_token()
            if tok_fecha.tipo != "ParenDir":
                raise SyntaxError("Parêntese não fechado corretamente")
            
            return exp
        
        raise SyntaxError(f"Token inesperado: {tok}")

    def analisar_exp_m(self):
        """Análise de expressões multiplicativas"""
        esq = self.analisar_prim()
        
        # Verifica próximo token sem consumir
        tok = self.lexer.olhar_proximo_token()
        
        # Repete enquanto encontrar operadores de multiplicação/divisão
        while tok and tok.tipo in ["Mult", "Div"]:
            # Consome o operador
            op_token = self.lexer.proximo_token()
            
            # Analisa próximo operando primário
            dir = self.analisar_prim()
            
            # Cria nó de operação binária
            esq = OpBin(op_token.lexema, esq, dir)
            
            # Atualiza próximo token
            tok = self.lexer.olhar_proximo_token()
        
        return esq

    def analisar_exp_a(self):
        """Análise de expressões aditivas"""
        esq = self.analisar_exp_m()
        
        # Verifica próximo token sem consumir
        tok = self.lexer.olhar_proximo_token()
        
        # Repete enquanto encontrar operadores de soma/subtração
        while tok and tok.tipo in ["Soma", "Sub"]:
            # Consome o operador
            op_token = self.lexer.proximo_token()
            
            # Analisa próximo termo multiplicativo
            dir = self.analisar_exp_m()
            
            # Cria nó de operação binária
            esq = OpBin(op_token.lexema, esq, dir)
            
            # Atualiza próximo token
            tok = self.lexer.olhar_proximo_token()
        
        return esq

def interpretar(arvore: Exp):
    """Interpreta a árvore de expressão"""
    if isinstance(arvore, Const):
        return arvore.valor
    elif isinstance(arvore, OpBin):
        esq = interpretar(arvore.op_esq)
        dir = interpretar(arvore.op_dir)
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

def analisar(entrada: str):
    """Função de conveniência para análise de expressões"""
    lexer = Lexer(entrada)
    parser = Parser(lexer)
    arvore = parser.analisar_exp_a()
    
    # Verifica se todos os tokens foram consumidos
    tok_final = lexer.proximo_token()
    if tok_final.tipo != "EOF":
        raise SyntaxError("Tokens sobrando após análise")
    
    return arvore

def tokenizar(entrada: str):
    """Tokenização da entrada"""
    lexer = Lexer(entrada)
    tokens = []
    while True:
        token = lexer.proximo_token()
        tokens.append(token)
        if token.tipo == "EOF":
            break
    return [token.lexema for token in tokens][:-1]

def imprimir_arvore_centralizada(arvore):
    """Mantida a função original de impressão da árvore"""
    if not isinstance(arvore, OpBin) and not isinstance(arvore, Const):
        return
    
    def altura(arvore):
        if isinstance(arvore, Const):
            return 1
        return 1 + max(altura(arvore.op_esq), altura(arvore.op_dir))
    
    def preencher_niveis(arvore, nivel, posicao, largura, matriz, conexoes):
        if arvore is None:
            return
        
        meio = (posicao[0] + posicao[1]) // 2
        matriz[nivel][meio] = str(arvore.operador if isinstance(arvore, OpBin) else arvore.valor)
        
        if isinstance(arvore, OpBin):
            esq_meio = (posicao[0] + meio - 1) // 2
            dir_meio = (meio + 1 + posicao[1]) // 2
            conexoes[nivel + 1][esq_meio] = '/'
            conexoes[nivel + 1][dir_meio] = '\\'
            preencher_niveis(arvore.op_esq, nivel + 2, (posicao[0], meio - 1), largura, matriz, conexoes)
            preencher_niveis(arvore.op_dir, nivel + 2, (meio + 1, posicao[1]), largura, matriz, conexoes)
    
    h = altura(arvore)
    largura = 2 ** h  # largura da matriz
    matriz = [[' ' for _ in range(largura)] for _ in range(h * 2)]
    conexoes = [[' ' for _ in range(largura)] for _ in range(h * 2)]
    
    preencher_niveis(arvore, 0, (0, largura - 1), largura, matriz, conexoes)
    
    for i in range(h * 2):
        linha = ''.join(conexoes[i]) if i % 2 else ''.join(matriz[i])
        print(linha.rstrip())
