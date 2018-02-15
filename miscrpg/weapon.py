from damageable import Damage, SlashingDamage, BleedingDamage, MixedDamage, CrushingDamage


class Weapon:
    def __init__(self, damage):
        assert isinstance(damage, Damage) or isinstance(damage, MixedDamage), 'must input instance of Damage'
        self.damage = damage
    

class ColdWeapon(Weapon):
    pass


class Sword(ColdWeapon):
    def __init__(self):
        super().__init__(MixedDamage([
            SlashingDamage(30),
            BleedingDamage(2, 10)
        ]))


class NatureWeapon(Weapon):
    pass


class Fist(NatureWeapon):
    def __init__(self):
        super().__init__(CrushingDamage(5))
