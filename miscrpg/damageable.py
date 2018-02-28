from copy import deepcopy
from rpg_logs import battle_log

class Damage:
    name = 'unknown'
    def __init__(self, value, permanent=False):
        self.value = value  # immediate damage
        self.is_permanent = permanent


class TurnBasedDamage(Damage):
    def __init__(self, value, turn_value=0, turns=0, permanent=False):
        super().__init__(value, permanent)
        self.turn_value = turn_value  # damage per turn
        self.turns = turns  # number of turns


class PiercingDamage(Damage):
    name = 'piercing'


class SlashingDamage(Damage):
    name = 'slashing'


class CrushingDamage(Damage):
    name = 'crushing'


class BleedingDamage(TurnBasedDamage):
    name = 'bleeding'
    def __init__(self, turn_value=0, turns=0, permanent=False):
        super().__init__(0, turn_value, turns, permanent)


class MixedDamage:
    lst = []  # list of all damages
    def __init__(self, lst):
        assert all(isinstance(x, Damage) for x in lst), 'can only include a "damage"' 
        self.lst = lst

    def add(self, damage):
        assert isinstance(damage, Damage), 'can only add a "damage"'
        self.lst.append(damage)


class Owner:
    """owner of damageable item, must have name
    """
    name = None


class Damageable:
    """Damageable thing has a condition value, if the value is zero, it losts its functionality,
       if the value is -max_value, it's no longer repairable
    """

    name = 'unknown'
    owner = Owner()

    def __init__(self, condition_value=1):
        self.cur_value = condition_value
        self.max_value = condition_value
        self.damages = []

    def set_owner(self, owner):
        assert isinstance(owner, Owner), 'only an Owner can own this'
        self.owner = owner

    def take_damage(self, damage):
        if isinstance(damage, TurnBasedDamage):
            self.damages.append(deepcopy(damage))  # we need to track it
        if damage.is_permanent:
            self.max_value -= damage.value  # hurt max value
        else:
            self.cur_value -= damage.value

    def change_max_value(self, delta):
        self.max_value += delta
        if self.cur_value > self.max_value:
            self.cur_value = self.max_value

    def change_cur_value(self, delta):
        self.cur_value += delta
        if self.cur_value > self.max_value:
            self.cur_value = self.max_value
        if self.cur_value < -self.max_value:
            self.cur_value = -self.max_value

    def value(self):
        return self.cur_value if self.cur_value > 0 else 0  # its value coming from it's functionable

    def is_broken(self):
        return self.cur_value <= -self.max_value  # cannot be repaired

    def take_turn(self):
        damages = []
        for damage in self.damages:
            if damage.is_permanent:
                self.change_max_value(-damage.turn_value)
                battle_log.add('%s suffered permanent [%s] damage on [%s] -%d' % (self.owner, damage.name, self.name, damage.turn_value))
            else:
                self.change_cur_value(-damage.turn_value)
                battle_log.add('%s suffered [%s] damage on [%s] -%d' % (self.owner, damage.name, self.name, damage.turn_value))
            damage.turns -= 1
            if damage.turns > 0:
                damages.append(damage)
        self.damages = damages
