from damageable import Damageable

class KnowledgeLevel(Damageable):
    def __init__(self, value):
        super().__init__(value)  # knowledge level as a condition value