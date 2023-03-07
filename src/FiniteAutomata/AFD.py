""" The AFN class contains all the necessary properties to describe an AFD"""
# graphviz allow us to do an AFN grahp
import graphviz

# tabulate allow us to print the properties in a fancy way (it is not elementary)
from tabulate import tabulate

class Direct_AFD(object):
    def __init__(self,postfix):

        #Process variables
        self.binary_tree        = []
        self.followpost_table   = []
        self.numeral_id         = None
        self.postfix            = postfix
        self.numbering_exceptions   = list("*|.?+E")
        self.temporal_transitions   = []
        self.asignacion = {}

        '''AFD consist of:'''
        #The values of these variables will change

        # Initial state
        self.q_o = None
        # Transition function
        self.delta = {}
        # Input simbols
        self.sigma = set()
        # Finite set of states
        self.que = []
        # Acceptence states
        self.F = []

        # AFN and graph properties
        if self.postfix == 'ERROR':
            print(f'{"─"*117}')
            print(f'{"─"*51}AFD not avaiable{"─"*50}')
            print(f'{"─"*117}\n')
        else:
            self.postfix = self.postfix+'#.'
            print(f'AFD Postfix -> {self.postfix}\n')
            self.transform_postfix_to_afd()
            self.AFD_graph()
    # Function used in transform_postfix_to_afn to find the values ​​associated with a certain operator
    def child_node(self, father_position, arbol):

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

    def transform_postfix_to_afd(self):

        self.postfix = list(self.postfix)

        # Binary_tree fill
        for symbol in range(len(self.postfix)):
            self.binary_tree.append(AFD_node(self.postfix[symbol]))

        # Enumerate principal leafs and firstpos, lastpos, nullable and followpos_table
        initial_id = 1
        for leaf in self.binary_tree:
            if leaf.value not in self.numbering_exceptions:
                leaf.id = initial_id
                leaf.nullable = False
                leaf.firstpos.add(initial_id)
                leaf.lastpos.add(initial_id)
                self.followpost_table.append(AFD_followpos(leaf.value, initial_id))
                if leaf.value == '#':
                    self.numeral_id = initial_id
                initial_id += 1
            if leaf.value == 'E':
                leaf.nullable = True

        # Nullable function
        for position, leaf in enumerate(self.binary_tree):
            if leaf.value == '*':
                leaf.nullable = True

            elif leaf.value == '+':
                leaf.nullable = False

            elif leaf.value == '|':
                leaf.nullable = self.binary_tree[self.child_node(position, self.binary_tree)[1]].nullable or self.binary_tree[self.child_node(position, self.binary_tree)[0]].nullable
                self.binary_tree[self.child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '.':
                leaf.nullable = self.binary_tree[self.child_node(position, self.binary_tree)[1]].nullable and self.binary_tree[self.child_node(position, self.binary_tree)[0]].nullable
                self.binary_tree[self.child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

        # Cleaning binary_tree
        for leaf in self.binary_tree:
            leaf.analyzed = False

        # Firstpos function
        for position, leaf in enumerate(self.binary_tree):
            if leaf.value == '*':
                leaf.firstpos = self.binary_tree[self.child_node(position, self.binary_tree)[0]].firstpos
                self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '+':
                pass

            elif leaf.value == '|':
                leaf.firstpos = self.binary_tree[self.child_node(position, self.binary_tree)[1]].firstpos | self.binary_tree[self.child_node(position, self.binary_tree)[0]].firstpos
                self.binary_tree[self.child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '.':
                if self.binary_tree[self.child_node(position, self.binary_tree)[1]].nullable == True:
                    leaf.firstpos = self.binary_tree[self.child_node(position, self.binary_tree)[1]].firstpos  | self.binary_tree[self.child_node(position, self.binary_tree)[0]].firstpos
                    self.binary_tree[self.child_node(position, self.binary_tree)[1]].analyzed = True
                    self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True
                else:
                    leaf.firstpos = self.binary_tree[self.child_node(position, self.binary_tree)[1]].firstpos
                    self.binary_tree[self.child_node(position, self.binary_tree)[1]].analyzed = True
                    self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

        # Cleaning binary_tree
        for leaf in self.binary_tree:
            leaf.analyzed = False


        # Lastpos function

        for position, leaf in enumerate(self.binary_tree):
            if leaf.value == '*':
                leaf.lastpos = self.binary_tree[self.child_node(position, self.binary_tree)[0]].lastpos
                self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '+':
                pass

            elif leaf.value == '|':
                leaf.lastpos = self.binary_tree[self.child_node(position, self.binary_tree)[1]].lastpos | self.binary_tree[self.child_node(position, self.binary_tree)[0]].lastpos
                self.binary_tree[self.child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '.':
                if self.binary_tree[self.child_node(position, self.binary_tree)[0]].nullable == True:
                    leaf.lastpos = self.binary_tree[self.child_node(position, self.binary_tree)[1]].lastpos  | self.binary_tree[self.child_node(position, self.binary_tree)[0]].lastpos
                    self.binary_tree[self.child_node(position, self.binary_tree)[1]].analyzed = True
                    self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True
                else:
                    leaf.lastpos = self.binary_tree[self.child_node(position, self.binary_tree)[0]].lastpos
                    self.binary_tree[self.child_node(position, self.binary_tree)[1]].analyzed = True
                    self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

        # Cleaning binary_tree
        for leaf in self.binary_tree:
            leaf.analyzed = False

        # Binary Tree
        # print(f'--> Binary Tree:')
        # for leaf in self.binary_tree:
        #     print(leaf)

        # Followpos function
        for position, leaf in enumerate(self.binary_tree):
            if leaf.value == '*':
                A = self.binary_tree[self.child_node(position, self.binary_tree)[0]].lastpos
                B = self.binary_tree[self.child_node(position, self.binary_tree)[0]].firstpos

                self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

                for f_row in self.followpost_table:
                    if f_row.id in A:
                        f_row.followpos = f_row.followpos | B

            elif leaf.value == '+':
                pass

            elif leaf.value == '|':
                self.binary_tree[self.child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '.':
                A = self.binary_tree[self.child_node(position, self.binary_tree)[1]].lastpos
                B = self.binary_tree[self.child_node(position, self.binary_tree)[0]].firstpos

                self.binary_tree[self.child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[self.child_node(position, self.binary_tree)[0]].analyzed = True

                for f_row in self.followpost_table:
                    if f_row.id in A:
                        f_row.followpos = f_row.followpos | B

        # print(f'\n--> Followpos table:')
        # for f_row in self.followpost_table:
        #     print(f_row)



        # Alfabeto
        for char in self.postfix:
            if char not in self.numbering_exceptions and char != '#':
                self.sigma.add(char)
        # Transition function
        # self.delta.append(AFD_row(self.binary_tree[-1].firstpos,self.followpost_table, self.sigma))


        # print('\nTransiton creation\n')

        already_registrated = []
        already_registrated.append(self.binary_tree[-1].firstpos)
        self.q_o = str(self.binary_tree[-1].firstpos)
        self.que.append(str(self.binary_tree[-1].firstpos))

        while len(already_registrated) != 0:
            self.temporal_transitions.append(AFD_row(already_registrated.pop(), self.followpost_table, self.sigma))

            for p_new_state in self.temporal_transitions[-1].different_states:
                if str(p_new_state) != 'set()':
                    if str(p_new_state) not in self.que and p_new_state not in already_registrated:
                        already_registrated.append(p_new_state)
                        self.que.append(str(p_new_state))

        for transition in self.temporal_transitions:
            self.delta[str(transition.state)] = {}
        for state in self.delta:
            for letter in self.sigma:
                self.delta[state][letter] = []


        for afd_row in self.delta:
            for transition in self.temporal_transitions:
                if str(transition.state) == afd_row:
                    for letter in self.sigma:
                        if str(transition.transitions[letter]) != 'set()':
                            self.delta[afd_row][letter].append(str(transition.transitions[letter]))

        for afd_row in self.delta:
            for state in afd_row:
                if state == str(self.numeral_id):
                    self.F.append(afd_row)

        # Pasar de numeros a letras
        abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if len(self.que)<27:
            for position, state in enumerate(self.que):
                self.asignacion[str(state)] = abecedario[position]
            self.que    = [self.asignacion[state] for state in self.que]
            self.F      = [self.asignacion[state] for state in self.F]
            self.q_o    = self.asignacion[self.q_o]

            delta_letras = {}
            for conjunto, valores in self.delta.items():
                letra = self.asignacion[str(conjunto)]
                valores_letras = {}
                for k, v in valores.items():
                    valores_letras[k] = [self.asignacion[s] if s in self.asignacion else s for s in v]
                delta_letras[letra] = valores_letras
            self.delta = delta_letras
        """AFD FINAL RESULTS"""

        print(f'{"─"*117}')
        print(f'\n{"─"*50}AFD final results{"─"*50}\n')
        print(f'{"─"*117}\n')

        """ Final prints without tabulate"""

        # print(f'\nEstados ->{self.que}')
        # print(f'Transiciones ->\n')

        # for x in self.delta:
        #     print(x, "", self.delta[x])

        # print(f'\nSimbolos -> {self.sigma}')
        # print(f'Estados de aceptacion -> {self.F}')
        # print(f'Estado inicial-> {self.q_o}\n')

        """ Fancy prints with tabulate"""
        AFD_proporties = [
            ["Estados", self.que],
            ["Simbolos", self.sigma],
            ["Estados de aceptacion", self.F],
            ["Estado inicial", self.q_o],
        ]
        print(tabulate(AFD_proporties, tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')

        AFD_delta = []
        for key, value in self.delta.items():
            subtable = []
            for subkey, subvalue in value.items():
                subtable.append([subkey, subvalue])
            AFD_delta.append([key, tabulate(subtable, tablefmt="plain", numalign="center", stralign="left")])

        print(tabulate(AFD_delta, headers=['Estado             ', 'Transicion'], tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')


    def AFD_graph(self):
        # Graficas
        f= graphviz.Digraph(name="AFD_directo")
        f.attr(rankdir='LR')


        for x, y in self.delta.items():
            if x in self.F:
                f.node(str(x), shape = "doublecircle", style = 'filled', fillcolor = 'lightblue')
            elif x == self.q_o:
                f.node(str(x), shape = "circle", style = 'filled', fillcolor = 'lightgreen')
            else:
                f.node(str(x), shape = "circle")

        for x in self.delta:
            for y in self.delta[x]:
                    if len(self.delta[x][y]) != 0:
                        for w in self.delta[x][y]:
                            f.edge(x,w, label = y, arrowhead='vee')

        f.node("", height = "0",width = "0", shape = "box")
        f.edge("",self.q_o, arrowhead='vee', )
        # f.render("./src/GraphedFiniteAutomata/Direct_AFD", format="png", view="True")
        f.render("./src/GraphedFiniteAutomata/Direct_AFD", format="png")

class AFD_row(object):
    def __init__(self, state, f_table, sigma):
        self.f_table    = f_table
        self.alphabet   = sigma

        self.different_states  = []


        self.state      = state
        self.transitions    = {}
        self.states_values = []

        for char in self.alphabet:
            self.transitions[char] = set()

        for state in self.state:
            for f_row in self.f_table:
                if state == f_row.id:
                    self.states_values.append(f_row)

        for char in self.alphabet:
            for state_value in self.states_values:
                if char == state_value.value:
                    self.transitions[char] = self.transitions[char] | state_value.followpos

        # print('---------------------')
        # for x in self.states_values:
        #     print(x)

        for tran in self.transitions:
            if self.transitions[tran] != self.state and str(self.transitions[tran] != 'set()'):
                self.different_states.append(self.transitions[tran])

        # Remove duplicate elements
        self.different_states = list(set([tuple(element) for element in self.different_states]))
        self.different_states = [set(element) for element in self.different_states]


    def __str__(self):
        # return f"Estado: {self.state} Estados creados: {self.different_states} Transitions:{self.transitions}"
        return f"Estado: {self.state} Transitions:{self.transitions}"

class AFD_node(object):
    def __init__(self, value, id=None):

        self.id         = id
        self.value      = value
        self.nullable   = None
        self.firstpos   = set([])
        self.lastpos    = set([])
        self.analyzed   = False


    def __str__(self):
        cadena="Id:" +str(self.id)+"\t\t"+self.value+"\t\tNullable:" +str(self.nullable)+"\t\tFirstpos:" +str(self.firstpos)+"\t\tLastpos:" +str(self.lastpos)
        return cadena

class AFD_followpos(object):
    def __init__(self,value,id):
        self.id         = id
        self.value      = value
        self.followpos = set([])

    def __str__(self):
        return f" Id: {self.id}\tValue: {self.value}\tFollowpos: {self.followpos}"


