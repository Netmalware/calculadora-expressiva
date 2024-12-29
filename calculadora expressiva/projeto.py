__author__ = "Kevin Moreira"

# Juro que não sou bom em Matemática! #

import keyboard
import sys
import threading
import time
import re
from simpleeval import simple_eval, InvalidExpression

def analisar(expressao, variaveis={}):
    try:
        if not re.match(r'^[\d+\-*/().^,\s\w]+$', expressao):
            raise ValueError("Expressão contém caracteres inválidos. Apenas números, operadores (+, -, *, /, ^), parênteses, espaços e variáveis são permitidos.")
        
        if re.search(r'([+\-*/^]{2,})', expressao):
            raise ValueError("Expressão contém operadores consecutivos inválidos.")
        
        resultado = simple_eval(expressao, variables=variaveis)
        return resultado
    except InvalidExpression as e:
        raise ValueError(f"Erro de sintaxe na expressão: {str(e)}")
    except ZeroDivisionError:
        raise ValueError("Divisão por zero não permitida.")
    except Exception as e:
        raise ValueError(f"Erro desconhecido: {str(e)}")

def sair():
    print("Ctrl + End pressionado! Programa encerrado.")
    sair_programa.set()

sair_programa = threading.Event()

keyboard.add_hotkey('ctrl+end', sair)

def monitorar_teclas():
    while not sair_programa.is_set():
        if keyboard.is_pressed('ctrl+end'):
            sair()
            break
        time.sleep(0.1)

teclado_thread = threading.Thread(target=monitorar_teclas, daemon=True)
teclado_thread.start()

variaveis = {}

print("Pressione Ctrl + End para sair.")

while not sair_programa.is_set():
    entrada = input("[calcular]: ")

    try:
        if not entrada.strip():
            raise ValueError("Entrada não pode ser vazia. Por favor, forneça uma expressão válida.")

        if "definir" in entrada.lower():
            match = re.match(r"definir\s+(\w+)\s*=\s*(.+)", entrada.strip(), re.IGNORECASE)
            if match:
                variavel_nome = match.group(1)
                variavel_valor = match.group(2)
                try:
                    variaveis[variavel_nome] = simple_eval(variavel_valor, variables=variaveis)
                    print(f"Variável '{variavel_nome}' definida com o valor: {variaveis[variavel_nome]}")
                except Exception as e:
                    print(f"Falha ao definir a variável: {e}")
            else:
                print("Formato de definição de variável inválido. Use 'definir nome = valor'.")
        else:
            resultado = analisar(entrada, variaveis)
            print(f"Resultado: {resultado:.4f}" if isinstance(resultado, float) else f"Resultado: {resultado}")

    except ValueError as e:
        print(f"Falhou: {e}")
    except Exception as e:
        print(f"Falhou: Erro desconhecido - {e}")

teclado_thread.join()


# This project was made using:
#
# Microsoft Visual Studio Code v.1.96.2 - Integrated Development Enviroment used for develop this calculator
# OpenAI ChatGPT 4.0 Mini (Free version) - For some complex tasks and processes, in addition of logic variables 
# Python.org Website - For research of used libraries in this project 
# Wikipedia - Where i read about logarithm terms, some math functions and how apply it correctly.

# Please Rate, comment, edit and interact with me to help in my works and study.

# Thanks for look up this project.