from damageable import Damageable

class ImmuneCondition(Damageable):
    def __init__(self, value):
        super().__init__(value)  # immune system condition as a value