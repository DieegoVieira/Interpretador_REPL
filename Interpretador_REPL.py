class Simbolo:
    def __init__(self, categoria, conteudo):
        self.categoria = categoria
        self.conteudo = conteudo

    def __repr__(self):
        return f'Simbolo({self.categoria}, "{self.conteudo}")'


from enum import Enum

class CategoriaSimbolo(Enum):
    SOMA = '+'
    SUBTRACAO = '-'
    MULTIPLICACAO = '*'
    DIVISAO = '/'
    NUMERO = 'NUM'
    IDENTIFICADOR = 'ID'
    IGUAL = '='
    PARENTESE_ESQ = '('
    PARENTESE_DIR = ')'
    FIM = 'EOF'

class AnalisadorLexico:
    def __init__(self, texto):
        self.texto = texto
        self.indice = 0
        self.caractere = texto[0] if texto else ''

    def avancar(self):
        self.indice += 1
        self.caractere = self.texto[self.indice] if self.indice < len(self.texto) else ''

    def ignorar_espacos(self):
        while self.caractere and self.caractere.isspace():
            self.avancar()

    def capturar_numero(self):
        acumulador = ''
        while self.caractere and (self.caractere.isdigit() or self.caractere == '.'):
            acumulador += self.caractere
            self.avancar()
        return Simbolo(CategoriaSimbolo.NUMERO, acumulador)

    def capturar_nome(self):
        acumulador = ''
        while self.caractere and (self.caractere.isalnum() or self.caractere == '_'):
            acumulador += self.caractere
            self.avancar()
        return Simbolo(CategoriaSimbolo.IDENTIFICADOR, acumulador)

    def proximo_simbolo(self):
        while self.caractere:
            if self.caractere.isspace():
                self.ignorar_espacos()
                continue

            if self.caractere.isdigit():
                return self.capturar_numero()

            if self.caractere.isalpha() or self.caractere == '_':
                return self.capturar_nome()

            simbolos_diretos = {
                '+': CategoriaSimbolo.SOMA,
                '-': CategoriaSimbolo.SUBTRACAO,
                '*': CategoriaSimbolo.MULTIPLICACAO,
                '/': CategoriaSimbolo.DIVISAO,
                '=': CategoriaSimbolo.IGUAL,
                '(': CategoriaSimbolo.PARENTESE_ESQ,
                ')': CategoriaSimbolo.PARENTESE_DIR
            }

            if self.caractere in simbolos_diretos:
                categoria = simbolos_diretos[self.caractere]
                self.avancar()
                return Simbolo(categoria, categoria.value)

            raise Exception(f"Caractere inválido: {self.caractere}")

        return Simbolo(CategoriaSimbolo.FIM, '')

class InterpretadorSintatico:
    def __init__(self, lexico, contexto):
        self.lexico = lexico
        self.contexto = contexto
        self.simbolo = self.lexico.proximo_simbolo()

    def aceitar(self, esperado):
        if self.simbolo.categoria == esperado:
            self.simbolo = self.lexico.proximo_simbolo()
        else:
            raise Exception(f"Esperado {esperado}, mas encontrado {self.simbolo.categoria}")

    def fator(self):
        simb = self.simbolo
        if simb.categoria == CategoriaSimbolo.PARENTESE_ESQ:
            self.aceitar(CategoriaSimbolo.PARENTESE_ESQ)
            resultado = self.expressao()
            self.aceitar(CategoriaSimbolo.PARENTESE_DIR)
            return resultado
        elif simb.categoria == CategoriaSimbolo.NUMERO:
            self.aceitar(CategoriaSimbolo.NUMERO)
            return float(simb.conteudo)
        elif simb.categoria == CategoriaSimbolo.IDENTIFICADOR:
            nome = simb.conteudo
            self.aceitar(CategoriaSimbolo.IDENTIFICADOR)
            if nome not in self.contexto:
                raise Exception(f'Variável "{nome}" não definida')
            return self.contexto[nome]
        else:
            raise Exception("Fator inválido")

    def termo(self):
        resultado = self.fator()
        while self.simbolo.categoria in (CategoriaSimbolo.MULTIPLICACAO, CategoriaSimbolo.DIVISAO):
            if self.simbolo.categoria == CategoriaSimbolo.MULTIPLICACAO:
                self.aceitar(CategoriaSimbolo.MULTIPLICACAO)
                resultado *= self.fator()
            elif self.simbolo.categoria == CategoriaSimbolo.DIVISAO:
                self.aceitar(CategoriaSimbolo.DIVISAO)
                resultado /= self.fator()
        return resultado

    def expressao(self):
        resultado = self.termo()
        while self.simbolo.categoria in (CategoriaSimbolo.SOMA, CategoriaSimbolo.SUBTRACAO):
            if self.simbolo.categoria == CategoriaSimbolo.SOMA:
                self.aceitar(CategoriaSimbolo.SOMA)
                resultado += self.termo()
            elif self.simbolo.categoria == CategoriaSimbolo.SUBTRACAO:
                self.aceitar(CategoriaSimbolo.SUBTRACAO)
                resultado -= self.termo()
        return resultado

    def executar_comando(self):
        if self.simbolo.categoria == CategoriaSimbolo.IDENTIFICADOR:
            nome_var = self.simbolo.conteudo
            token_backup = self.simbolo
            indice_backup = self.lexico.indice
            caractere_backup = self.lexico.caractere
            self.aceitar(CategoriaSimbolo.IDENTIFICADOR)

            if self.simbolo.categoria == CategoriaSimbolo.IGUAL:
                self.aceitar(CategoriaSimbolo.IGUAL)
                valor = self.expressao()
                self.contexto[nome_var] = valor
            else:
                self.lexico.indice = indice_backup - len(token_backup.conteudo)
                self.lexico.caractere = self.lexico.texto[self.lexico.indice]
                self.simbolo = self.lexico.proximo_simbolo()
                valor = self.expressao()
                print(f'Resultado: {valor}')
        else:
            valor = self.expressao()
            print(f'Resultado: {valor}')

def principal():
    print('🔢 Interpretador simples (digite "sair" para encerrar)')
    memoria = {}
    while True:
        try:
            entrada = input('>>> ')
            if entrada.strip().lower() == 'sair':
                break
            analisador = InterpretadorSintatico(AnalisadorLexico(entrada), memoria)
            analisador.executar_comando()
        except Exception as erro:
            print(f'⚠️ Erro: {erro}')

if __name__ == '__main__':
    principal()
