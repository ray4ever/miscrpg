from damageable import Damageable

class CardioCondition(Damageable):
    def __init__(self, value):
        super().__init__(value)  # cardio system condition as a value