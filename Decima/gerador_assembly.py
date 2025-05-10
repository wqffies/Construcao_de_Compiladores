# Alessandra Maria Ramos 20200136795
# Anna Myllenne Araújo 20220005899
# Enrique Pedrosa Sousa 20210026545
# Maria Sa Gurgel 20210025127
# Gisele Silva Gomes 20210025824

from arvore_sintatica_atividade10 import *

class GeradorCodigoFun:
    """Gera código assembly para a linguagem Fun"""
    def __init__(self, tabela_simbolos):
        self.tabela_simbolos = tabela_simbolos
        self.codigo = []
        self.label_counter = 0
        self.var_counter = 0
        self.variaveis_declaradas = set()
    
    def gerar_label(self):
        """Gera um novo label único"""
        self.label_counter += 1
        return f"L{self.label_counter}"
    
    def emit(self, instrucao):
        """Adiciona uma instrução ao código"""
        self.codigo.append(instrucao)
    
    def gerar_programa(self, programa):
        """Gera código para o programa completo"""
        # Seção BSS - variáveis globais
        self.codigo.append(".section .bss")
        
        # Declara variáveis globais
        for decl in programa.declaracoes:
            if isinstance(decl, VarDecl):
                self.codigo.append(f".lcomm {decl.var}, 8")
                self.variaveis_declaradas.add(decl.var)
        
        # Seção de texto
        self.codigo.append("")
        self.codigo.append(".section .text")
        self.codigo.append(".globl _start")
        
        # Gera código para as funções
        for decl in programa.declaracoes:
            if isinstance(decl, FunDecl):
                self.gerar_funcao(decl)
        
        # Ponto de entrada do programa
        self.codigo.append("_start:")
        
        # Inicializa variáveis globais
        for decl in programa.declaracoes:
            if isinstance(decl, VarDecl):
                self.gerar_expressao(decl.exp)
                self.emit(f"mov %rax, {decl.var}")
        
        # Gera código para o main
        for cmd in programa.main_comandos:
            self.gerar_comando(cmd)
        
        # Gera código para a expressão de retorno do main
        self.gerar_expressao(programa.main_resultado)
        
        # Finaliza o programa usando o estilo esperado
        self.emit("call imprime_num")
        self.emit("call sair")
        self.emit('.include "runtime.s"')

    def gerar_funcao(self, func):
        """Gera código para uma declaração de função"""
        # Busca informações da função (já declarada pelo parser)
        funcao_info = self.tabela_simbolos.buscar(func.nome)
        if not funcao_info:
            raise ValueError(f"Função '{func.nome}' não encontrada")
        
        # Entra no escopo da função
        self.tabela_simbolos.entrar_funcao(funcao_info)
        
        # Atualiza informações dos parâmetros
        offset = 24  # Começa após RBP (8) + ER (8) + parâmetros
        for i, param in enumerate(func.params):
            param_info = {
                'tipo': 'parametro',
                'offset': offset + i * 8,
                'escopo': 'local'
            }
            self.tabela_simbolos.declarar_local(param, param_info)
        
        # Rótulo da função
        self.emit(f"{func.nome}:")
        
        # Prólogo da função
        self.emit("push %rbp")
        
        # Calcula espaço necessário para variáveis locais
        local_vars = [d for d in func.corpo if isinstance(d, VarDecl)]
        local_space = len(local_vars) * 8
        
        if local_space > 0:
            self.emit(f"sub ${local_space}, %rsp")
        
        self.emit("mov %rsp, %rbp")
        
        # Processa variáveis locais
        for i, decl in enumerate(local_vars):
            if isinstance(decl, VarDecl):
                var_info = {
                    'tipo': 'variavel_local',
                    'offset': i * 8,
                    'escopo': 'local'
                }
                self.tabela_simbolos.declarar_local(decl.var, var_info)
                
                # Gera código para inicializar a variável
                self.gerar_expressao(decl.exp)
                self.emit(f"mov %rax, {i * 8}(%rbp)")
        
        # Gera código para comandos
        for item in func.corpo:
            if not isinstance(item, VarDecl):  # Pula declarações de variáveis
                self.gerar_comando(item)
        
        # Gera código para a expressão de retorno
        self.gerar_expressao(func.resultado)
        
        # Epílogo da função
        if local_space > 0:
            self.emit(f"add ${local_space}, %rsp")
        self.emit("pop %rbp")
        self.emit("ret")
        
        # Sai do escopo da função
        self.tabela_simbolos.sair_funcao()
        self.emit("")  # Linha em branco para separar funções
    
    def gerar_comando(self, cmd):
        """Gera código para um comando"""
        if isinstance(cmd, Atrib):
            self.gerar_atribuicao(cmd)
        elif isinstance(cmd, If):
            self.gerar_if(cmd)
        elif isinstance(cmd, While):
            self.gerar_while(cmd)
        elif isinstance(cmd, FunCall):
            self.gerar_expressao(cmd)  # Chamada de função como comando
    
    def gerar_atribuicao(self, atrib):
        """Gera código para uma atribuição"""
        # Gera código para a expressão
        self.gerar_expressao(atrib.exp)
        
        # Busca informações da variável
        var_info = self.tabela_simbolos.buscar(atrib.var)
        if not var_info:
            raise ValueError(f"Variável '{atrib.var}' não declarada")
        
        # Armazena o valor na variável
        if var_info['tipo'] == 'variavel_local' or var_info['tipo'] == 'parametro':
            self.emit(f"mov %rax, {var_info['offset']}(%rbp)")
        else:  # Variável global
            self.emit(f"mov %rax, {atrib.var}")
    
    def gerar_if(self, if_cmd):
        """Gera código para um comando if"""
        label_else = f"Lfalso{self.label_counter}"
        label_endif = f"Lfim{self.label_counter}"
        self.label_counter += 1
        
        # Gera código para a condição
        self.gerar_expressao(if_cmd.condicao)
        
        # Testa se a condição é falsa
        self.emit("cmp $0, %rax")
        self.emit(f"jz {label_else}")
        
        # Gera código para o bloco then
        for cmd in if_cmd.entao:
            self.gerar_comando(cmd)
        
        # Pula para o fim do if
        self.emit(f"jmp {label_endif}")
        
        # Label do else
        self.emit(f"{label_else}:")
        
        # Gera código para o bloco else
        for cmd in if_cmd.senao:
            self.gerar_comando(cmd)
        
        # Label do fim do if
        self.emit(f"{label_endif}:")
    
    def gerar_while(self, while_cmd):
        """Gera código para um loop while"""
        label_inicio = f"Linicio{self.label_counter}"
        label_fim = f"Lfim{self.label_counter}"
        self.label_counter += 1
        
        # Label do início do loop
        self.emit(f"{label_inicio}:")
        
        # Gera código para a condição
        self.gerar_expressao(while_cmd.condicao)
        
        # Testa se a condição é falsa
        self.emit("cmp $0, %rax")
        self.emit(f"jz {label_fim}")
        
        # Gera código para o corpo do loop
        for cmd in while_cmd.corpo:
            self.gerar_comando(cmd)
        
        # Volta para o início do loop
        self.emit(f"jmp {label_inicio}")
        
        # Label do fim do loop
        self.emit(f"{label_fim}:")
    
    def gerar_expressao(self, exp):
        """Gera código para uma expressão"""
        if isinstance(exp, Const):
            self.emit(f"mov ${exp.valor}, %rax")
        elif isinstance(exp, Var):
            self.gerar_var(exp)
        elif isinstance(exp, OpBin):
            self.gerar_op_binaria(exp)
        elif isinstance(exp, FunCall):
            self.gerar_chamada_funcao(exp)
    
    def gerar_var(self, var):
        """Gera código para acessar uma variável"""
        var_info = self.tabela_simbolos.buscar(var.nome)
        if not var_info:
            raise ValueError(f"Variável '{var.nome}' não declarada")
        
        if var_info['tipo'] == 'variavel_local' or var_info['tipo'] == 'parametro':
            self.emit(f"mov {var_info['offset']}(%rbp), %rax")
        else:  # Variável global
            self.emit(f"mov {var.nome}, %rax")
    
    def gerar_op_binaria(self, op):
        """Gera código para uma operação binária"""
        # Gera código para o lado esquerdo
        self.gerar_expressao(op.op_esq)
        self.emit("push %rax")
        
        # Gera código para o lado direito
        self.gerar_expressao(op.op_dir)
        
        # Recupera o lado esquerdo
        self.emit("pop %rbx")
        
        # Realiza a operação
        if op.operador == '+':
            self.emit("add %rbx, %rax")
        elif op.operador == '-':
            self.emit("sub %rbx, %rax")
        elif op.operador == '*':
            self.emit("imul %rbx, %rax")
        elif op.operador == '/':
            self.emit("xchg %rax, %rbx")
            self.emit("cqo")
            self.emit("idiv %rbx")
        elif op.operador == '<':
            self.emit("xor %rcx, %rcx")
            self.emit("cmp %rax, %rbx")
            self.emit("setl %cl")
            self.emit("mov %rcx, %rax")
        elif op.operador == '>':
            self.emit("xor %rcx, %rcx")
            self.emit("cmp %rax, %rbx")
            self.emit("setg %cl")
            self.emit("mov %rcx, %rax")
        elif op.operador == '==':
            self.emit("xor %rcx, %rcx")
            self.emit("cmp %rax, %rbx")
            self.emit("setz %cl")
            self.emit("mov %rcx, %rax")
        elif op.operador == '<=':
            self.emit("xor %rcx, %rcx")
            self.emit("cmp %rax, %rbx")
            self.emit("setle %cl")
            self.emit("mov %rcx, %rax")
        elif op.operador == '>=':
            self.emit("xor %rcx, %rcx")
            self.emit("cmp %rax, %rbx")
            self.emit("setge %cl")
            self.emit("mov %rcx, %rax")
    
    def gerar_chamada_funcao(self, call):
        """Gera código para uma chamada de função"""
        # Busca informações da função
        func_info = self.tabela_simbolos.buscar(call.nome)
        if not func_info:
            raise ValueError(f"Função '{call.nome}' não declarada")
        
        if func_info['tipo'] != 'funcao':
            raise ValueError(f"'{call.nome}' não é uma função")
        
        # Verifica número de parâmetros
        if len(call.params) != len(func_info['params']):
            raise ValueError(f"Função '{call.nome}' espera {len(func_info['params'])} parâmetros, mas {len(call.params)} foram fornecidos")
        
        # Empilha parâmetros na ordem inversa
        for param in reversed(call.params):
            self.gerar_expressao(param)
            self.emit("push %rax")
        
        # Chama a função
        self.emit(f"call {call.nome}")
        
        # Remove parâmetros da pilha
        if len(call.params) > 0:
            self.emit(f"add ${len(call.params) * 8}, %rsp")
