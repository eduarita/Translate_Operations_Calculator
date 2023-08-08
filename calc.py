import ply.lex as lex

# lex.py se utiliza para tokenizar una cadena de entrada
calc = True
# Lista de nombres de tokens
tokens = [
    'NUMERO',
    'SUMA',
    'RESTA',
    'DIVISION',
    'MULTIPLICACION',
    'LLAVEIZQ',
    'LLAVEDER'
]

# Indicamos Reglas Lexicas con Expresiones regulares
"""
t_  en PLY se utiliza para definir un token con una expresion regular.

La r significa que la cadena debe tratarse como una cadena sin procesar, 
lo que significa que se ignorarán todos los códigos de escape.
Ej: '\n' se tratará como un carácter de nueva línea, 
mientras que r'\n' se tratará como los caracteres \ seguido de n.
"""
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_LLAVEIZQ = r'\('
t_LLAVEDER = r'\)'

# Expresión regular para los números
def t_NUMERO(token):
     #\d: Digitos del 0-9, + Coincide con 1 o más de los token anterior.
    r'\d+'
    token.value = int(token.value)
    return token

# Se ignorarán espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores si no coincide un token
def t_error(token):
  print("Token no coincide con gramática '%s'" % token.value[0])
  token.lexer.skip(1)

# Construcción del Analizador Léxico
lexer = lex.lex()

#App
while calc:
  print("Calculadora")
  print("Escriba S para salir")
  user = input()
  formatedTokens = []
  if(user.lower() == 's'):
    break

  # Se pasa al analizador léxico los datos
  """
  Los tokens del Analizador Lexico son tuplas, que contiene:
  Tipo de token, el valor del token, posición del token, etc.
  """
  lexer.input(user)
  tokenDict = {}
  # Se realiza Tokenización
  for tok in lexer:
    formatedTokens.append((tok.type, tok.value))

  for tokenType, tokenValue in formatedTokens:
    print(f"{tokenType}: {tokenValue}", end=", ")
  print()

