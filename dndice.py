from random import randint
import re

# Supported formats:
# [A]dX[(L|H|K)n][.Y1[.Y2[...]]]
# A - number of dice
# X - number of sides of dice
# . - operation: allowed are + - * x /
# Ln/Hn/Kn - discard the Lowest n dice or Keep the Highest n dice. - will only apply the first of these, in order LHK
# Y1,Y2,... - operand
# warning: doesn't respect order of operations. So +5*3 will first add 5, then multiply by 3.
# example: 4d6+3 rolls 4 dice with 6 faces each, afterwards adds 3.

HELP = '''Usage: (`<arg>`: required, `[arg]`: optional, `arg1|arg2`: either arg1 or arg2):
`\\*sidedroll <expr1>[+<expr2>[+<expr3>[...]]]`
with `expr1`, `expr2` etc. being of the following format 
```[N]d<F>[<L|H|K><n>][<Y1>[<Y2>[...]]]```
with:
`N` - number of dice to be rolled (if omitted, assumed to be 1)
`F` - number of faces of each dice
`Ln`|`Hn`|`Kn`: discard the **L**owest *n* dice or **K**eep the **H**ighest *n* dice
`Y1`, `Y2` etc. - operations to apply to this roll, supported: + - \\* x / (add, subtract, multiply, multiply, divide) followed by a number.
These are parsed in order (no proper order of operations)

Examples:
`d6+3` - rolls one dice with 6 sides and adds 3 to the roll
`4d20\\*5+4` - rolls 4 20-sided dice, multiplies the result by 5 and adds 4
`2d6+3d10` - rolls 2 6-sided and 3 10-sided dice
`5d6k3` - rolls 5 6-sided dice and only keeps the 3 highest. Equivalent to `5d6l2` and `5d6h3`'''

# Parse a single dice roll
def randomDice(dice):
    # Format for the whole roll
    diceexp = re.compile('(?:\D+)?(\d*)d(\d+)((([\+\-\*x\/LH])(\d+))+)?',re.IGNORECASE)
    # Format for modifiers
    addsexp = re.compile('[\+\-\*x\/LH]\d+',re.IGNORECASE)
    numexp = re.compile('(\d+)')
    m = diceexp.match(dice)
    
    # Result of rolls
    result = 0
    rolls = []
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
        rolls.append(randint(1,facenum))
        # result += randint(1,facenum)
    
    # sort the rolls for further processing
    
    rolls.sort()
    if 'l' in dice.lower():
        index = dice.lower().find('l') + 1
        number = int(numexp.match(dice[index:]).group())
        
        # Can't drop more dice than available, drop all of them
        if number > dicenum:
            return 0
        
        
        for i in range(number,len(rolls)):
            result += rolls[i]
    elif 'h' in dice.lower():
        index = dice.lower().find('h') + 1
        number = int(numexp.match(dice[index:]).group())
        
        # Can't keep more dice than available, keeping all of them
        if number > dicenum:
            number = dicenum
        for i in range(len(rolls)-number,len(rolls)):
            result += rolls[i]
    elif 'k' in dice.lower():
        index = dice.lower().find('k') + 1
        number = int(numexp.match(dice[index:]).group())
        
        # Can't keep more dice than available, keeping all of them
        if number > dicenum:
            number = dicenum
        for i in range(len(rolls)-number,len(rolls)):
            result += rolls[i]
    else:
        for i in range(len(rolls)):
            result += rolls[i]
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
    # Help requested?
    if dice.lower() == "help" or '?' in dice:
        return HELP
    
    # Pattern
    diceexp1 = re.compile('(\d*d\d+)(([\+\-\*x\/HLK]\d+(?!d))+)?', re.IGNORECASE)
    # Total roll
    total = 0
    
    results = diceexp1.findall(dice)
    
    if len(results) == 0:
        return "There has been an error parsing the notation. Pass help as argument to see the usage."
    else:
        # Total up the rolls
        for d in results:
            string = ""
            # Discard the last part of the matched expression, it's a weird duplicate, join the rest together (the modifiers get split off)
            for part in dice:
                string += part
            
            total += randomDice(string)
        return str(total)
