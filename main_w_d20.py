from enum import Enum
from colorama import init, Fore, Back, Style
from gameGlobals import *
import msvcrt
import os
import random
import math

class Util():
    """Class with static functions for general utility
    """
    
    @staticmethod
    def gen_random_coords(gridSize=16):

        x = int(random.random()*gridSize)
        y = int(random.random()*gridSize)

        return (x, y)

class Cursor():
    """Class with static functions for interfacing with console cursor"""

    @staticmethod
    def move(x, y):
        """Move the cursor to (x, y) - 1-based coordinates.
        
        Args:
            x: x refers to the console cursor's row (acts as the VERTICAL placement)
            y: y refers to the console cursor's column (acts as the HORIZONTAL placement)
        """
        #print(f'\033[{y};{x}H', end='')
        print(f'\033[{y};{x}H', end='')

    @staticmethod
    def set_background_color(r, g, b):
        """Set the background color using RGB (24-bit color)."""
        print(f'\033[48;2;{r};{g};{b}m', end='')

    @staticmethod
    def reset_colors():
        """Reset text and background colors."""
        print('\033[0m', end='')

class Dice:

    @staticmethod
    def roll(numDice, rollRange, critRangeModifier=0, rerollLow=0):
        #create variable where you will keep adding the sum of your dice rolls to

        rollSum = 0
        isMaxRoll = False
        rollOutcomes = []

        #for loop for each dice roll, where you will be rolling each dice and adding to the total sum
        for r in range(numDice):

            isCrit = False
            isMaxRoll = False
            rollValue = round(random.random() * (rollRange))+1

            #Checks if rerollLow value is greater than 0
            if rerollLow >= 0:
                #If rollValue is equal to or less than the rerollLow's value, roll the dice again and keep new result
                if rollValue <= rerollLow:
                    
                    rollValue = round(random.random() * (rollRange-1))+1

            #Checks roll value against range, if equal, isCrit becomes true and increases number of crits
            if rollValue == rollRange:
                isMaxRoll = True

            if (rollRange - critRangeModifier) <= rollValue:
                isCrit = True

            rollOutcomes.append((rollValue, isMaxRoll, isCrit))
                
            rollSum += rollValue

        return rollSum, rollOutcomes
    
    @staticmethod
    def rollAdvantage(numDice, rollRange, critRangeModifier=0, rerollLow=0):
        #Roll two sets of the determined dice and return the larger of the two rolls as rollSum and rollOutcomes
        rollSum1, rollOutcomes1 = Dice.roll(numDice, rollRange, critRangeModifier, rerollLow )
        rollSum2, rolllOutcomes2 = Dice.roll(numDice, rollRange, critRangeModifier, rerollLow)

        rollSum = max([rollSum1, rollSum2])                
        return rollSum, rollOutcomes1, rolllOutcomes2

    @staticmethod
    def rollDisadvantage(numDice, rollRange, critRangeModifier=0, rerollLow=0):
        #Roll two sets of the determined dice and return the smaller of the two rolls as rollSum and rollOutcomes
        rollSum1, rollOutcomes1 = Dice.roll(numDice, rollRange, critRangeModifier, rerollLow )
        rollSum2, rolllOutcomes2 = Dice.roll(numDice, rollRange, critRangeModifier, rerollLow)

        rollSum = min([rollSum1, rollSum2])        
        return rollSum, rollOutcomes1, rolllOutcomes2

"""playerClassProps = {
    'fighter': {
        'hpDice': 10,
        'baseStrength': 5,
        'allowedWeaponTypes': [WeaponTypes.Sword, WeaponTypes.Shield, WeaponTypes.Bow, WeaponTypes.Staff, WeaponTypes.Dagger],
        'tierSpells': {}
    },
    'wizard': {
        'hpDice': 10,
        'baseStrength': 5,
        'allowedWeaponTypes': [WeaponTypes.Staff],
        'tierSpells': {
            'tier1': [],
            'tier2': [],
            'tier3': [],
            'tier4': [],
            'tier5': []
        }
    },
    'rogue': {
        'hpDice': 10,
        'baseStrength': 5,
        'allowedWeaponTypes': [WeaponTypes.Dagger, WeaponTypes.Bow],
        'tierSpells': {}
    },
    'cleric':{
        'hpDice': 10,
        'baseStrength': 5,
        'allowedWeaponTypes': [WeaponTypes.Staff],
        'tierSpells': {
                'tier1': [],
                'tier2': [],
                'tier3': [],
                'tier4': [],
                'tier5': []
            }
    }
}"""

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
    
class Tile():
    """A Tile object will represent an individual cell in a world's grid.
        A Tile will have a background color it can be rendered as, as a boolean flag
        indicating if it can traversed by actors, and a container listing actor(s) currently standing in the tile
    """
    
    def __init__(self, coords, isPathable=True, tileColor=Back.BLUE):
        
        self.coords = coords
        self.backgroundColor = tileColor
        self.isPathable = isPathable
        self.actors = []    #list of actor(s) currently occupying the tile
        self.updated = False

    def render(self, cursorFocus=False):
        """Render individual tile.
        """

        gridX = self.coords[0]
        gridY = self.coords[1]

        cursorX = 1 + (gridX * 3)
        cursorY = 1 + gridY

        #pre-positioning for where I want to start printing from
        Cursor.move(cursorX, cursorY)

        #this is where we actually print our tile
        print(self.getRenderString(cursorFocus=cursorFocus), end='')

    def getRenderString(self, cursorFocus=False):
        """Get string that will be used for rendering the tile
        """
        
        #by default, what renders on empty tile is '*' char
        tileText = "*"
 
        #set tile's background color
        if not cursorFocus:
            
            if self.isOccupied():
                self.backgroundColor = Back.LIGHTYELLOW_EX
            else:
                self.backgroundColor = Back.LIGHTBLACK_EX
        else:
            self.backgroundColor = Back.CYAN

        #based on actors in tile, determine printer char
        #[player, player, monster, player]
        for tileActor in self.actors:

            if type(tileActor).__name__ == 'Player':
                tileText = (Fore.GREEN + "P")

            elif type(tileActor).__name__ == 'Monster':
                tileText = (Fore.RED + "M")

            elif type(tileActor).__name__ == 'Merchant':
                tileText = (Fore.YELLOW + "$")

            elif type(tileActor).__name__ == 'Boss':
                tileText = (Fore.LIGHTMAGENTA_EX + "B")

        return (self.backgroundColor + f" {tileText} " + Style.RESET_ALL)

    def isOccupied(self):
        """Returns a true or false value indicating if there are one or more actors within the tile

        Args:
            None

        Returns:
            if actors list has 0 items, then False will be returned
            if actors list has 1 or more items, then True will be returned
        """
        return len(self.actors) > 0

class World():

    def __init__(self, gridSize=20):

        self.gridSize = gridSize
        self.grid =     self.generateWorldGrid()
        #define containers where players and enemy Actor instances will be stored
        self.players =  []
        self.enemies =  []

    def generateWorldGrid(self):
        """Generate 2-D matrix, where by default, each grid cell is an empty Tile."""
        
        rows = []

        #[0, 1, 2, 3, ... 19]
        #building empty 2d matrix
        for X in range(self.gridSize):
            col =  []

            #[0, 1, 2, 3, ... 19]
            for Y in range(self.gridSize):
                #(A,B) - (0,0), (0,1), (0,2), (0,3)...(0,19)
                col.append(Tile((X,Y)))
            
            rows.append(col)

        #world.grid[ 0][ 0] LEFT TOP
        #world.grid[ 0][19] LEFT BOTTOM
        #world.grid[19][ 0] RIGHT TOP
        #world.grid[19][19] RIGHT BOTTOM

        return rows

    def render(self):

        for x in range(self.gridSize):

            for y in range(self.gridSize):
                
                myTile = self.grid[x][y]
                myTile.render()

        return
    
        #traverse each row in the grid
        for row in self.grid:

            #(x, row)
            #for each tile in a row, add to its printable string, 
            #   then print once all row tiles have been accounted for  
            rowStr = ""
            for tile in row:
                rowStr += tile.getRenderString()
            print(rowStr)

    def findUnoccupiedTile(self):
        """Attempts to find andd return a random empty tile by iteratively
        checking each tile in the grid until first unoccupied tile is found"""

        #ordered check on grid rows and columns
        for rowNum in range(self.gridSize):

           for rowCol in range(self.gridSize):  
                
                tileToReturn = self.grid[rowCol][rowNum]

                if not tileToReturn.isOccupied():
                    return tileToReturn
        
        return None

    def getRandomUnoccupiedTile(self):
        """Attempts to find and return a random empty Tile from the world's grid."""

        tileToReturn = None
        tileFound = False

        breakLimit = 3
        breakCount = 0

        #while loop will keep going while conditions in it are true
        #The while will keep trying to findd a random empty tile
        while not tileFound and breakCount < breakLimit:
            
            #generate random coordinates to get random tile to check
            coords = Util.gen_random_coords(gridSize=self.gridSize)
            x = coords[0]
            y = coords[1]

            tileToReturn = self.grid[x][y]

            #if unoccupied tile found, 
            if not tileToReturn.isOccupied():
                tileFound = True
                break

            #safety check to avoid being stuck in perpetual while loop
            breakCount += 1

        #if tileFound is False or tileToReturn is None:
        #    raise Exception("Unable to find empty tile in world.")

        return tileToReturn

#def render_grid_ascii(Player[] players, Monster[] monsters, int gridSize=16):
#DEPRECATED
def render_grid_ascii(players, monsters, gridSize=16):

    os.system('cls')
    #stdscr.clear()

    for gx in range(gridSize):
        
        rowStr = "\n"

        for gy in range(gridSize):

            coordsOccupied = False

            for player in players:

                if (gx, gy) == player.coords:
                    rowStr += (Back.YELLOW + Fore.GREEN + " P " + Style.RESET_ALL)
                    coordsOccupied = True
                    
            if not coordsOccupied:
                for monster in monsters:
                    if (gx, gy) == monster.coords:
                        rowStr += (Fore.RED + " M " + Style.RESET_ALL)
                        coordsOccupied = True
            
            if not coordsOccupied:
                rowStr += " * "

        print(rowStr)
#DEPRECATED
def testOld():
    occupied = []

    #create player
    playerCoords = Util.gen_random_coords()
    occupied.append(playerCoords)
    pc = Player(1, 50, 1, 5, playerCoords, "Steve")

    #make player talk
    pc.talk()

    monsters = []
    #create monsters
    #first pass:    i = 2
    #second pass:   i = 3
    #third pass:    i = 4
    for i in range(2,10,1):

        monsterCoords = Util.gen_random_coords()
        while monsterCoords in occupied:
            monsterCoords = Util.gen_random_coords()
        occupied.append(monsterCoords)

        myMonster = Monster(i, 10, 1, 2, monsterCoords)
        monsters.append(myMonster)

    #make each monster talk
    for myMonster in monsters:
        myMonster.talk()
        myMonster.tellLocation()

    os.system('cls')

    while True:
        key = msvcrt.getch()
        print(f"Key pressed: {key}!")

        if key == b'q':
            break
        if key == b'w':
            pc.move(DIRECTIONS.UP)
        if key == b's':
            pc.move(DIRECTIONS.DOWN)
        if key == b'a':
            pc.move(DIRECTIONS.LEFT)
        if key == b'd':
            pc.move(DIRECTIONS.RIGHT)

        render_grid_ascii([pc], monsters)

    print("Exited out of function!")

def getStarterEquipment():
    """generates a set of equipment for new players: ShortSword and Leather Armor with a quality of poor each"""
    items = []
    #(self, weight, name, sellValue, isEquippable, isEquipped, quality, weaponType, boon, bane, damageDiceRange, isConsumable=False, isStackable=False, quantity=1, stackMaxSize=1)
    weaponRoll = int(random.random() * (10))

    myLeatherArmor = BodyArmor(1, 'Poor Leather Armor', 0, True, BODY_ARMOR_TYPE.LEATHER, METAL_TYPE.FABRIC, QUALITY.POOR, False, any)
    myLongSword = Weapon(1, 'Poor Longsword', 0, True, False, QUALITY.POOR, WEAPON_TYPE.LONGSWORD, [], [], METAL_TYPE.STEEL)
    items.extend([myLongSword, myLeatherArmor])
    return items
 
def createWorld(gridSize, playerNum, monsterNum):
    """Generates and return a new randomly-generated world.

    Args:
        gridSize: (int) size of square grid to be generated for the world
        playerNum: (int) number of players to generate
        monsterNum: (int) number of monsters to generatte

    Returns:
        World class instance
    """
    #generate world with empty tiles
    myWorld = World(gridSize=gridSize)

    #random name list
    fantasyNames = [
        "Arannis", "Thalindra", "Gorim", "Elowen", "Kaelen",
        "Drakthar", "Sylvara", "Vorstag", "Lyra", "Zalthar",
        "Morwen", "Kelvhan", "Aelric", "Virelith", "Fenthis",
        "Bryndis", "Xalvador", "Tessara", "Korrin", "Mythra",
        "Eryndor", "Quilathe", "Threx", "Isolde", "Ravonak",
        "Altharion", "Calista", "Galdric", "Nymeria", "Zarvok",
        "Leothar", "Seraphina", "Draven", "Aeliana", "Vornak",
        "Thalor", "Ellaria", "Krynn", "Selene", "Rhovan",
        "Faelar", "Ysolde", "Varis", "Zyra", "Torhild",
        "Andareth", "Maelis", "Faylen", "Jorund", "Eldrin"
    ]

    fantasyNames[0]
    fantasyNames[20]
    
    #start id counter
    idNum = 1

    pickedNameIndexes = []

    #generate players
    #playerNum = 3
    #range(playerNum) = [0, 1, 2]
    #i is a placeholder
    for i in range(playerNum):

        #pick a random name from fantasyNames list
        #random() returns a decimal number between 0 and 1
        #len(fantasyNames) is a positive integer (let's say 50)

        #we multiply so that the range is between 0 and len(fantasyNames) (50)
        #a valid number would 42.69
        
        #the int(n) function type casts a value intto an integer
        nameIndex = int(random.random() * len(fantasyNames))

        #we're only reattmpting once if name already picked
        if nameIndex in pickedNameIndexes:
            nameIndex = int(random.random() * len(fantasyNames))      

        playerName = fantasyNames[nameIndex]

        #find random unoccupied tile in the world that we can place actor in
        unoccupiedTile = myWorld.getRandomUnoccupiedTile()    
 
        #create player instance once we've found an unoccupied tile they can be placed in
        # myPlayer = Player(self, id, hp, moveSpeed, losRange, coords, armorClass, name, inventory, equipped, strength, dexterity, constitution, wisdom, intelligence, charisma, spellList, spellCaster=False)
        equippedDic = DEFAULT_EQUIPPED_DICT
        
        starterEquipment = getStarterEquipment()

        myPlayer = Player(idNum, 8, 30, 30, unoccupiedTile.coords, 10, playerName, starterEquipment, equippedDic, 10, 10, 10, 10, 10, 10, [], False)

        for myItem in myPlayer.inventory:
            if myItem.isEquippable:
                if myPlayer.canEquip(myItem):
                    myPlayer.equip(myItem)

        #add player instance to list of world's players
        myWorld.players.append(myPlayer) 
        #add player instance to (formerly unoccupied) tile's list of actors in it
        unoccupiedTile.actors.append(myPlayer)
        #increment ID value after each Monster actor has been created
        idNum += 1

    #generate monsters
    for i in range(monsterNum):

        #find random unoccupied tile in the world that we can place actor in
        unoccupiedTile = myWorld.getRandomUnoccupiedTile()    
        #create player instance once we've found an unoccupied tile they can be placed in
        myMonster = Monster(idNum, 50, 1, 5, unoccupiedTile.coords, 12)
        #add player instance to list of world's enemies
        myWorld.enemies.append(myMonster)       
        #add player instance to (formerly unoccupied) tile's list of actors in it
        unoccupiedTile.actors.append(myMonster)
        #increment ID value after each Monster actor has been created
        idNum += 1

    return myWorld

def playerMovement():



    pass

def worldCursorTest():

    #clear screen
    os.system('cls')

    #create world
    gridSize = 20
    #playerCount = 3
    #monsterCount = 10
    myWorld = createWorld(gridSize, 3, 10)

    #render world
    myWorld.render()

    activePlayer = None

    # for player in myWorld.players:
    #     print(player)

    # return

    playerGridX = 0
    playerGridY = 0

    gridX = 0
    gridY = 0

    prevGridX = 0
    prevGridY = 0

    #reset console cursor position to top left corner
    Cursor.move(0, 0)

    while True:
        key = msvcrt.getch()
        #print(f"Key pressed: {key}!")
        
        #move cursor to below the grid
        Cursor.move(65, 1)
        print(f"Key pressed: {key}!")

        diffX = 0
        diffY = 0

        playerDiffX = 0
        playerDiffY = 0

        if key == b'r':
            #rollSum, isCrit, numCrits

            rollSum, rollOutcomes = Dice.roll(2,20)

            cursorRow = 21

            totalCrits = 0

            maxRolls = 0

            Cursor.move(65,20)
            print("            ")

            Cursor.move(65,20)
            print(rollSum)

            for eachDie in rollOutcomes:
                # (rollValue, isMaxRoll, isCrit)

                rollValue = eachDie[0]
                isMaxRoll = eachDie[1]
                isCrit = eachDie[2]
                
                if isCrit:
                    totalCrits += 1
                if isMaxRoll:
                    maxRolls += 1

                Cursor.move(65, cursorRow       )
                print("                "        )
                Cursor.move(65, cursorRow       )
                print(f"rollValue {rollValue}"  )
                cursorRow += 1

            Cursor.move(65, cursorRow       )
            print("                "        )
            Cursor.move(65, cursorRow       )
            print(f"totalcrits {totalCrits}")
            cursorRow += 1

            Cursor.move(65, cursorRow   )
            print("               "     )
            Cursor.move(65, cursorRow   )
            print(f"maxRolls {maxRolls}")
            cursorRow += 1

        if key == b'q':
            break
        if key == b'w':
            #UP Cursor
            diffY = -1
            #pc.move(DIRECTIONS.UP)
        if key == b's':
            #DOWN Cursor
            diffY = 1
            #pc.move(DIRECTIONS.DOWN)
        if key == b'a':
            #LEFT Cursor
            diffX = -1
            #pc.move(DIRECTIONS.LEFT)
        if key == b'd':
            #RIGHT Cursor
            diffX = 1
            #pc.move(DIRECTIONS.RIGHT)
        if key == b'\r':
            #ENTER
            myTile = myWorld.grid[gridX][gridY]
            #Sets active player
            for tileActor in myTile.actors:
                if type(tileActor).__name__ == 'Player':
                    activePlayer = tileActor

                    playerGridX = gridX
                    playerGridY = gridY

                    break
            # elif activePlayer is not None:
            #     activePlayer = None
        if key == b'H':
            #UP ARROW (Active Player Up)
            playerDiffY = -1
        if key == b'P':
            #DOWN ARROW (Active Player Down)
            playerDiffY = 1
        if key == b'K':
            #LEFT ARROW (Active Player Left)
            playerDiffX = -1
        if key == b'M':
            #RIGHT ARROW (Active Player Right)
            playerDiffX = 1

        myTile = None

        if gridX+diffX < gridSize and gridY+diffY < gridSize and gridX+diffX >= 0 and gridY+diffY >= 0:
            
            #store grid values BEFORE they're updated
            prevGridX = gridX
            prevGridY = gridY

            #update current selected grid values
            gridX = diffX + gridX
            gridY = diffY + gridY

            myTile = myWorld.grid[gridX][gridY]
            myTile.render(cursorFocus=True)

            #ddeterrmine if previously highlighted tile should become un-highlighted
            if prevGridX != gridX or prevGridY != gridY:
                myOldTile = myWorld.grid[prevGridX][prevGridY]
                myOldTile.render(cursorFocus=False)

        if (activePlayer is not None 
            and (playerDiffX != 0 or playerDiffY != 0)  #Have we pressed any keys that would cause player movement
            and playerGridX+playerDiffX < gridSize      #If players destination tile is within grid size
            and playerGridY+playerDiffY < gridSize      #If players destination tile is within grid size
            and playerGridX+playerDiffX >= 0            #checks player destination against lowest bound of grid
            and playerGridY+playerDiffY >= 0):          #checks player destination against lowest bound of grid

            #store grid values BEFORE they're updated
            prevPlayerGridX = playerGridX
            prevPlayerGridY = playerGridY

            #update desired player destination
            playerGridX = playerDiffX + playerGridX
            playerGridY = playerDiffY + playerGridY

            myDestinationTile = myWorld.grid[playerGridX][playerGridY]  

            if not myDestinationTile.isOccupied():

                myPrevTile = myWorld.grid[prevPlayerGridX][prevPlayerGridY]
                
                Cursor.move(65,9)
                print(f"My Prev Tile:{myPrevTile.coords}")
                Cursor.move(65,10)
                print(f"my Destination Tile: {myDestinationTile.coords}")
                Cursor.move(65,11)
                print(f"{activePlayer.name}'s Armor Class: {activePlayer.armorClass}")
                Cursor.move(65,12)
                print(f"equipped: {activePlayer.equipped[EQUIP_SLOTS.MAINHAND].name}")
                
                myPrevTile.actors.remove(activePlayer)
                myDestinationTile.actors.append(activePlayer)
                activePlayer.coords = (playerGridX, playerGridY)
                Cursor.move(65,13)
                print(f"my active player coords:{activePlayer.coords}")

                myDestinationTile.render()

            else:
                #If the tile is occupied, we must reset the positioning of active players location for further movement
                playerGridX = activePlayer.coords[0]
                playerGridY = activePlayer.coords[1]
    
            if prevPlayerGridX != playerGridX or prevPlayerGridY != playerGridY:
                myPrevTile.render()

            #myTile.render(cursorFocus=True)

            #deterrmine if previously highlighted tile should become un-highlighted
            if prevGridX != gridX or prevGridY != gridY:
                myOldTile = myWorld.grid[prevGridX][prevGridY]
                myOldTile.render(cursorFocus=False)

        if key == b'v':
            if activePlayer is not None:
                myTile = myWorld.grid[gridX][gridY]
                #Define attack target
                for tileActor in myTile.actors:
                    if type(tileActor).__name__ == 'Monster':
                        adjacentTiles = getAdjacentTiles(myWorld, gridX, gridY)
                        if activePlayer.coords in adjacentTiles:
                            activePlayer.attack(tileActor, ROLL_TYPE.NORMAL)

        #move cursor to below the grid
        Cursor.move(65, 2)
        print(f"Grid Coords: ({gridX},{gridY})")
        
        if myTile is not None:
            Cursor.move(65, 3)
            print(f"Tile Coords: ({myTile.coords})")

        renderOverlay(myWorld, myTile)

    print("Breaking out of while loop!")

def getAdjacentTiles(myworld, gridX, gridY):
    rows, cols = len(myworld.grid), len(myworld.grid)
    adjacentTiles = []
    #Define the search area in X,Y
    moves = [(-1,0), (1,0), (0,-1), (0,1), (1,1), (-1,1), (1,-1),(-1,-1)]
    
    for dc, dr in moves:
        newGridX, newGridY = gridX + dc, gridY + dr

        if  0 <= newGridX < rows and 0 <= newGridY < cols:
            adjacentTiles.append((newGridX, newGridY))

    return adjacentTiles

def renderOverlay(myWorld, currentlySelectedTile):

    #we set our cursor to the right of the grid
    cursorRow = 4
    cursorCol = 65

    #resetting 19 lines to empty whitespace for overlay
    for i in range(3,10,1):
        Cursor.move(cursorCol, i)
        print("                                     ")

    if currentlySelectedTile is None:
        return

    #if tile has any actors in it, print their data
    for tileActor in currentlySelectedTile.actors:
        
        if type(tileActor).__name__ == 'Player':
            Cursor.move(cursorCol, cursorRow)
            print(f"Name: {tileActor.name}")
            cursorRow += 1
        
        Cursor.move(cursorCol, cursorRow)
        print(f"ID: {tileActor.id}")
        cursorRow += 1

        Cursor.move(cursorCol, cursorRow)
        print(f"Coords: {tileActor.coords}")
        cursorRow += 1

        Cursor.move(cursorCol, cursorRow)
        print(f"HP: {tileActor.hp}")
        cursorRow += 1

        Cursor.move(cursorCol, cursorRow)
        print(f"losRange: {tileActor.losRange}")
        cursorRow += 1

        # Cursor.move(cursorCol, cursorRow)
        # print(f"moveSpeed: {tileActor.moveSpeed}")
        # cursorRow += 1

        Cursor.move(cursorCol, cursorRow)
        print(f"armorClass: {tileActor.armorClass}")
        cursorRow += 1


def main():

    worldCursorTest()

main()