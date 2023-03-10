"""
Autor: Gabriel Vicente (20498)
Proyecto: Laboratorio B

Descripción:
Laboratorio B para la clase Diseño de Lenguajes
Generar AFN a partir de una expresión regular
Generar AFD a partir de una expresión regular
Generar AFD a partir de AFN
Minimización de AFD
Simulación de AFN y AFD

Tomando en cuenta operaciones y abreviaturas
[* , + , . , ? , |]

Al igual que la jerarquia de los parentesis
"""

#Imports needed for lab A
from Tools.InfixToPostfix import *
from Tools.utils import *
from FiniteAutomata.AFN import *
from FiniteAutomata.AFD import *
from FiniteAutomata.AFD_minimization import *

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
"sfgsg(a|b)(a|b)*ab(c?)asdfaslakjsdfhalsdkjfhalskjfdd"
"""

# Description
description()

# Regex request
regex = "(a|b)(a|b)*ab(c?)"
# regex = input('Enter a regular expression from which to generate your AFN: ')

#Postfix to AFN
print(f'\n{InfixToPostfix(regex)}\n')

# AFN
NFA  = AFN(InfixToPostfix(regex).postfix)

# AFD from AFN
DFA_from_NFA = AFD_from_AFN(NFA)

# Direct AFD
# DFA    = Direct_AFD(InfixToPostfix(regex).postfix)

# MInimization AFD form AFN
DFA_minized = AFD_min(DFA_from_NFA)
