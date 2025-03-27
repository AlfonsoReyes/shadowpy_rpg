
class Actor:

    def __init__(self, id, hp, moveSpeed, losRange, coords):

        self.id =           id
        self.hp =           hp
        self.moveSpeed =    moveSpeed
        self.losRange =     losRange
        self.coords =       coords

    def tellLocation(self):

        print(f"My location is {self.coords}!")

    def move(self, direction, gridSize=16):

        x = self.coords[0]
        y = self.coords[1]

        if direction == DIRECTIONS.UP:
            newCoords = (x-1, y)
        elif direction == DIRECTIONS.DOWN:
            newCoords = (x+1, y)
        elif direction == DIRECTIONS.LEFT:
            newCoords = (x, y-1)
        elif direction == DIRECTIONS.RIGHT:
            newCoords = (x, y+1)

        #collision check goes here
        newX = newCoords[0]
        newY = newCoords[1]

        if newX >= 0 and newX < gridSize and newY >= 0 and newY < gridSize:
            self.coords = newCoords

    def __str__(self):
        output = ""
        output += f"id: {self.id}\n"
        output += f"coords: {self.coords}\n"
        output += f"hp: {self.hp}\n"
        output += f"moveSpeed: {self.moveSpeed}\n"
        output += f"losRange: {self.losRange}\n"

        return output
    
class Player(Actor):

    # def __init__(self, id, hp, moveSpeed, losRange, coords, name, inventory=[]):

    def __init__(self, id, hp, moveSpeed, losRange, coords, armorClass, name, inventory, equipped, strength, dexterity, constitution, wisdom, intelligence, charisma, spellList, spellCaster=False):
        super().__init__(id, hp, moveSpeed, losRange, coords)

        self.name =         name
        self.inventory =    inventory
        self.equipped =     equipped
        self.strength =     strength
        self.dexterity =    dexterity
        self.constitution = constitution
        self.wisdom =       wisdom
        self.intelligence = intelligence
        self.charisma =     charisma
        self.spellCaster =  spellCaster
        self.spellList =    spellList
        self.maximumInventorySize = self.maximumInventory()
        self.armorClass =   self.getArmorClass()

    def maximumInventory(self):
        maxInventory = max(self.strength, 10)
        return maxInventory

    def getArmorClass(self):
        armorClass = 0
        dexBonus = self.getDexterityBonus()
        equippedArmor = self.equipped[EQUIP_SLOTS.BODYARMOR]

        if equippedArmor is None:
            armorClass = 10 + dexBonus
            return armorClass
                
        armorClass = equippedArmor.flatArmorClass + (min(dexBonus, equippedArmor.maxDexBonus))
        return armorClass

    def equip(self, targetItem):    
        """Prevalidation for the item being able to equip to the targetEquipSlot is presumed true.
        This is based on canEquip function returning a true or not.
            
        Create a function to refresh the characters bonus' from new equipped item status"""
        match targetItem.equipType:
            case EQUIP_TYPE.ONE_HANDED:
                if self.equipped[EQUIP_SLOTS.MAINHAND ] == None:
                    self.equipped[EQUIP_SLOTS.MAINHAND] = targetItem
                    targetItem.equipped = True

                elif self.equipped[EQUIP_SLOTS.OFFHAND] == None:
                    self.equipped[EQUIP_SLOTS.OFFHAND ] = targetItem
                    targetItem.equipped = True

            case EQUIP_TYPE.MAIN_HANDED:
                if self.equipped[EQUIP_SLOTS.MAINHAND ] == None:
                    self.equipped[EQUIP_SLOTS.MAINHAND] = targetItem
                    targetItem.equipped = True

            case EQUIP_TYPE.TWO_HANDED:
                if (self.equipped[EQUIP_SLOTS.MAINHAND ] == None) and (self.equipped[EQUIP_SLOTS.OFFHAND] == None):
                    self.equipped[EQUIP_SLOTS.MAINDHAND] = targetItem
                    self.equipped[EQUIP_SLOTS.OFFHAND  ] = targetItem 
                    targetItem.equipped = True

            case EQUIP_TYPE.BODY_ARMOR:
                if self.equipped[EQUIP_SLOTS.BODYARMOR ] == None:
                    self.equipped[EQUIP_SLOTS.BODYARMOR] = targetItem
                    self.armorClass = self.getArmorClass()
                    targetItem.equipped = True

    def canEquip(self, targetItem):
        #Matches targetItem equipType to the different player EquipSlots that they would/could fill
        match targetItem.equipType:
            case EQUIP_TYPE.ONE_HANDED:
                return (self.equipped[EQUIP_SLOTS.MAINHAND] == None) or (self.equipped[EQUIP_SLOTS.OFFHAND] == None)
            case EQUIP_TYPE.MAIN_HANDED:
                return self.equipped[EQUIP_SLOTS.MAINHAND] == None
            case EQUIP_TYPE.TWO_HANDED:
                return (self.equipped[EQUIP_SLOTS.MAINHAND] == None) and (self.equipped[EQUIP_SLOTS.OFFHAND] == None)
            case EQUIP_TYPE.BODY_ARMOR:
                return self.equipped[EQUIP_SLOTS.BODYARMOR] == None
        return False

    #Set of helper functions to collect players stat bonus'
    def getStrengthBonus(self):
        StrengthBonus = math.floor((self.strength-10)/2)
        return StrengthBonus
    def getDexterityBonus(self):
        dexterityBonus = math.floor((self.dexterity-10)/2)
        return dexterityBonus
    def getConstitutionBonus(self):
        constititionBonus = math.floor((self.constitution-10)/2)
        return constititionBonus
    def getWisdomBonus(self):
        wisdomBonus = math.floor((self.wisdom-10)/2)
        return wisdomBonus
    def getIntelligenceBonus(self):
        intelligenceBonus = math.floor((self.intelligence-10)/2)
        return intelligenceBonus
    def getCharismaBonus(self):
        charismaBonus = math.floor((self.charisma-10)/2)
        return charismaBonus
    #Set of helper functions to collect players stat bonus'
    
    def attack(self, targetActor, rollType):
        attackersAttackBonus = 0
        isHit = False
        isCrit = False
        damage = 0

        #Grab defending monsters AC and store it as defenersArmorClass value
        defendersArmorClass = targetActor.armorClass
        #Determine equipped weapons
        mainHandWeapon = self.equipped[EQUIP_SLOTS.MAINHAND]
        offHandWeapon  = self.equipped[EQUIP_SLOTS.OFFHAND ]
        twoHanded = False
        weaponDieOne, weaponDieTwo = mainHandWeapon.weaponProperties['weaponDie']
        #Determine if using a two handed weapon
        if mainHandWeapon == offHandWeapon:
            twoHanded = True
        #Grab characters STR bonus
        strBonus = self.getStrengthBonus()
        #Add all of weapons attack bonus' to the attack
        attackersAttackBonus += mainHandWeapon.baseAttackBonus

        #If the mainhand weapon contains the finesse property, we comapre dex and str bonus' and use the larger of the two for the attack
        if mainHandWeapon is not None:
            if WEAPON_ATTRIBUTE.FINESSE in mainHandWeapon.weaponProperties['weaponAttributes']:
                dexBonus = self.getDexterityBonus()
                attackersAttackBonus += max(dexBonus, strBonus)
            #elif WEAPON_ATTRIBUTE.RANGED in mainHandWeapon.weaponProperties['weaponAttributes']:
                # attackersAttackBonus += dexBonus
            else:
                attackersAttackBonus += strBonus

        #Rolling for attack determined by whether attack has advantage, disadvantage or neither
        if rollType == ROLL_TYPE.NORMAL:
            attackSum, attackOutcomes = Dice.roll(1,20)
        elif rollType == ROLL_TYPE.ADVANTAGE:
            attackSum, attackOutcomes = Dice.rollAdvantage(1,20)
        elif rollType == ROLL_TYPE.DISADVANTAGE:
            attackSum, attackOutcomes = Dice.rollDisadvantage(1,20)
        #Check for critical hit
        for eachDie in attackOutcomes:
            isCrit = eachDie[2]
            if isCrit:
                break

        attackSum += attackersAttackBonus
    
        #Auto land attack, else compare attack attackSum against defenders AC to determine if attack lands
        if isCrit:
            isHit = True
            if WEAPON_ATTRIBUTE.VERSATILE in mainHandWeapon.weaponProperties['weaponAttributes']:
                damage, damageOutcomes = Dice.roll(2, weaponDieTwo)
            else:
                damage, damageOutcomes = Dice.roll(2, weaponDieOne)
        elif attackSum >= defendersArmorClass:
            isHit = True
            if WEAPON_ATTRIBUTE.VERSATILE in mainHandWeapon.weaponProperties['weaponAttributes']:
                damage, damageOutcomes = Dice.roll(2, weaponDieTwo)
            damage, damageOutcomes = Dice.roll(1, weaponDieOne)

        damage += mainHandWeapon.baseDamageBonus
        # damageType = mainHandWeapon.weaponProperties['damageType']

        targetActor.hp -= damage

    def talk(self):
        
        print(f"Hello World! My name is {self.name}!")
    
    #when we call something like print(player)
    def __str__(self):

        output = super().__str__()
        output += f"name: {self.name}\n"

        return output

class Monster(Actor): 

    def __init__(self, id, hp, moveSpeed, losRange, coords, armorClass):
        super().__init__(id, hp, moveSpeed, losRange, coords)

        self.armorClass = armorClass

    def talk(self):
        
        print(f"Rawr. I'm monster {self.id}")