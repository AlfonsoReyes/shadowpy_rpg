from gameGlobals import *


class Item():

    def __init__(self, weight, name, baseCost, equipSlots = None,  isConsumable=False, isStackable=False, quantity=1, stackMaxSize=1):
        
        self.weight =       weight
        self.name =         name 
        self.baseCost =     baseCost
        self.isConsumable = isConsumable
        self.isStackable =  isStackable
        self.quantity =     quantity
        self.stackMaxSize = stackMaxSize
        self.equipSlots =   equipSlots

class BodyArmor(Item):

    def __init__(self, weight, name, baseCost, isEquippable, armorType, metalType, quality, isEquipped, isConsumable=False, isStackable=False, quantity=1, stackMaxSize=1):
        super().__init__(weight, name, baseCost, isEquippable, isConsumable, isStackable, quantity, stackMaxSize)

        self.armorTpe =             armorType
        self.armorProperties =      ARMOR_DICT[armorType]
        self.baseCost =             ARMOR_DICT[armorType]['cost']
        self.equipType =            ARMOR_DICT[armorType]['equipType']
        self.metalType =            metalType
        self.metalProperties =      METAL_DICT[metalType]
        self.quality =              quality
        self.qualityProperties =    QUALITY_DICT[quality]
        self.isEquipped =           isEquipped
        self.isEquippable =         isEquippable
        self.flatArmorClass =       0
        self.maxDexBonus =          0

        self.refreshArmorBonuses()

    def refreshArmorBonuses(self):
        self.flatArmorClass = self.armorProperties['armorClass'] + self.metalProperties['armorClassBonus'] + self.qualityProperties['armorClassBonus']
        self.maxDexBonus = self.armorProperties['maxDexBonus']

class Weapon(Item):

    def __init__(self, weight, name, baseCost, isEquippable, isEquipped, quality, weaponType, boon, bane, metalType, isConsumable=False, isStackable=False, quantity=1, stackMaxSize=1):
        super().__init__(weight, name, baseCost, isEquippable, isConsumable, isStackable, quantity, stackMaxSize)
        
        self.weaponType =           weaponType
        self.weaponProperties =     WEAPON_DICT[weaponType]
        self.baseCost =             WEAPON_DICT[weaponType]['cost']
        self.equipType =            WEAPON_DICT[weaponType]['equipType']
        self.metalType =            metalType
        self.metalProperties =      METAL_DICT[metalType]
        self.quality =              quality
        self.qualityProperties =    QUALITY_DICT[quality]
        self.baseAttackBonus =      0
        self.baseDamageBonus =      0
        self.isEquipped =           isEquipped
        self.isEquippable =         isEquippable
        self.boon =                 boon
        self.bane =                 bane
        
        self.refreshWeaponBonuses()

    def refreshWeaponBonuses(self):
        
        self.baseAttackBonus = self.metalProperties['attackBonus'] + self.qualityProperties['attackBonus']
        self.baseDamageBonus = self.metalProperties['damageBonus'] + self.qualityProperties['damageBonus']
        
        pass