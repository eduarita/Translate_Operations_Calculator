import shutil
import ply.lex as lex
import ply.yacc as yacc

# lex.py se utiliza para tokenizar una cadena de entrada
calc = True

#----------ANALIZADOR LEXICO----------

# Lista de nombres de tokens
tokens = [
    'NUMERO',
    'SUMA',
    'RESTA',
    'DIVISION',
    'MULTIPLICACION',
    'LLAVEIZQ',
    'LLAVEDER',
    "POTENCIA",
    "DECIMAL",
    'OPERAR',
    'CORCHIZQ',
    'CORCHDER',
    'FINCAD'
]

# Indicamos Reglas Lexicas con Expresiones regulares
# Definir las expresiones regulares que identifiquen cuándo
# Ocurren los tokens anteriores

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
t_POTENCIA = r'\^'
t_OPERAR = "OPERAR"
t_CORCHIZQ = r'\['
t_CORCHDER = r'\]'
t_FINCAD = r'\$'


# Al declarar los numeros decimales y enteros, se declaran primero los decimales
# Luego, se declaran los enteros

# Expresión regular para los números decimales
def t_DECIMAL(token):
      #\d\.\d: Uno o más digitos seguido de PUNTO DECIMAL seguido de uno o más digitos
      r'\d+\.\d+'
      token.value = float(token.value)
      return token

# Expresión regular para los números enteros
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

#----------FIN ANALIZADOR LEXICO----------


#----------ANALIZADOR SINTÁCTICO----------

#Tupla para definir y agrupar la precedencia de las operaciones
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'POTENCIA', 'MULTIPLICACION', 'DIVISION'),
    ('right', 'UMENOS'),
    ('left', 'LLAVEIZQ', 'LLAVEDER'),
    ('left', 'CORCHIZQ', 'CORCHDER'),
)

#Definir la gramatica BNF a utilizar
resultados = []
operacion = {}

def p_instrucciones_lista(t):
    '''instrucciones    : instruccion instrucciones
                        | instruccion '''   
    
def p_instrucciones_operar(t):
    'instruccion : OPERAR CORCHIZQ expresion CORCHDER FINCAD'
    resultados.append([t[3]])
    operacion[t[1]] = t[3]

    print('El resultado de la expresión es: ' + str(t[3]))

def p_instrucciones_expr(t):
    'instruccion : expresion'
    print(t[1])

def p_expresion_binaria(t):
    '''expresion : expresion SUMA expresion
                  | expresion RESTA expresion
                  | expresion MULTIPLICACION expresion
                  | expresion DIVISION expresion
                  | expresion POTENCIA expresion'''

    try:
        if t[2] == '+'  : t[0] = t[1] + t[3]
        elif t[2] == '-': t[0] = t[1] - t[3]
        elif t[2] == '*': t[0] = t[1] * t[3]
        elif t[2] == '/': t[0] = t[1] / t[3]
        elif t[2] == '^': t[0] = pow(t[1] , t[3])
    except ZeroDivisionError:
        error = "Error, División por cero"
        print(error)

def p_expresion_unaria(t):
    'expresion : RESTA expresion %prec UMENOS'
    t[0] = -t[2]

def p_expresion_agrupacion(t):
    'expresion : LLAVEIZQ expresion LLAVEDER'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion    : NUMERO
                    | DECIMAL'''
    t[0] = t[1]

def p_error(t):
    operacion["OPERAR"] = 0

    print("Error sintáctico en '%s'" % t.value)

#----------FIN ANALIZADOR SINTÁCTICO----------

# Construcción del Analizador Léxico
lexer = lex.lex()

# Construcción del analizador sintáctico
parser = yacc.yacc()

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

  expresion = "OPERAR[%s]$" %(user)
  print("La cadena de entrada es: " + expresion)
  parser.parse(expresion)
  resultado = operacion["OPERAR"]
  lexer.input(user)
  tokenDict = {}

  # Se realiza Tokenización y se imprimen los datos
  for tok in lexer:
    formatedTokens.append((tok.type, tok.value))

  for tokenType, tokenValue in formatedTokens:
    print(f" {tokenType}: {tokenValue}", end=", ")
  print()

