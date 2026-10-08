import sys
from analisador_lexico import ErroLexico
from analisador_sintatico import Parser, ErroSintatico


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py arquivo.txt")
        sys.exit(1)
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            src = f.read()
        for linha in Parser(src).program():
            print(linha)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {sys.argv[1]}")
        sys.exit(1)
    except (ErroLexico, ErroSintatico) as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()