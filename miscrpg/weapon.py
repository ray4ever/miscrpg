from damageable import Damage, SlashingDamage, BleedingDamage, MixedDamage, CrushingDamage


class Weapon:
    def __init__(self, damage):
        assert isinstance(damage, Damage) or isinstance(damage, MixedDamage), 'must input instance of Damage'
        self.damage = damage
    

class Sword(Weapon):
    def __init__(self):
        super().__init__(MixedDamage([
            SlashingDamage(30),
            BleedingDamage(2, 10)  # bleeding for 10 turns if not treated
        ]))


class Club(Weapon):
    def __init__(self):
        super().__init__(MixedDamage([
            CrushingDamage(30)
        ]))


class NatureWeapon(Weapon):
    pass


class Limbs(NatureWeapon):
    def __init__(self):
        super().__init__(CrushingDamage(5))
