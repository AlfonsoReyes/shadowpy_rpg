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

class MenuOption():
    def __init__(self, name, selected):
        self.name =     name
        self.selected = selected
        self.backgroundColor = Back.BLACK

    def getRenderString(self):
        optionText = ''

        if self.selected:
            self.backgroundColor = Back.LIGHTCYAN_EX
        else:
            self.backgroundColor = Back.BLACK

        return (self.backgroundColor + f"<{self.name}>" + Style.RESET_ALL)

class MainMenu():
    def __init__(self):
        self.options = [MenuOption('Start Game', selected=True), MenuOption('Exit Game', selected=False)]     
        self.focusIndex = 0
        pass

    def render(self):
        
        cursorX = 0
        cursorY = 0
        
        for option in self.options:
            Cursor.move(cursorX, cursorY)
            print(option.getRenderString())
            cursorY -= 1

    #Going up is moving down in the len List, approaching zero
    def onUp(self):
        if self.focusIndex == (len(self.options)-1):
            pass
        else:
            self.focusIndex += 1

    def onDown(self):
        if self.focusIndex == 0:
            pass
        else:
            self.focusIndex -= 1

    def getSelectedOption(self):
        """Returns menu option as currently focused"""
        return self.options[self.focusIndex]
        