from damageable import Owner, Damageable, Damage, SlashingDamage, BleedingDamage, MixedDamage, CrushingDamage


class Weapon(Damageable):
    def __init__(self, damage, condition):
        assert isinstance(damage, Damage) or isinstance(damage, MixedDamage), 'must input instance of Damage'
        super().__init__(condition)  # how many use until broken
        self.damage = damage
    

class Sword(Weapon):
    name = 'sword'
    def __init__(self):
        super().__init__(MixedDamage([
            SlashingDamage(30),
            BleedingDamage(2, 10)  # bleeding for 10 turns if not treated
        ]), 100)


class Club(Weapon):
    name = 'club'
    def __init__(self):
        super().__init__(MixedDamage([
            CrushingDamage(15)
        ]), 500)


class NatureWeapon(Weapon):
    def __init__(self, damage, owner):
        assert isinstance(damage, Damage) or isinstance(damage, MixedDamage), 'must input instance of Damage'
        super().__init__(damage, 0)  # natural weapon does not have own condition, it purely relies on owner muscle
        self.set_owner(owner)
        self.damage = damage


class Limbs(NatureWeapon):
    name = 'limbs'
    def __init__(self, owner):
        super().__init__(CrushingDamage(5), owner)
