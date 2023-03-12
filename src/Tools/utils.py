# graphviz allow us to do an AFN grahp
import graphviz

# tabulate allow us to print the properties in a fancy way (it is not elementary)
from tabulate import tabulate

def description():
    print(f'\n{"─"*117}\n{"─"*50}WELCOME TO LAB A!{"─"*50}\n{"─"*85} Auth. Gabriel Vicente 20498 UVG\n')
    print(' --> Note that')
    print('\t*\tSpace is not a valid transition')
    print('\t*\tEpsilon is represented by our \"E\" character ')
    print('\t*\tIf you wanna use our program again you need to close the generated pdf')
    print('\t*\tThe AFN will be generated only if regex is valid\n')

def banner(header, row_jumps = True):
    value   = 120
    banner = "{:─^120}".format(header)

    print(f'{"─"*value}')

    if row_jumps:
        print(f'\n{banner}\n')
    else:
        print(f'{banner}')
    print(f'{"─"*value}\n')

def child_node(father_position, arbol):

    # Space to save the children position
    children = []

    # Position where the analysis begin
    to_analize = father_position - 1

    # While we are not out the array the process continues
    while (to_analize != -1):

        # If the analyzed property is False it represents a child
        # we appende this position to our result
        if arbol[to_analize].analyzed == False and len(children) < 2:
            children.append(to_analize)

        # We substract a position until the while es False
        to_analize -= 1

    # We return the children
    return children

def finite_automaton_graph(F,q_o,delta, titulo):
    f= graphviz.Digraph(name=titulo)
    f.attr(rankdir='LR')


    for x, y in delta.items():
        if x in F:
            f.node(str(x), shape = "doublecircle", style = 'filled', fillcolor = 'lightblue')
        elif x == q_o:
            f.node(str(x), shape = "circle", style = 'filled', fillcolor = 'lightgreen')
        else:
            f.node(str(x), shape = "circle")

    for x in delta:
        for y in delta[x]:
                if len(delta[x][y]) != 0:
                    for w in delta[x][y]:
                        f.edge(x,w, label = y, arrowhead='vee')

    f.node("", height = "0",width = "0", shape = "box")
    f.edge("",q_o, arrowhead='vee')
    render = "./src/GraphedFiniteAutomata/"+titulo
    f.render(render, format="png", view="True")

def finite_automaton_results(que,sigma,F,q_o,delta, tabulation = True):
    if tabulation:
        Properties = [
            ["Estados", que],
            ["Simbolos", sigma],
            ["Estados de aceptacion", F],
            ["Estado inicial", q_o],
        ]

        print(tabulate(Properties, tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')

        Delta = []
        for key, value in delta.items():
            subtable = []
            for subkey, subvalue in value.items():
                subtable.append([subkey, subvalue])
            Delta.append([key, tabulate(subtable, tablefmt="plain", numalign="center", stralign="left")])

        print(tabulate(Delta, headers=['Estado             ', 'Transicion'], tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')
    else:
        print(f'\nEstados ->{que}')
        print(f'Transiciones ->\n')

        for x in delta:
            print(x, "", delta[x])

        print(f'\nSimbolos -> {sigma}')
        print(f'Estados de aceptacion -> {F}')
        print(f'Estado inicial-> {q_o}\n')

def letter_rename(numero):
    tabla = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I',
            '9': 'J', '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R',
            '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y', '25': 'Z'}

    if numero > 25:
        letras = []
        for digito in str(numero):
            letras.append(tabla[digito])
        return ''.join(letras)
    else:
        letras = []
        letras.append(tabla[str(numero)])
        return ''.join(letras)


# Previos process register

        # Easy read
        # delta_letras = {}
        # for conjunto, valores in self.delta.items():
        #     letra = self.asignacion[str(conjunto)]
        #     valores_letras = {}
        #     for k, v in valores.items():
        #         valores_letras[k] = [self.asignacion[s] if s in self.asignacion else s for s in v]
        #     delta_letras[letra] = valores_letras
        # self.delta = delta_letras