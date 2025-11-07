import random

def Board():
    global count
    global BoardLine
    row=0
    column=0
    for row in range(7):
        BoardLine[0][row+1]=" "+str(row+1)+" "#label the rows
    for column in range(6):
        BoardLine[column+1][0]=" "+str(column+1)+" "
    for x in range(len(BoardLine)):
        print("")#change the row
        for h in range(len(BoardLine[x])):
            print(BoardLine[x][h],end = "")#Construct the Board
    print("") # To change to the next line
            
def Available_Columns():
    AvailableColumns = []
    for i in range(1,8,1):
        if NextAvailableSpace[i] != 0:
            AvailableColumns.append(i)
    return AvailableColumns

def NextStep(choice):
    global count
    global BoardLine
    if count % 2 == 0:
        BoardLine[NextAvailableSpace[choice]][choice] = " # "
        NextAvailableSpace[choice] -= 1
        count += 1

    else:
        BoardLine[NextAvailableSpace[choice]][choice] = " @ "
        NextAvailableSpace[choice] -= 1
        count += 1

def ReverseNextStep(LastChoice):
    global count
    global BoardLine
    count -= 1
    NextAvailableSpace[LastChoice] += 1
    BoardLine[NextAvailableSpace[LastChoice]][LastChoice] = "   "
        
def SelectChoice():
    while True:
        try:
            choice = int(input("Please input the column you want to make the next move:"))
        except ValueError:
            print("Please input the correct column!")
            continue
        if not 1 <= choice <= 7:
            print("This column does not exist!")
            continue
        if NextAvailableSpace[choice] == 0:
            print("This column is already full!")
            continue
        break
    return choice
def win(last_column): #Check if anyone wins 
    global count
    global BoardLine
    global mode
    global sequence
    global control
#idea: we only need the information about the column of the last step, since in connect-four, the last move is always at the top of a column.
    position = (NextAvailableSpace[last_column] + 1,last_column) #This is the current position of the last move.
    """print("Position: ", position)"""
    row = position[0]
    col = position[1]
    Current = BoardLine[row][col] # The current type of move.
    """print('Current: "',Current,'"' )"""
    directions = [[(0,1),(0,-1)],[(1,0),(-1,0)],[(1,1),(-1,-1)],[(1,-1),(-1,1)]]
    for direction in directions:
        count1 = 0
        for i in range(2): #The two tuples are on a straight line
            row = position[0]
            col = position[1]
            x = direction[i][0]
            y = direction[i][1]
            flag = True #This indicates whether the positions belong to the same person
            while flag == True:
                try:
                    row += x
                    col += y
                    if BoardLine[row][col] == Current:
                        count1 += 1
                    else:
                        flag = False
                except IndexError:
                    flag = False
        if count1 >= 3:
            control = 1


def RandomComputer():
    Available_Columns()
    choice = random.randint(1,len(Available_Columns()))
    return choice
def MoreAdvancedComputer(): #This computer will avoid the immediate step that will end the game, and tends to fall in the middle three columns since there tends to be more chance to win.
    global count
    global Sequence
    global control
    ChoiceList = Available_Columns()
    Weight = [0 for i in range(len(ChoiceList))]
    for i in ChoiceList:
        NextStep(i)
        win(i)
        if control == 1:#The computer will win directly
            ReverseNextStep(i)
            control = 0
            return i
        else:
            ReverseNextStep(i)
    count += 1 # Assume the next step belongs to the player            
    for i in range(len(ChoiceList)):        
        if ChoiceList[i] == 1 or ChoiceList[i] == 7:
            Weight[i] = 4
        elif ChoiceList[i] == 2 or ChoiceList[i] == 6:
            Weight[i] = 6
        else:
            Weight[i] = 7         
    for col in ChoiceList:# To check if the player have any route that directly leads to win.
        NextStep(col)
        win(col)
        if control == 1: # The player will win at this step after falling at this place. The computer will resist this.
            count -= 1
            ReverseNextStep(col)
            control = 0
            return col
        else:
            ReverseNextStep(col)
    count -= 1 #reverse

    
    for col in ChoiceList:# To check if after this move,the player have any route that directly leads to win.

        NextStep(col)
        for PossibleChoice in [max(col-1,1),col,min(col+1,7)]:
            if NextAvailableSpace[PossibleChoice] == 0: #Full
                continue
            NextStep(PossibleChoice)
            win(PossibleChoice)
            if control == 1:
                ReverseNextStep(PossibleChoice)
                control = 0
                index = -1
                for j in ChoiceList:
                    index += 1
                    if j == PossibleChoice:
                        Weight[index] = 0
            else:
                ReverseNextStep(PossibleChoice)
        ReverseNextStep(col)
#Now remains the possible moves and their corresponding weights.
    """    print("Next Available Space: ", NextAvailableSpace)"""
    for i in range(len(ChoiceList)):
        if Weight[i] == 0:
            continue
        else:
            if NextAvailableSpace[ChoiceList[i]] <= 3:
                Weight[i] = 2 #set a low weight to columns remaining not enough spaces.
                
    """ print("Weight: ",Weight)
    print("ChoiceList: ",ChoiceList)"""
    if Weight == [0 for i in range(len(ChoiceList))]:#The computer will lose anyway
        choice = random.choices(ChoiceList,k=1)[0]
    else:
        choice = random.choices(ChoiceList,weights = Weight,k=1)[0]
        # I have no idea why this result is always a list with only one element...
    #probably because I am not familiar with this function.
    return choice

def Computer():
    global level
    if level == 1:
        return RandomComputer()
    if level == 2:
        return MoreAdvancedComputer()
    if level == 3:
        return HardComputer()

def GameEnd():
    global control
    if control == 1 and mode == 1:
        if count % 2  == 0:
            print("Player 1 wins.")
        else:
            print("Player 2 wins.")
    elif control == 1 and mode == 2:
        if count % 2 != Sequence % 2:
            print("Congratulations! You win!")
        else:
            print("Oops! The computer wins!")

def This_token():
    global count
    if count % 2 == 0:
        return " # "
    else:
        return " @ "
def Opposite_token():
    global count
    if count % 2 == 0:
        return " @ "
    else:
        return " # "
#For Hard Level
def evaluate_board(ai_token):
    global control
    if ai_token == " # ":
        player_token = " @ "
    else:
        player_token = " # "
    # Prefer to have a move on the middle column
    middle = 4
    middle_score = 0
    score_total = 0 #This is the total score of the board
    for r in range(1, 7):
        if BoardLine[r][middle] == ai_token:
            middle_score += 1
        elif BoardLine[r][middle] == player_token:
            middle_score -= 1
    score_total += middle_score * 3

    def score(board): # To evaluate the score of four in a row, a colomn, and a line.
        ai = board.count(ai_token)
        player = board.count(player_token)
        empty = board.count("   ")
        value = 0
        if ai == 4: value += 100000
        elif ai == 3 and empty == 1: value += 100
        elif ai == 2 and empty == 2: value += 10
        if player == 3 and empty == 1: value -= 120
        elif player == 2 and empty == 2: value -= 12
        return value
    #four directions, k is the change in that direction.
    for i in range(1, 7):
        for j in range(1, 5):
            score_total += score([BoardLine[i][j+k] for k in range(4)])

    for i in range(1, 8):
        for j in range(1, 4):
            score_total += score([BoardLine[j+k][i] for k in range(4)])

    for i in range(1, 4):
        for j in range(1, 5):
            score_total += score([BoardLine[i+k][j+k] for k in range(4)])
  
    for i in range(4, 7):
        for j in range(1, 5):
            score_total += score([BoardLine[i-k][j+k] for k in range(4)])

    return score_total

def minimax(depth, maximizing, ai_token):
    global count
    global control
    valid_cols = Available_Columns()
    if depth == 0 or valid_cols == []:
        return None, evaluate_board(ai_token)
    
    if maximizing == True: # This role is AI's
        best_col = None
        best_val = -(10 ** 9)
        for col in valid_cols:
            NextStep(col)
            win(col)
            if control == 1:
                last_token = BoardLine[NextAvailableSpace[col] + 1][col]
                if last_token == ai_token:
                    val = 10 ** 8
                else:
                    val = - (10 ** 8)
                control = 0
            else:
                control = 0
                a, val = minimax(depth - 1, False, ai_token) # As the function returns a tuple, we create a useless variable to contain the first one.

            ReverseNextStep(col)
            control = 0

            if val > best_val:
                best_val= val
                best_col = col

        return best_col, best_val
    else: # It's the Player's turn so we want to minimise this
        best_col = None
        best_val = 10 ** 9
        
        for col in valid_cols:
            NextStep(col)
            win(col)
            if control == 1:
                last_token = BoardLine[NextAvailableSpace[col] + 1][col]
                if last_token == ai_token:
                    val = (10 ** 8)
                else:
                    val = -(10 ** 8)
                control = 0
            else:
                control = 0
                a, val = minimax(depth - 1, True, ai_token) # Similar reason as before

            ReverseNextStep(col)
            control = 0

            if val < best_val:
                best_val = val
                best_col = col
        return best_col, best_val


def HardComputer():
    global control
    ai_token = This_token()
    depth = 3
    valid_cols = Available_Columns()
    for col in valid_cols: # If this step will win directly, immediatly.
        NextStep(col)
        win(col)
        if control == 1:
            control = 0
            ReverseNextStep(col)
            return col
        ReverseNextStep(col)
    best_col, a = minimax(depth, True, ai_token)
    print(best_col)
    if best_col == None:
        best_col = random.choice(valid_cols)
    return best_col


#initialize        
print("""In this code, the 2 players will use the notations"@"and "#" as the representation of white and black. The black one,"@", will be the first one to move.""")
mode = int(input("""Press "1" for playing with friends, and press "2" for playing with the computer:""")) #introduction
control=0 #indicate if the game ends
count=1 #role
BoardLine=[["   ","   ","   ","   ","   ","   ","   ","   "] for i in range(7)]
 #the structure of the board. The spaces can separate the labels to make the board more spreaded out
NextAvailableSpace=["",6,6,6,6,6,6,6]#to note if a column is full.
 #This number is the next row in a specific column that can have a move.


#main
if mode == 1:
    Board()
    while control == 0:
        if count % 2 == 0:
            print("""Now is player 2("#")'s turn.""", end = "")
        else:
            print("""Now is player 1("@")'s turn.""", end = "")
        choice = SelectChoice()
        NextStep(choice)
        Board()
        win(choice)

    
elif mode == 2:
    Sequence = int(input("Please choose 1 if you want to move first and 2 for second:"))
    level = int(input("Please choose the level of computer(1 stands for easy, 2 for medium, 3 for hard.):"))
    Board()
    while control == 0:
            if Sequence == 1:
                if count % 2 == 1:# Player First
                    choice = SelectChoice()
                else:
                    choice = Computer()
                    print(f"The computer falls on column {choice}.")
                NextStep(choice)
                Board()
                win(choice)
                GameEnd()
            else:

                if count % 2 == 0:
                    choice = SelectChoice()
                else:
                    choice = Computer()
                    print(f"The computer falls on column {choice}.")
                NextStep(choice)
                Board()
                win(choice)
                GameEnd()
                        
 
            

