
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