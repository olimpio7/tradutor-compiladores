from analisador_lexico import tokenizar

PRIMEIRO_EXPR = ("(", "num", "id")


class ErroSintatico(Exception):
    pass


class Parser:
    def __init__(self, src):
        self.toks = tokenizar(src)
        self.pos = 0
        self.buf = []
        self.saida = []

    @property
    def atual(self):
        return self.toks[self.pos]

    def casar(self, tipo):
        t = self.atual
        if t.tipo != tipo:
            self.erro(f"esperado '{tipo}'")
        self.pos += 1
        return t

    def erro(self, msg):
        t = self.atual
        enc = "fim do arquivo" if t.tipo == "EOF" else f"'{t.lexema}'"
        raise ErroSintatico(f"Linha {t.linha}: {msg}, encontrado {enc}")

    def program(self):
        self.casar("Matexpr")
        self.block()
        self.casar("EOF")
        return self.saida

    def block(self):
        self.casar("{")
        while self.atual.tipo == "type":
            self.decl()
        self.stmts()
        self.casar("}")

    def decl(self):
        self.casar("type")
        self.casar("id")
        self.casar(";")

    def stmts(self):
        while self.atual.tipo == "{" or self.atual.tipo in PRIMEIRO_EXPR:
            self.stmt()

    def stmt(self):
        if self.atual.tipo == "{":
            self.block()
        elif self.atual.tipo in PRIMEIRO_EXPR:
            self.expr()
            self.casar(";")
            self.saida.append(" ".join(self.buf))
            self.buf = []
        else:
            self.erro("esperado comando ou '}'")

    def expr(self):
        self.term()
        while self.atual.tipo in ("+", "-"):
            op = self.casar(self.atual.tipo).lexema
            self.term()
            self.buf.append(op)

    def term(self):
        self.fact()
        while self.atual.tipo in ("*", "/"):
            op = self.casar(self.atual.tipo).lexema
            self.fact()
            self.buf.append(op)

    def fact(self):
        t = self.atual
        if t.tipo == "(":
            self.casar("(")
            self.expr()
            self.casar(")")
        elif t.tipo in ("num", "id"):
            self.buf.append(self.casar(t.tipo).lexema)
        else:
            self.erro("esperado expressão (número, id ou '(')")