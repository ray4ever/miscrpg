from damageable import Damageable

class MuscularCondition(Damageable):
    name = 'muscle'

    def __init__(self, value):
        super().__init__(value)  # muscular system condition as value