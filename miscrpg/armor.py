from resistance import Resistance, SlashResistance, CrushResistance, PierceResistance, MixedResistance
from damageable import Damageable, Damage, MixedDamage, SlashingDamage, CrushingDamage, PiercingDamage
from rpg_logs import battle_log


damage_resistance_map = {
    SlashingDamage.name: SlashResistance.name,
    CrushingDamage.name: CrushResistance.name,
    PiercingDamage.name: PierceResistance.name,
    Damage.name: CrushResistance.name  # unknown damage defaults crushing, mostly not used
}


class Armor(Damageable):
    def __init__(self, condition, resistance):
        assert isinstance(resistance, Resistance) or isinstance(resistance, MixedResistance), 'must input instance of Resistance'
        super().__init__(condition)
        if isinstance(resistance, MixedResistance):
            self.resistances = resistance.lst
        else:
            self.resistances = [resistance]

    def resist(self, damage):
        if self.cur_value > 0:  # armor condition > 0 to resist
            if isinstance(damage, MixedDamage):
                damages = damage.lst
            else:
                damages = [damage]
            for dmg in damages:
                assert dmg.name and dmg.name != 'unknown', '%s: damage name must be known' % self.name
                for r in self.resistances:
                    if damage_resistance_map.get(dmg.name) == r.name:
                        dmg_value = dmg.value - r.value
                        if dmg_value < 0:
                            dmg_value = 0
                        battle_log.add("%s's armor [%s] resisted damage by: %d -> %d" % (self.owner.name, self.name, dmg.value, dmg_value))
                        dmg.value = dmg_value
            self.cur_value -= 1  # armor will be damaged after each "resist"
            battle_log.add("%s's armor [%s] condition decreased to: %d" % (self.owner.name, self.name, self.cur_value))
        return damage
    

class LeatherArmor(Armor):
    name = 'leather'
    weight = 5

    def __init__(self, condition=50):
        super().__init__(condition, MixedResistance([
            SlashResistance(5),
            CrushResistance(5),
            PierceResistance(5),
        ]))


class NatureArmor(Armor):
    weight = 0
    def __init__(self, owner, resistance):
        super().__init__(0, resistance)
        self.set_owner(owner)


class Skin(NatureArmor):
    name = 'skin'
    def __init__(self, owner):
        super().__init__(owner, Resistance(0))


class Shell(NatureArmor):
    name = 'shell'
    def __init__(self, owner):
        super().__init__(owner, MixedResistance([
            SlashResistance(10),
            PierceResistance(20),
        ]))
