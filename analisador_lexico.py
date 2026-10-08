import string


class ErroLexico(Exception):
    pass


class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha


SIMBOLOS = "+-*/(){};"


def tokenizar(texto):
    tokens = []
    pos = 0
    linha = 1

    while pos < len(texto):
        c = texto[pos]

        if c == "\n":
            linha += 1
            pos += 1

        elif c in " \t\r":
            pos += 1

        elif texto.startswith("//", pos):
            while pos < len(texto) and texto[pos] != "\n":
                pos += 1

        elif texto.startswith("/*", pos):
            fim = texto.find("*/", pos + 2)
            if fim == -1:
                raise ErroLexico(f"Linha {linha}: comentário não fechado")
            linha += texto.count("\n", pos, fim)
            pos = fim + 2

        elif c.isdigit():
            inicio = pos
            while pos < len(texto) and texto[pos].isdigit():
                pos += 1
            if pos < len(texto) and texto[pos] == ".":
                pos += 1
                if pos >= len(texto) or not texto[pos].isdigit():
                    raise ErroLexico(f"Linha {linha}: número float malformado")
                while pos < len(texto) and texto[pos].isdigit():
                    pos += 1
            tokens.append(Token("num", texto[inicio:pos], linha))

        elif c in string.ascii_letters:
            inicio = pos
            while pos < len(texto) and texto[pos] in string.ascii_letters:
                pos += 1
            palavra = texto[inicio:pos]
            if palavra == "Matexpr":
                tokens.append(Token("Matexpr", palavra, linha))
            elif palavra in ("int", "float"):
                tokens.append(Token("type", palavra, linha))
            else:
                tokens.append(Token("id", palavra, linha))

        elif c in SIMBOLOS:
            tokens.append(Token(c, c, linha))
            pos += 1

        else:
            raise ErroLexico(f"Linha {linha}: caractere inválido '{c}'")

    tokens.append(Token("EOF", "", linha))
    return tokens