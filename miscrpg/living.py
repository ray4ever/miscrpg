from muscular_system import MuscularCondition
from immune_system import ImmuneCondition
from sensory_system import SensoryCondition
from cardio_system import CardioCondition
from damageable import Damage, TurnBasedDamage, MixedDamage, SlashingDamage, BleedingDamage, CrushingDamage
from weapon import Fist, Sword, NatureWeapon, ColdWeapon, Weapon
from copy import deepcopy

class Living:
    CRIPPLED_THRESHOLD = 0.6

    def __init__(self, name='nameless', muscular=1, immune=1, sensory=1, cardio=1, perks=[]):
        self.name = name
        self.m = MuscularCondition(muscular)  # strength, mobility
        self.i = ImmuneCondition(immune)  # resistence to discease, poison
        self.s = SensoryCondition(sensory)  # initiative, ranged attack, precision (criticals)
        self.c = CardioCondition(cardio)  # energy, regeneration
        self.perks = perks
        self.turn_based = [self.m, self.i, self.s, self.c]
        self.damageable = [self.m, self.i, self.s, self.c]
        self.weapon = Fist()

    def attack(self):
        adjusted = []
        if isinstance(self.weapon.damage, MixedDamage):
            damages = self.weapon.damage.lst
        else:
            damages = [self.weapon.damage]
        for damage in damages:
            dmg = deepcopy(damage)
            if isinstance(self.weapon, NatureWeapon):
                dmg.value = int(dmg.value * (self.m.cur_value / 100))
            elif isinstance(self.weapon, ColdWeapon):
                dmg.value = int(dmg.value * (self.m.cur_value / 100))
            adjusted.append(dmg)
        if len(adjusted) > 1:
            return MixedDamage(adjusted)
        else:
            return adjusted[0]

    def health(self):
        return self.m.cur_value * self.s.cur_value // 100

    def energy(self):
        return self.c.cur_value // 10

    def regeneration(self):
        return self.c.cur_value // 70  # fail to regenrate if cardio condition lower than 70%

    def is_dead(self):
        return self.s.cur_value == 0 and len(self.s.damages) == 0  # permanent nerve zero

    def is_disabled(self):
        return self.m.cur_value == 0

    def is_crippled(self):
        return (self.m.cur_value / self.m.max_value) < Living.CRIPPLED_THRESHOLD

    def is_paralyzed(self):
        return self.s.cur_value == 0

    def take_turn(self):
        for x in self.turn_based:
            x.take_turn()
            x.change_cur_value(self.regeneration())

    def take_damage(self, damage):
        if isinstance(damage, MixedDamage):
            damages = damage.lst
        else:
            damages = [damage]  # make it list
        for dmg in damages:
            if isinstance(dmg, SlashingDamage):
                self.m.take_damage(dmg)
            elif isinstance(dmg, BleedingDamage):
                self.c.take_damage(dmg)
            elif isinstance(dmg, CrushingDamage):
                self.s.take_damage(dmg)


class Intelligent(Living):
    def equip(self, weapon):
        assert isinstance(weapon, Weapon), 'must input instance of Weapon'
        self.weapon = weapon


if __name__ == "__main__":
    player = Intelligent('Player', 100, 100, 100, 100)
    player.equip(Sword())
    monster = Living('Monster', 500, 100, 50, 100)  # stronger muscle, but weaker sensory system
    monster.take_damage(player.attack())
    player.take_damage(monster.attack())
    for turn in range(0, 11):
        print('Turn %d' % turn)
        for being in [player, monster]:
            stats = [x.cur_value for x in being.damageable]
            print('%s %s (crippled=%s)' % (being.name, stats, being.is_crippled()))
            being.take_turn()
