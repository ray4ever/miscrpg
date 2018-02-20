from copy import deepcopy

class Resistance:
    name = 'unknown'
    def __init__(self, value):
        self.value = value  # immediate Resistance


class PierceResistance(Resistance):
    name = 'piercing'


class SlashResistance(Resistance):
    name = 'slashing'


class CrushResistance(Resistance):
    name = 'crushing'


class MixedResistance:
    lst = []  # list of all resistances
    
    def __init__(self, lst):
        assert all(isinstance(x, Resistance) for x in lst), 'can only include a "resistance"' 
        self.lst = lst

    def add(self, resistance):
        assert isinstance(resistance, Resistance), 'can only add a "resistance"'
        self.lst.append(resistance)
