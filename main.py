"""
Autor: Gabriel Vicente (20498)
Proyecto: Laboratorio A

Descripción:
Laboratorio A para la clase Diseño de Lenguajes
Generar AFN a partir de una expresión regular

Tomando en cuenta operaciones y abreviaturas
[* , + , . , ? , |]

Al igual que la jerarquia de los parentesis
"""

#Imports needed for lab A
from Tools.InfixToPostfix import *
from FiniteAutomata.AFN import *
from FiniteAutomata.AFD import *

#REGEX EXAMPLES
"""
"ab*ab*"
"0?(1?)?0*"
"(a*|b*)c"
"(a|b)*abb"
"(a|E)b(a+)c?"
"(b|b)*abb(a|b)*"
"(a|b)*a(a|b)(a|b)"
"(a|b)(a|b)*ab(c?)"
"""

# Description

print(f'\n{"─"*117}\n{"─"*50}WELCOME TO LAB A!{"─"*50}\n{"─"*85} Auth. Gabriel Vicente 20498 UVG\n')
print(' --> Note that')
print('\t*\tSpace is not a valid transition')
print('\t*\tEpsilon is represented by our \"E\" character ')
print('\t*\tIf you wanna use our program again you need to close the generated pdf')
print('\t*\tThe AFN will be generated only if regex is valid\n')

# Regex request
regex = "(a|b)(a|b)*ab(c?)"
# regex = input('Enter a regular expression from which to generate your AFN: ')

#Postfix to AFN
print(f'\n{InfixToPostfix(regex)}\n')
# AFN(InfixToPostfix(regex).postfix)
Direct_AFD(InfixToPostfix(regex).postfix)

























#AFN

#Validación de AFN

#AFD a partir de AFN

#Validacion de AFD a partir de AFN

#AFD directo

#Validacion de AFD directo
