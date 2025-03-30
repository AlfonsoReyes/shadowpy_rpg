from enum import Enum
from colorama import init, Fore, Back, Style
from gameGlobals import *
from util import Dice, Util, Cursor 
from actor import Actor, Player, Monster
import msvcrt
import os
import random
import math
from world import World, Tile
from item import *

class Game():
    def __init__(self, worldSize = 20, playerToCreate = 1, monstersToCreate = 1):
        self.worldSize = worldSize
        self.players = []
        self.enemies = []
        self.world: World = self.createWorld()
        self.actorId = 1
        self.populateGame(playerToCreate, monstersToCreate)

    def populateGame(self, playerToCreate, monstersToCreate):
        self.createPlayers(playerToCreate)
        self.createMonsters(monstersToCreate)
        
    def createPlayers(self, numPlayers):

        pickedNameIndexes = []
        fantasyNames = FANTASY_NAMES

        #generate players
        #playerNum = 3
        #range(playerNum) = [0, 1, 2]
        #i is a placeholder
        for i in range(numPlayers):

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
            unoccupiedTile = self.world.getRandomUnoccupiedTile()    
    
            #create player instance once we've found an unoccupied tile they can be placed in
            # myPlayer = Player(self, id, hp, moveSpeed, losRange, coords, armorClass, name, inventory, equipped, strength, dexterity, constitution, wisdom, intelligence, charisma, spellList, spellCaster=False)
            equippedDic = DEFAULT_EQUIPPED_DICT
            
            starterEquipment = self.getStarterEquipment()

            myPlayer = Player(self.actorId, 8, 30, 30, unoccupiedTile.coords, 10, playerName, starterEquipment, equippedDic, 10, 10, 10, 10, 10, 10, [], False)

            #Auto-equips starter equipment for new players in Player class function
            for myItem in myPlayer.inventory:
                if myItem.isEquippable:
                    if myPlayer.canEquip(myItem):
                        myPlayer.equip(myItem)

            #add player instance to list of world's players
            self.players.append(myPlayer) 
            #add player instance to (formerly unoccupied) tile's list of actors in it
            unoccupiedTile.actors.append(myPlayer)
            #increment ID value after each Monster actor has been created
            self.actorId += 1

    def createMonsters(self, numMonsters):        
        for i in range(numMonsters):

            #find random unoccupied tile in the world that we can place actor in
            unoccupiedTile = self.world.getRandomUnoccupiedTile()
            #create player instance once we've found an unoccupied tile they can be placed in
            myMonster = Monster(self.actorId, 50, 1, 5, unoccupiedTile.coords, 12)
            #add player instance to list of world's enemies
            self.enemies.append(myMonster)       
            #add player instance to (formerly unoccupied) tile's list of actors in it
            unoccupiedTile.actors.append(myMonster)
            #increment ID value after each Monster actor has been created
            self.actorId += 1

    def createWorld(self):
        """Generates and return a new randomly-generated world.
        Returns: World class instance"""
        #generate world with empty tiles
        return World(self.worldSize)

    def run(self):

        #clear screen
        os.system('cls')

        #create world
        gridSize = 20
        #playerCount = 3
        #monsterCount = 10
        myWorld = self.world
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

            #Sends directions to active player actor for movement in game
            if activePlayer and (playerDiffX != 0 or playerDiffY != 0):
                activePlayer.handlePlayerMovement(playerDiffX, playerDiffY, self)
                    #determine if previously highlighted tile should become un-highlighted

                if prevGridX != gridX or prevGridY != gridY:
                    myOldTile = myWorld.grid[prevGridX][prevGridY]
                    myOldTile.render(cursorFocus=False)

                nearbyActors = activePlayer.getNearbyActors(self.enemies, 15)

                allPerceptionChecks = []

                for actorTuple in nearbyActors:
                    if actorTuple[0].losRange >= actorTuple[1]:
                        perceptionCheck = actorTuple[0].perceptionCheck()
                        allPerceptionChecks.append[perceptionCheck]
                    
                if len(allPerceptionChecks) > 0:
                    if activePlayer.stealthCheck() <= max(allPerceptionChecks):
                        #Enter combat nerd code
                        pass

                        """Grab list of enemies in actorTuple, grab all playerActors in matrix and add to combat
                        'tracker' list. have each actor roll for initiative. Sort actors from highest to lowest.
                        start combat loop."""
                    

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

                #determine if previously highlighted tile should become un-highlighted
                if prevGridX != gridX or prevGridY != gridY:
                    myOldTile = myWorld.grid[prevGridX][prevGridY]
                    myOldTile.render(cursorFocus=False)

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
                            adjacentTiles = self.getAdjacentTiles(myWorld, gridX, gridY)
                            if activePlayer.coords in adjacentTiles:
                                activePlayer.attack(tileActor, ROLL_TYPE.NORMAL)

            #move cursor to below the grid
            Cursor.move(65, 2)
            print(f"Grid Coords: ({gridX},{gridY})")
            
            if myTile is not None:
                Cursor.move(65, 3)
                print(f"Tile Coords: ({myTile.coords})")

            self.renderOverlay(myWorld, myTile)

    def getAdjacentTiles(self, myworld, gridX, gridY):
        rows, cols = len(myworld.grid), len(myworld.grid)
        adjacentTiles = []
        #Define the search area in X,Y
        moves = [(-1,0), (1,0), (0,-1), (0,1), (1,1), (-1,1), (1,-1),(-1,-1)]
        
        for dc, dr in moves:
            newGridX, newGridY = gridX + dc, gridY + dr

            if  0 <= newGridX < rows and 0 <= newGridY < cols:
                adjacentTiles.append((newGridX, newGridY))

        return adjacentTiles

        print("Breaking out of while loop!")

    def renderOverlay(self, myWorld, currentlySelectedTile):

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

    def getStarterEquipment(self):
        """generates a set of equipment for new players: ShortSword and Leather Armor with a quality of poor each"""
        items = []
        #(self, weight, name, sellValue, isEquippable, isEquipped, quality, weaponType, boon, bane, damageDiceRange, isConsumable=False, isStackable=False, quantity=1, stackMaxSize=1)
        weaponRoll = int(random.random() * (10))

        myLeatherArmor = BodyArmor(1, 'Poor Leather Armor', 0, True, BODY_ARMOR_TYPE.LEATHER, METAL_TYPE.FABRIC, QUALITY.POOR, False, any)
        myLongSword = Weapon(1, 'Poor Longsword', 0, True, False, QUALITY.POOR, WEAPON_TYPE.LONGSWORD, [], [], METAL_TYPE.STEEL)
        items.extend([myLongSword, myLeatherArmor])
        return items