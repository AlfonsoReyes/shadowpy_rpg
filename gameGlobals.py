from enum import Enum

class MAX_DEX_BONUS(Enum):
    MAXANY = 4
    MAXTHREE = 3
    MAXTWO = 2
    MAXZERO = 0

class EQUIP_SLOTS(Enum):
    MAINHAND = 1
    OFFHAND = 2
    BODYARMOR = 3
    RINGSLOT1 = 4
    RINGSLOT2 = 5
    GLOVES = 6
    WAIST = 7
    HELMET = 8
    BACK = 9
    BOOTS = 10
    NECK = 11

class COMBAT_RANGE(Enum):
    CLOSE = 1
    NEAR = 2
    FAR = 3

class DAMAGE_TYPE(Enum):
    SLASHING = 1
    BLUDGEONING = 2
    PIERCING = 3
    COLD = 4
    FIRE = 5
    LIGHTNING = 6
    POISON = 7
    PURE = 8

class QUALITY(Enum):
    POOR = 1
    NORMAL = 2
    UNCOMMON = 3
    RARE = 4
    EPIC = 5
    LEGENDARY = 6

class METAL_TYPE(Enum):
    FABRIC = 1
    STEEL = 2
    MYTHRAL = 3
    ADAMANTINE = 4
    STARSTEEL = 5
    EVLEDREEM = 6
    ARGENTUM = 7
    VOLCANITE = 8

class EQUIP_TYPE(Enum):
    ONE_HANDED = 1
    MAIN_HANDED = 2
    TWO_HANDED = 3
    BODY_ARMOR = 4

class WEAPON_TYPE(Enum):
    BASTARDSWORD = 1
    CLUB = 2
    CROSSBOW = 3
    DAGGER  = 4
    GREATAXE = 5
    GREATSWORD = 6
    JAVELIN = 7
    LONGBOW = 8
    LONGSWORD = 9
    MACE = 10
    SHORTBOW = 11
    SHORTSWORD = 12
    SPEAR = 13
    STAFF = 14
    WARHAMMER = 15

class WEAPON_ATTRIBUTE(Enum):
    FINESSE = 1
    LETHAL = 2
    TWOHANDED = 3
    QUICKDRAW = 4
    VERSATILE = 5
    LOADING = 6
    THROWN = 7
    HEAVY = 8
    REACH = 9

class WEAPON_DICE(Enum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12

class DIRECTIONS(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class ROLL_TYPE(Enum):
    NORMAL = 1
    ADVANTAGE = 2
    DISADVANTAGE = 3

class BODY_ARMOR_TYPE(Enum):
    """Rogues can wear up to brigadine, priest and fighter can any armor, wizards can wear clotharmor (Functions as no AC)"""
    CLOTHARMOR = 1 #10AC + DEX 
    LEATHER = 2 #11AC + DEX 
    BRIGANDINE = 3 #12AC + DEX 
    CHAINMAIL = 4 #14AC + Dex (CAP 2?) -1DMG, 2 Weight
    BANDEDMAIL = 5 #Flat 14AC, -1DMG, 2 Weight
    FULLPLATE = 6 #FLAT 16AC, -2DMG, 3 Weight

class ANCESTRY(Enum):
    HALFDWARF = 1
    HALFELF = 2
    HALFORC = 3
    HUMAN = 4
    LIZARDMAN = 5
    LEGALLY_DISTINCT_KHAJIT = 6

class DIRECTIONS(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class ROLL_TYPE(Enum):
    NORMAL = 1
    ADVANTAGE = 2
    DISADVANTAGE = 3

QUALITY_DICT = {
    QUALITY.POOR: {
        'attackBonus': 0,
        'damageBonus': 0,
        'sellModifier': 0.4,
        'buyModifier': 0.9,
        'impressionBonus': -1,
        'weaponShatterChance': 0.05,
        'armorClassBonus': 0,
        'armorBreakModifier': 0.7,
    },
    QUALITY.NORMAL: {
        'attackBonus': 0,
        'damageBonus': 0,
        'sellModifier': 0.9,
        'buyModifier': 1.0,
        'impressionBonus': 0,
        'shatterChance': 0.025,
        'armorClassBonus': 0,
        'armorBreakModifier': 1.0,
    },
    QUALITY.UNCOMMON: {
        'attackBonus': 1,
        'damageBonus': 1,
        'sellModifier': 1.1,
        'buyModifier': 1.4,
        'impressionBonus': 1,
        'shatterChance': 0.01,
        'armorClassBonus': 1,
        'armorBreakModifier': 1.3,
    },
    QUALITY.RARE: {
        'attackBonus': 2,
        'damageBonus': 2,
        'sellModifier': 1.5,
        'buyModifier': 2.1,
        'impressionBonus': 2,
        'shatterChance': 0.005,
        'armorClassBonus': 1,
        'armorBreakModifier': 1.7,
    },
    QUALITY.EPIC: {
        'attackBonus': 3,
        'damageBonus': 3,
        'sellModifier': 2.0,
        'buyModifier': 2.9,
        'impressionBonus': 4,
        'shatterChance': 0.001,
        'armorClassBonus': 2,
        'armorBreakModifier': 2.2,
    },
    QUALITY.LEGENDARY:{
        'attackBonus': 4,
        'damageBonus': 4,
        'sellModifier': 3.4,
        'buyModifier': 5.0,
        'impressionBonus': 8,
        'shatterChance': 0,
        'armorClassBonus': 3,
        'armorBreakModifier': 3,
    }
}

METAL_DICT = {
    METAL_TYPE.FABRIC:{ # Base tier 1 metal
        'attackBonus': 0,
        'damageBonus': 0,
        'sellModifier': 0.85,
        'buyModifier': 1.0,
        'impressionBonus': 0,
        'shatterModifier': 1.0,
        'armorClassBonus': 0,
        'armorBreakThreshold': 8,
        'weightBonus': 0,
    },
    METAL_TYPE.STEEL:{ # Base tier 1 metal
        'attackBonus': 0,
        'damageBonus': 0,
        'sellModifier': 0.85,
        'buyModifier': 1.0,
        'impressionBonus': 0,
        'shatterModifier': 1.0,
        'armorClassBonus': 0,
        'armorBreakThreshold': 8,
        'weightBonus': 0,
    },
    METAL_TYPE.MYTHRAL:{ # Tier 2 Metal Light-weight armor
        'attackBonus': 1,
        'damageBonus': 1,
        'sellModifier': 1.2,
        'buyModifier': 1.5,
        'impressionBonus': 2,
        'shatterModifier': 0.8,
        'armorClassBonus': 0,
        'armorBreakThreshold': 10,
        'weightBonus': -1,
    },
    METAL_TYPE.ADAMANTINE:{ # Tier 2 Metal Execptionnaly dense armor
        'attackBonus': 1,
        'damageBonus': 2,
        'SsellModifier': 1.4,
        'buyModifier': 1.7,
        'impressionBonus': 1,
        'shatterModifier': 0.6,
        'armorClassBonus': 1,
        'armorBreakThreshold': 14,
        'weightBonus': 1,
    },
    METAL_TYPE.STARSTEEL:{ # Tier 3 Metal
        'attackBonus': 2,
        'damageBonus': 4,
        'sellModifier': 1.7,
        'buyModifier': 2.0,
        'impressionBonus': 2,
        'shatterModifier': 0.3,
        'armorClassBonus': 2,
        'armorBreakThreshold': 18,
        'weightBonus': 1,
    },
    METAL_TYPE.EVLEDREEM:{ # Tier 4 Metal - Ancient forgotten elven metal, beautifully crafted with jewels to improve the magics enchanted onto it
        'attackBonus': 3,
        'damageBonus': 3,
        'sellModifier': 2.6,
        'buyModifier': 3.5,
        'impressionBonus': 7,
        'shatterModifier': 0,
        'armorClassBonus': 2,
        'armorBreakThreshold': 20,
        'weightBonus': -1,
    },
    METAL_TYPE.ARGENTUM:{ # Tier 3 Metal - A silver, Mythral and Adamantine based alloy
        'attackBonus': 2,
        'damageBonus': 2,
        'sellModifier': 1.6,
        'buyModifier': 2.0,
        'impressionBonus': 4,
        'shatterModifier': 0.55,
        'armorClassBonus': 1,
        'armorBreakThreshold': 16,
        'weightBonus': 0,
    },
    METAL_TYPE.VOLCANITE:{ # Tier 4 Metal - Forged during the Cataclysm War, Dwarven smiths created an alloy that is rumored only to melt by using heat from the earth itself. While, this metal is a deep black
                    # color, it is highly reactive to blunt force, absorbing it as heat as color changes crimson.
        'attackBonus': 3,
        'damageBonus': 5,
        'sellModifier': 2.4,
        'buyModifier': 3.4,
        'impressionBonus': 4,
        'shatterModifier': 0,
        'armorClassBonus': 3,
        'armorBreakThreshold': 24,
        'weightBonus': 2,
    }
}

WEAPON_DICT = {
    WEAPON_TYPE.BASTARDSWORD:{
        'cost': 15,
        'weaponDie': [WEAPON_DICE.D8.value, WEAPON_DICE.D10.value],
        'weaponAttributes': [WEAPON_ATTRIBUTE.VERSATILE, WEAPON_ATTRIBUTE.HEAVY],
        'damageType': DAMAGE_TYPE.SLASHING,
        'combatRange': COMBAT_RANGE.CLOSE,
        'equipType': EQUIP_TYPE.MAIN_HANDED
    },
    WEAPON_TYPE.CLUB:{
        'cost': 15,
        'weaponDie': [WEAPON_DICE.D4.value, None],
        'weaponAttributes': [],
        'damageType': DAMAGE_TYPE.BLUDGEONING,
        'combatRange': [COMBAT_RANGE.NEAR],
        'equipType': EQUIP_TYPE.MAIN_HANDED
    },
    WEAPON_TYPE.CROSSBOW:{
        'cost': 15,
        'weaponDie': [WEAPON_DICE.D8.value, None],
        'weaponAttributes': [WEAPON_ATTRIBUTE.LOADING, WEAPON_ATTRIBUTE.TWOHANDED],
        'damageType': DAMAGE_TYPE.PIERCING,
        'combatRange': [COMBAT_RANGE.FAR],
        'equipType': EQUIP_TYPE.TWO_HANDED
    },
    WEAPON_TYPE.DAGGER:{
        'cost': .5,
        'weaponDie': [WEAPON_DICE.D4.value, None],
        'weaponAttributes': [WEAPON_ATTRIBUTE.FINESSE, WEAPON_ATTRIBUTE.LETHAL, WEAPON_ATTRIBUTE.THROWN, WEAPON_ATTRIBUTE.QUICKDRAW],
        'damageType': DAMAGE_TYPE.PIERCING,
        'combatRange': [COMBAT_RANGE.CLOSE, COMBAT_RANGE.NEAR],
        'equipType': EQUIP_TYPE.ONE_HANDED
    },
    WEAPON_TYPE.GREATAXE:{
        'cost': 10,
        'weaponDie': [WEAPON_DICE.D8.value, WEAPON_DICE.D10.value],
        'weaponAttributes': [WEAPON_ATTRIBUTE.VERSATILE, WEAPON_ATTRIBUTE.TWOHANDED, WEAPON_ATTRIBUTE.HEAVY],
        'damageType': DAMAGE_TYPE.SLASHING,
        'combatRange': [COMBAT_RANGE.CLOSE],
        'equipType': EQUIP_TYPE.MAIN_HANDED
    },
    WEAPON_TYPE.GREATSWORD:{
        'cost': 12,
        'weaponDie': [WEAPON_DICE.D12.value, None],
        'weaponAttributes': [WEAPON_ATTRIBUTE.TWOHANDED, WEAPON_ATTRIBUTE.HEAVY],
        'damageType': DAMAGE_TYPE.SLASHING,
        'combatRange': [COMBAT_RANGE.CLOSE],
        'equipType': EQUIP_TYPE.TWO_HANDED
    },
    WEAPON_TYPE.JAVELIN:{
        'cost': .5,
        'weaponDie': [WEAPON_DICE.D4.value, WEAPON_DICE.D8.value],
        'weaponAttributes': [WEAPON_ATTRIBUTE.THROWN],
        'damageType': DAMAGE_TYPE.PIERCING,
        'combatRange': [COMBAT_RANGE.CLOSE, COMBAT_RANGE.NEAR],
        'equipType': EQUIP_TYPE.MAIN_HANDED
    },
    WEAPON_TYPE.LONGBOW:{
        'cost': 8,
        'weaponDie': [WEAPON_DICE.D6.value, None],
        'weaponAttributes': [WEAPON_ATTRIBUTE.TWOHANDED, WEAPON_ATTRIBUTE.LETHAL],
        'damageType': DAMAGE_TYPE.PIERCING,
        'combatRange': [COMBAT_RANGE.FAR],
        'equipType': EQUIP_TYPE.TWO_HANDED
    },
    WEAPON_TYPE.LONGSWORD:{
        'cost': 9,
        'weaponDie': [WEAPON_DICE.D8.value, None],
        'weaponAttributes': [WEAPON_ATTRIBUTE.LETHAL],
        'damageType': DAMAGE_TYPE.SLASHING,
        'combatRange': [COMBAT_RANGE.CLOSE],
        'equipType': EQUIP_TYPE.MAIN_HANDED
    },
    WEAPON_TYPE.MACE:{
        'cost': 5,
        'weaponDie': [WEAPON_DICE.D6.value, None],
        'weaponAttributes': [],
        'damageType': DAMAGE_TYPE.BLUDGEONING,
        'combatRange': [COMBAT_RANGE.CLOSE],
        'equipType': EQUIP_TYPE.MAIN_HANDED
    },
    WEAPON_TYPE.SHORTBOW:{
        'cost': 6,
        'weaponDie': [WEAPON_DICE.D4.value, None],
        'weaponAttributes': [WEAPON_ATTRIBUTE.TWOHANDED],
        'damageType': DAMAGE_TYPE.PIERCING,
        'combatRange': [COMBAT_RANGE.FAR],
        'equipType': EQUIP_TYPE.TWO_HANDED
    },
    WEAPON_TYPE.SHORTSWORD:{
        'cost': 7,
        'weaponDie': [WEAPON_DICE.D6.value, None],
        'weaponAttributes': [],
        'damageType': DAMAGE_TYPE.SLASHING,
        'combatRange': [COMBAT_RANGE.CLOSE],
        'equipType': EQUIP_TYPE.ONE_HANDED
    },
    WEAPON_TYPE.SPEAR:{
        'cost': .5,
        'weaponDie': [WEAPON_DICE.D6.value, None],
        'weaponAttributes': [WEAPON_ATTRIBUTE.THROWN],
        'damageType': DAMAGE_TYPE.PIERCING,
        'combatRange': [COMBAT_RANGE.CLOSE, COMBAT_RANGE.NEAR],
        'equipType': EQUIP_TYPE.MAIN_HANDED
    },
    WEAPON_TYPE.STAFF:{
        'cost': .5,
        'weaponDie': [WEAPON_DICE.D4.value, None],
        'weaponAttributes': [WEAPON_ATTRIBUTE.TWOHANDED],
        'damageType': DAMAGE_TYPE.BLUDGEONING,
        'combatRange': [COMBAT_RANGE.CLOSE],
        'equipType': EQUIP_TYPE.TWO_HANDED
    },
    WEAPON_TYPE.WARHAMMER:{
        'cost': 10,
        'weaponDie': [WEAPON_DICE.D10.value],
        'weaponAttributes': [WEAPON_ATTRIBUTE.TWOHANDED],
        'damageType': DAMAGE_TYPE.BLUDGEONING,
        'combatRange': [COMBAT_RANGE.CLOSE],
        'equipType': EQUIP_TYPE.TWO_HANDED
    }
}

ARMOR_DICT = {
    BODY_ARMOR_TYPE.CLOTHARMOR: {
        'cost': 1,
        'weight': 1,
        'armorClass': 10,
        'maxDexBonus': 4,
        'damageReduction': 0,
        'sneakDisadvantage': False,
        'swimDisadvantage': False,
        'strengthRequirement': 0,
        'equipType': EQUIP_TYPE.BODY_ARMOR
    },
    BODY_ARMOR_TYPE.LEATHER: {
        'cost': 1,
        'weight': 1,
        'armorClass': 11,
        'maxDexBonus': 4,
        'damageReduction': 0,
        'sneakDisadvantage': False,
        'swimDisadvantage': False,
        'strengthRequirement': 0,
        'equipType': EQUIP_TYPE.BODY_ARMOR
    },
    BODY_ARMOR_TYPE.BRIGANDINE: {
        'cost': 1,
        'weight': 1,
        'armorClass': 12,
        'maxDexBonus': 4,
        'damageReduction': 0,
        'sneakDisadvantage': False,
        'swimDisadvantage': False,
        'strengthRequirement': 0,
        'equipType': EQUIP_TYPE.BODY_ARMOR
    },
    BODY_ARMOR_TYPE.CHAINMAIL: {
        'cost': 1,
        'weight': 2,
        'armorClass': 13,
        'maxDexBonus': 3,
        'damageReduction': 1,
        'sneakDisadvantage': False,
        'swimDisadvantage': False,
        'strengthRequirement': 12,
        'equipType': EQUIP_TYPE.BODY_ARMOR
    },
    BODY_ARMOR_TYPE.BANDEDMAIL: {
        'cost': 1,
        'weight': 2,
        'armorClass': 14,
        'maxDexBonus': 2,
        'damageReduction': 1,
        'sneakDisadvantage': False,
        'swimDisadvantage': False,
        'strengthRequirement': 14,
        'equipType': EQUIP_TYPE.BODY_ARMOR
    },
    BODY_ARMOR_TYPE.FULLPLATE: {
        'cost': 1,
        'weight': 3,
        'armorClass': 16,
        'maxDexBonus': 0,
        'damageReduction': 2,
        'sneakDisadvantage': False,
        'swimDisadvantage': False,
        'strengthRequirement': 16,
        'equipType': EQUIP_TYPE.BODY_ARMOR
    }
}

DEFAULT_EQUIPPED_DICT = {
    EQUIP_SLOTS.MAINHAND: None,
    EQUIP_SLOTS.OFFHAND  : None,
    EQUIP_SLOTS.BODYARMOR: None,
    EQUIP_SLOTS.RINGSLOT1: None,
    EQUIP_SLOTS.RINGSLOT2: None,
    EQUIP_SLOTS.GLOVES   : None,
    EQUIP_SLOTS.WAIST    : None,
    EQUIP_SLOTS.HELMET   : None,
    EQUIP_SLOTS.BACK     : None,
    EQUIP_SLOTS.BOOTS    : None,
    EQUIP_SLOTS.NECK     : None
}