from damageable import Damageable

class SensoryCondition(Damageable):
    name = 'senses'

    def __init__(self, value):
        super().__init__(value)  # sensory system condition as a value