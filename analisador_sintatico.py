from analisador_lexico import tokenizar

PRIMEIRO_EXPR = ("(", "num", "id")


class ErroSintatico(Exception):
    pass


class Parser:
    def __init__(self, texto):
        self.tokens = tokenizar(texto)
        self.pos = 0
        self.traducao = []
        self.saida = []

    def atual(self):
        return self.tokens[self.pos]

    def casar(self, tipo):
        token = self.atual()
        if token.tipo != tipo:
            self.erro(f"esperado '{tipo}'")
        self.pos += 1
        return token

    def erro(self, mensagem):
        token = self.atual()
        if token.tipo == "EOF":
            encontrado = "fim do arquivo"
        else:
            encontrado = f"'{token.lexema}'"
        raise ErroSintatico(f"Linha {token.linha}: {mensagem}, encontrado {encontrado}")

    def program(self):
        self.casar("Matexpr")
        self.block()
        self.casar("EOF")
        return self.saida

    def block(self):
        self.casar("{")
        self.decls()
        self.stmts()
        self.casar("}")

    def decls(self):
        while self.atual().tipo == "type":
            self.decl()

    def decl(self):
        self.casar("type")
        self.casar("id")
        self.casar(";")

    def stmts(self):
        while self.atual().tipo == "{" or self.atual().tipo in PRIMEIRO_EXPR:
            self.stmt()

    def stmt(self):
        if self.atual().tipo == "{":
            self.block()
        else:
            self.expr()
            self.casar(";")
            self.saida.append(" ".join(self.traducao))
            self.traducao = []

    def expr(self):
        self.term()
        while self.atual().tipo in ("+", "-"):
            operador = self.casar(self.atual().tipo).lexema
            self.term()
            self.traducao.append(operador)

    def term(self):
        self.fact()
        while self.atual().tipo in ("*", "/"):
            operador = self.casar(self.atual().tipo).lexema
            self.fact()
            self.traducao.append(operador)

    def fact(self):
        token = self.atual()
        if token.tipo == "(":
            self.casar("(")
            self.expr()
            self.casar(")")
        elif token.tipo in ("num", "id"):
            self.traducao.append(self.casar(token.tipo).lexema)
        else:
            self.erro("esperado expressão (número, id ou '(')")