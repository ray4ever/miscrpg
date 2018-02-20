from muscular_system import MuscularCondition
from immune_system import ImmuneCondition
from sensory_system import SensoryCondition
from cardio_system import CardioCondition
from damageable import Damage, TurnBasedDamage, MixedDamage, SlashingDamage, BleedingDamage, CrushingDamage
from weapon import Limbs, Sword, NatureWeapon, Weapon
from armor import LeatherArmor, Skin
from rpg_logs import battle_log
from copy import deepcopy

class Living:
    name = 'unknown'
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
        self.weapon = Limbs()
        self.armor = Skin()
        for sub in self.turn_based:
            sub.owner = self.name  # no circular reference, just name

    def attack(self):
        adjusted = []
        if isinstance(self.weapon.damage, MixedDamage):
            damages = self.weapon.damage.lst
        else:
            damages = [self.weapon.damage]
        for damage in damages:
            dmg = deepcopy(damage)
            #TODO: check weapon type when dealing damages, firearms are not based on muscle condition
            dmg_value = int(dmg.value * (self.m.cur_value / 100))
            battle_log.add('%s weapon [%s] damage increased by muscle: %d -> %d' % (self.name, dmg.name, dmg.value, dmg_value))
            dmg.value = dmg_value
            adjusted.append(dmg)
        if len(adjusted) > 1:
            return MixedDamage(adjusted)
        else:
            return adjusted[0]

    def defend(self, damage):
        if self.armor is not None:
            damage = self.armor.resist(damage)
        self.take_damage(damage)

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
            x.take_turn()  # sub system may have turn-based effects, such as bleeding
            if x.cur_value < x.max_value:
                regen = self.regeneration()
                x.change_cur_value(regen)
                battle_log.add('%s [%s] condition regenerated by +%d' % (self.name, x.name, regen))

    def take_damage(self, damage):
        if isinstance(damage, MixedDamage):
            damages = damage.lst
        else:
            damages = [damage]  # make it a list
        for dmg in damages:
            if isinstance(dmg, SlashingDamage):
                self.m.take_damage(dmg)
            elif isinstance(dmg, BleedingDamage):
                self.c.take_damage(dmg)
            elif isinstance(dmg, CrushingDamage):
                self.s.take_damage(dmg)


class Intelligent(Living):
    def equip(self, weapon):
        assert isinstance(weapon, Weapon), '%s: must input instance of Weapon' % self.__class__.__name__
        self.weapon = weapon


if __name__ == "__main__":
    player = Intelligent('Player', 100, 100, 100, 100)
    player.equip(Sword())
    monster = Living('Monster', 500, 100, 50, 100)  # stronger muscle, but weaker sensory system
    monster.defend(player.attack())
    player.defend(monster.attack())
    for turn in range(0, 6):
        print('Turn %d' % turn)
        battle_log.flush()
        for being in [player, monster]:
            stats = [x.cur_value for x in being.damageable]
            print('%s %s (crippled=%s)' % (being.name, stats, being.is_crippled()))
            being.take_turn()
