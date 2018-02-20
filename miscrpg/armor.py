from resistance import Resistance, SlashResistance, CrushResistance, PierceResistance, MixedResistance
from damageable import Damageable, Damage, MixedDamage, SlashingDamage, CrushingDamage, PiercingDamage
from rpg_logs import battle_log


damage_resistance_map = {
    SlashingDamage.name: SlashResistance,
    CrushingDamage.name: CrushResistance,
    PiercingDamage.name: PierceResistance,
    Damage.name: CrushResistance  # unknown damage defaults crushing, mostly not used
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
                assert dmg.name and dmg.name != 'unknown', '%s: damage name must be known' % self.__class__.__name__
                resist = damage_resistance_map.get(dmg.name)
                assert resist is not None, '%s: damage resistance relation must exists' % self.__class__.__name__
                dmg_value = dmg.value - resist.value
                battle_log.add('damage resisted by [%s]: %d -> %d' % (self.__class__.__name__, dmg.value, dmg_value))
                dmg.value = dmg_value
            self.cur_value -= 1  # armor will be damaged after each "resist"
            battle_log.add('armor [%s] condition decreased to: %d' % self.cur_value)
        return damage
    

class LeatherArmor(Armor):
    def __init__(self, condition=50):
        super().__init__(condition, MixedResistance([
            SlashResistance(5),
            CrushResistance(5),
            PierceResistance(5),
        ]))


class NatureArmor(Armor):
    pass
    #TODO: nature armor will restore its condition per turn


class Skin(NatureArmor):
    def __init__(self, condition=0):
        super().__init__(condition, Resistance(0))


class Shell(NatureArmor):
    def __init__(self, condition=30):
        super().__init__(condition, MixedResistance([
            SlashResistance(10),
            PierceResistance(20),
        ]))
