from damageable import Owner, Damageable, Damage, SlashingDamage, BleedingDamage, SeqDamage, CrushingDamage


class Weapon(Damageable):
    def __init__(self, damage, condition):
        assert isinstance(damage, Damage) or isinstance(damage, SeqDamage), 'must input instance of Damage'
        super().__init__(condition)  # how many use until broken
        self.damage = damage
    

class Sword(Weapon):
    name = 'sword'
    weight = 5
    def __init__(self):
        super().__init__(SeqDamage([
            SlashingDamage(30),
            BleedingDamage(2, 10)  # bleeding for 10 turns if not treated
        ]), 100)


class Club(Weapon):
    name = 'club'
    weight = 10
    def __init__(self):
        super().__init__(SeqDamage([
            CrushingDamage(15)
        ]), 500)


class NatureWeapon(Weapon):
    weight = 0
    def __init__(self, damage, owner):
        assert isinstance(damage, Damage) or isinstance(damage, SeqDamage), 'must input instance of Damage'
        super().__init__(damage, 0)  # natural weapon does not have own condition, it purely relies on owner muscle
        self.set_owner(owner)
        self.damage = damage


class Limbs(NatureWeapon):
    name = 'limbs'
    def __init__(self, owner):
        super().__init__(CrushingDamage(5), owner)
