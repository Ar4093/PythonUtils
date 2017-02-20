from random import randint
import re

# Supported formats:
# [A]dX[.Y1[.Y2[...]]]
# A - number of dice
# X - number of sides of dice
# . - operation: allowed are + - * x /
# Y1,Y2,... - operand
# warning: doesn't respect order of operations. So +5*3 will first add 5, then multiply by 3.
# example: 4d6+3 rolls 4 dice with 6 faces each, afterwards adds 3.

# Parse a single dice roll
def randomDice(dice):
    # Format for the whole roll
    diceexp = re.compile('(?:\D+)?(\d*)d(\d+)((([\+\-\*x\/])(\d+))+)?',re.IGNORECASE)
    # Format for modifiers
    addsexp = re.compile('[\+\-\*x\/]\d+')
    m = diceexp.match(dice)
    
    # Result of rolls
    result = 0
    
    # Weird input?
    if not m:
        return 0
    # Get the number of dice to roll
    dicenum = 0
    if m.group(1) == "" or m.group(1) == None:
        dicenum = 1
    else:
        dicenum = int(m.group(1))
    
    # Get the number of faces on each dice
    facenum = int(m.group(2))
    
    # Roll the dice
    for i in range(dicenum):
        result += randint(1,facenum)
    
    # Any modifiers present? 
    if not m.group(3) == None:
        # Split them up
        n = addsexp.findall(m.group(3))
        # Modifiers
        for i in range(len(n)):
            # Value of modifier
            modval = int(n[i][1:])
            
            # Type of modifier
            if n[i][0] == '+':
                result += modval
            elif n[i][0] == '-':
                result -= modval
            elif n[i][0] in '*x':
                result *= modval
            elif n[i][0] == '/':
                result /= modval
    return result

# Parse a whole expression.
#
# Format: dice1[+dice2[+dice3[...]]]
# dice1, dice2, dice3, ...: Any valid dice format as written in the randomDice function.
#
# Returns: The total of all rolls as integer, None if there was no valid dice notation found
def dnDice(dice):
    # Pattern
    diceexp1 = re.compile('(\d*d\d+)(([\+\-\*x\/]\d+(?!d))+)?', re.IGNORECASE)
    # Total roll
    total = 0
    
    results = diceexp1.findall(dice)
    
    if len(results) == 0:
        return None
    else:
        # Total up the rolls
        for d in results:
            string = ""
            # Discard the last part of the matched expression, it's a weird duplicate, join the rest together (the modifiers get split off)
            for part in dice:
                string += part
            
            total += randomDice(string)
        return total
