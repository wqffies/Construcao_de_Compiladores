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
