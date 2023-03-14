"""
Clase que permite realizar la minimización de un AFD a partir de obtener su quintupla
Referencia: https://users.exa.unicen.edu.ar/catedras/ccomp1/ClaseAFNDMinimizacion.pdf
"""


# utils is usefull to rename the sets and prints
from Tools.utils import *

class AFD_min(object):
    def __init__(self, AFD):
        self.AFD = AFD
        self.subsets = {}

        ''' AFD min consist of:'''
        #The values of these variables will change

        # Initial state
        self.q_o    = None
        # Transition function
        self.delta  = {}
        # Input simbols
        self.sigma  = []
        # Finite set of states
        self.que    = []
        # Acceptence states
        self.F      = []

        if self.AFD.postfix == 'ERROR':
            banner(' Min AFD not available ', False)
        else:
            self.transform_afd_to_afd_min()
            # finite_automaton_graph(self.F, self.q_o, self.delta,'AFD_min')

    def transform_afd_to_afd_min(self):

        self.sigma = self.AFD.sigma

        self.delta = {str(state): {} for state in self.que}
        self.delta = {x: {letra: [] for letra in self.sigma} for x in self.delta}
        
        
        