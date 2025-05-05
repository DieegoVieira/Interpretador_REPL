# Interpretador REPL em Python

variaveis = {}

def parse_expression(expr):
    try:
        # Substitui variáveis pelos valores no dicionário
        for var in variaveis:
            expr = expr.replace(var, str(variaveis[var]))

        resultado = eval(expr)
        return resultado
    except NameError as e:
        raise Exception("Variável não definida.")
    except Exception as e:
        raise Exception(f"Erro na expressão: {e}")

def interpret(linha):
    if '=' in linha:
        var, expr = linha.split('=', 1)
        var = var.strip()
        expr = expr.strip()
        if not var.isidentifier():
            raise Exception(f"Nome de variável inválido: {var}")
        valor = parse_expression(expr)
        variaveis[var] = valor
        print(f"{var} = {valor}")
    else:
        resultado = parse_expression(linha.strip())
        print(resultado)

def repl():
    print("Interpretador REPL Python (digite 'sair' para encerrar)")
    while True:
        try:
            linha = input(">>> ")
            if linha.strip().lower() == "sair":
                break
            interpret(linha)
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    repl()
