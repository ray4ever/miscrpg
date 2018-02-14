from muscular_system import MuscularCondition
from immune_system import ImmuneCondition
from sensory_system import SensoryCondition
from cardio_system import CardioCondition
from damageable import Damage, TurnBasedDamage, MixedDamage, SlashingDamage, BleedingDamage

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

    def take_damage(self, damages):
        if isinstance(damages, MixedDamage):
            damages = damages.lst
        else:
            damages = [damages]  # make it list
        for damage in damages:
            if isinstance(damage, SlashingDamage):
                self.m.take_damage(damage)
            elif isinstance(damage, BleedingDamage):
                self.c.take_damage(damage)


if __name__ == "__main__":
    player = Living('Player', 100, 100, 100, 100)
    monster = Living('Monster', 500, 100, 50, 100)  # stronger muscle, but weaker sensory system
    slashed_and_bleeding = TurnBasedDamage(30, 2, 10)
    sword_damage = MixedDamage([
        SlashingDamage(30),
        BleedingDamage(2, 10)
    ])
    player.take_damage(sword_damage)
    monster.take_damage(sword_damage)
    for turn in range(0, 11):
        print('Turn %d' % turn)
        for being in [player, monster]:
            stats = [x.cur_value for x in being.damageable]
            print('%s %s (crippled=%s)' % (being.name, stats, being.is_crippled()))
            being.take_turn()
