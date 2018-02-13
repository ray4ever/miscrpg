from muscular_system import MuscularCondition
from immune_system import ImmuneCondition
from sensory_system import SensoryCondition
from cardio_system import CardioCondition
from damageable import Damage, TurnBasedDamage

class Living:
    CRIPPLED_THRESHOLD = 0.6

    def __init__(self, muscular=1, immune=1, sensory=1, cardio=1, perks=[]):
        self.m = MuscularCondition(muscular)  # strength, mobility
        self.i = ImmuneCondition(immune)  # resistence to discease, poison
        self.s = SensoryCondition(sensory)  # initiative, ranged attack, precision (criticals)
        self.c = CardioCondition(cardio)  # energy, agility
        self.perks = perks
        self.turn_based = [self.m, self.i, self.s, self.c]

    def health(self):
        return self.m.cur_value * self.s.cur_value

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


if __name__ == "__main__":
    player = Living(100, 100, 100, 100)
    monster = Living(500, 100, 50, 100)  # stronger muscle, but weaker sensory system
    slashed_and_bleeding = TurnBasedDamage(30, 2, 10)
    player.m.take_damage(slashed_and_bleeding)
    for turn in range(0, 11):
        print('Turn %d' % turn)
        print('Player health= %d (crippled=%s)' % (player.health(), player.is_crippled()))
        player.take_turn()
