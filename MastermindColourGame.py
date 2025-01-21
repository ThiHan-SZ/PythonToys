"""
Mastermind Game in Python

This program implements the popular Mastermind game.
The player has to guess a sequence of colors, and the computer provides feedback in the form of correct positions and correct colors.
The game continues until the player guesses the sequence correctly or runs out of attempts.
"""

# Colours
RED = "\U0001F534"
BLUE = "\U0001F535"
YELLOW = "\U0001F7E1"
GREEN = "\U0001F7E2"
PURPLE = "\U0001F7E3"
BROWN = "\U0001F7E4"
W_SQUARE = "\u25A0"
B_SQUARE = "\u25A1"

# List of colours
Colours = [RED, BLUE, YELLOW, GREEN, PURPLE, BROWN]

# Game variables
length = 0
gameseed = 0
GuessList = []

def RandomNumber(min, max):
    """
    Generates a random number between the specified minimum and maximum values using a linear congruential generator.

    Args:
        min (int): The minimum value of the desired range.
        max (int): The maximum value of the desired range.

    Returns:
        int: A pseudo-random number within the range [min, max].
    """
    global gameseed
    gameseed = (1664525 * gameseed + 1013904223) % (2**32)
    return min + (gameseed % (max - min + 1))

def CodeMakerGenerator(length, repeat_allowed = False):
    """
    Generates a random sequence of colours of the specified length, with or without repetition.

    Args:
        length (int): The length of the sequence to generate.
        repeat_allowed (bool): Whether to allow the same colour to appear more than once in the sequence. Defaults to False.

    Returns:
        str: A string of length 'length' representing the randomly generated sequence of colours.
    """
    code = []
    for i in range(length):
        choice = Colours[RandomNumber(0, len(Colours) - 1)]
        if repeat_allowed:
            code.append(choice)
        else:
            if choice not in code:
                code.append(choice)
                
    return code

def CodeMakerFeedback(code, guess):
    """
    Provides feedback on the player's guess in terms of correct positions and correct colours.

    Args:
        code (str): The target sequence of colours.
        guess (str): The player's guess.

    Returns:
        tuple: A tuple containing the number of correct positions and the number of correct colours.
    """
    correct_position = 0
    correct_colour = 0
    
    for i in range(len(code)):
        if code[i] == guess[i]:
            correct_position += 1
    
    for code_colour in set(code):
        # Count the number of times the code colour appears in the guess
        correct_colour += min(code.count(code_colour), guess.count(code_colour))
    
    # Adjust for overlap where both position and color match
    correct_colour -= correct_position
    return correct_position, correct_colour

def CodeBoard(guess, correct_position, correct_colour):
    """
    Displays the history of guesses and feedback.

    Args:
        guess (str): The player's guess.
        correct_position (int): The number of correct positions.
        correct_colour (int): The number of correct colours.
    """
    global GuessList
    GuessList.append((guess,correct_position,correct_colour))
    print(f"|{"Guess":^{len(guess)*6}}|{"Correct Position":^20}|{"Correct Colour":^20}|")
    for guess in GuessList:
        print("|", end="")
        for cell in guess[0]:
            print(f"{cell:^5}", end="") # Ensure each colour peg takes up 5 characters. ^ is used to center align the colour pegs
        print(f"|{guess[1]*W_SQUARE:^20}|{guess[2]*B_SQUARE:^20}|") # Ensure each set of square takes up 10 characters. ^ is used to center align the squares

def CodeBreakerGame():
    """
    Runs the Mastermind game where the player attempts to guess a randomly generated sequence of colors.

    The game provides an introductory message and instructions for the player. The player selects the 
    number of colors in the sequence and whether repetition of colors is allowed. The player has 10 
    attempts to guess the sequence, and feedback is provided after each guess in terms of correct 
    positions and correct colors. The game concludes when the player either guesses the sequence 
    correctly or exhausts all attempts.

    Uses:
        CodeMakerGenerator(length, repeat_allowed): Generates the target color sequence.
        CodeMakerFeedback(code, guess): Provides feedback on the player's guess.
        CodeBoard(guess, correct_position, correct_colour): Displays the history of guesses and feedback.
    """

    print("="*20)
    print("Welcome to Mastermind!")
    print("You will be given a sequence of colours and you must guess what they are.")
    print("There are 6 Colour : Red, Blue, Yellow, Green, Purple, Brown")
    print("Enter : RD, BL, YL, GN, PR, BN")
    print("You have 10 turns to guess the sequence.")
    print("Good Luck!")
    print("="*20)
    
    repititon = False
    global length
        
    attempts = 0
    max_attempts = 10
    
    while length < 4:
        # Get the length of the code
        # If length is less than 4, ask again
        # If length is greater than 6, enable repetition instead
        length = int(input("\nSelect the number of colours in the code : "))
        if length < 4:
            print("Please enter a number greater than 0")
        elif length > 6:
            print("!!! Code will contain repeat colours !!!")
            repititon = True
    
    if not repititon:
        # If repititon not already enabled
        # Allow repeat colours or not
        repititon_input = "X"
        while repititon_input not in ["Y", "N"]:
            repititon_input = input("\nDo you want to allow repeat colours? (Y/N) : ").upper()
            if repititon_input == "Y": 
                repititon = True
            elif repititon_input == "N":
                repititon = False
            else:
                print("Invalid input. Please enter Y or N.")
        
    code = CodeMakerGenerator(length, repititon)
    
    while attempts < max_attempts:
        guess = []
        ColoursAbrevDict = {"RD": RED, "BL": BLUE, "YL": YELLOW, "GN": GREEN, "PR": PURPLE, "BN": BROWN}
        print("Enter : 'RD', 'BL', 'YL', 'GN', 'PR', 'BN' or 'exit' to quit")
        for i in range(length):
            guesscell = 'X'
            while guesscell not in ColoursAbrevDict.keys():
                guesscell = input(f"Enter colour {i + 1} : ").upper()
                if guesscell == 'EXIT':
                    return 0
                elif guesscell not in ColoursAbrevDict.keys():
                    print("Invalid input. Please enter a valid colour.")
            guess.append(ColoursAbrevDict[guesscell])
        
        correct_position, correct_colour = CodeMakerFeedback(code, guess)
        if correct_position == length:
            print("Congratulations! You guessed the code in", attempts + 1, "attempts.")
            break
        else:
            print("Incorrect. You have", max_attempts - attempts - 1, "attempts left.")
            attempts += 1
        CodeBoard(guess, correct_position, correct_colour)
        
    if attempts == max_attempts:
        print("You have run out of attempts. The code was", "".join(code))
        print("Better luck next time!")
    

def play_loop():
    """
    Repeatedly plays the CodeBreakerGame until the user chooses to quit.

    Asks the user if they want to play again after each game, and if they answer 'N' (or any other input that's not 'Y'),
    the loop will terminate and the program will end with a goodbye message.

    Returns:
        None
    """

    playagain = True
    while playagain:
        CodeBreakerGame()
        playagain = input("\nDo you want to play again? (Y/N) : ").upper()
        if playagain == "N":
            playagain = False
            print("Thanks for playing!")

play_loop()
