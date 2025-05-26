# Interpretador REPL em Python

Este projeto implementa um **interpretador interativo** no estilo **REPL** (*Read–Eval–Print–Loop*), escrito em Python, com suporte a expressões matemáticas e manipulação de variáveis.

---

## Objetivo

O objetivo deste interpretador é permitir que o usuário:

* Avalie expressões matemáticas, como `2 + 3 * (4 - 1)`
* Defina variáveis com expressões, como `x = 5 + 2`
* Reutilize essas variáveis em novas expressões, como `x * 3`

---

## Como Funciona

O interpretador funciona em um laço contínuo que realiza as seguintes etapas:

1. **Read (Ler):** Lê a entrada digitada pelo usuário.
2. **Eval (Avaliar):** Interpreta a entrada, substitui variáveis por seus valores e avalia o resultado usando `eval()`.
3. **Print (Imprimir):** Exibe o resultado da expressão ou a definição da variável.
4. **Loop (Repetir):** Continua esperando novas entradas até que o usuário digite `sair`.

---

## Funcionalidades

* Avaliação de expressões matemáticas com operadores `+`, `-`, `*`, `/` e parênteses.
* Declaração e reuso de variáveis.
* Execução contínua até o comando `sair`.
* Tratamento de erros comuns, como:

  * Uso de variáveis não declaradas
  * Expressões malformadas

---

## Exemplos de Uso

```bash
>>> 2 + 3 * (4 - 1)
11

>>> x = 5
x = 5

>>> y = x + 7
y = 12

>>> y / 2
6.0

>>> sair
```
