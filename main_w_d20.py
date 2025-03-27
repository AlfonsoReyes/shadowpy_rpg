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