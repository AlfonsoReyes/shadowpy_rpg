from colorama import init, Fore, Back, Style
from gameGlobals import *
from util import Dice, Util, Cursor 

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
    
    def getAllUnoccupiedTiles(self):
        '''Returns all unoccupied tiles in the world'''
        unoccupiedTiles = []

        for rowNum in range(self.gridSize):
           for rowCol in range(self.gridSize):                  
                individualTile = self.grid[rowCol][rowNum]

                if not individualTile.isOccupied():
                    unoccupiedTiles.append(individualTile)

        return unoccupiedTiles