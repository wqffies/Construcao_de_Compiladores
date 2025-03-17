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

def imprimir_arvore_centralizada(arvore):
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

def tokenizar(entrada: str):
    lexer = Lexer(entrada)
    tokens = []
    while True:
        token = lexer.proximo_token()
        tokens.append(token)
        if token.tipo == "EOF":
            break
    tokens = [token.lexema for token in tokens]
    return tokens[:-1]

def analisar(tokens):
    def prox_token():
        return tokens.pop(0) if tokens else None
    
    def analisar_expressao():
        tok = prox_token()
        if tok is None:
            raise SyntaxError("Expressão incompleta")
        
        if tok.isdigit():
            return Const(int(tok))
        elif tok == '(':
            esq = analisar_expressao()
            operador = prox_token()
            if operador not in '+-*/':
                raise SyntaxError(f"Operador inválido: {operador}")
            dir = analisar_expressao()
            if prox_token() != ')':
                raise SyntaxError("Parêntese não fechado corretamente")
            return OpBin(operador, esq, dir)
        else:
            raise SyntaxError(f"Token inesperado: {tok}")
    
    arvore = analisar_expressao()
    if tokens:
        raise SyntaxError("Tokens sobrando após análise")
    return arvore

def interpretar(arvore: Exp):
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
            return esq / dir
        else:
            raise ValueError(f"Operador desconhecido: {arvore.operador}")