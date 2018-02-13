class Damage:
    def __init__(self, value, permanent=False):
        self.value = value  # immediate damage
        self.is_permanent = permanent


class TurnBasedDamage(Damage):
    def __init__(self, value, turn_value=0, turns=0, permanent=False):
        super().__init__(value, permanent)
        self.turn_value = turn_value  # damage per turn
        self.turns = turns  # number of turns


class Damageable:
    def __init__(self, condition_value=1):
        self.cur_value = condition_value
        self.max_value = condition_value
        self.damages = []

    def take_damage(self, damage):
        if isinstance(damage, TurnBasedDamage):
            self.damages.append(damage)  # we need to track it
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
        if self.cur_value < 0:  # bounded by 0 and max
            self.cur_value = 0
        elif self.cur_value > self.max_value:
            self.cur_value = self.max_value

    def take_turn(self):
        damages = []
        for damage in self.damages:
            if damage.is_permanent:
                self.change_max_value(-damage.turn_value)
            else:
                self.change_cur_value(-damage.turn_value)
            damage.turns -= 1
            if damage.turns > 0:
                damages.append(damage)
        self.damages = damages