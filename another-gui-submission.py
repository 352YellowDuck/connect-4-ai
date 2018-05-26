import sys
import numpy
from tkinter import Tk, Button, Frame, Canvas, font, messagebox

BOARD_WIDTH = 7
BOARD_HEIGHT = 6
SEARCH_DEPTH = 4

COMPUTER_PLAYER = 1
HUMAN_PLAYER = -1

gameState = [[0 for col in range(BOARD_WIDTH)] for row in range(BOARD_HEIGHT)]
moveHeights = [0] * BOARD_WIDTH
winner = 0
gameOver = False
remainingColumns = BOARD_WIDTH
compTileColor = "yellow"
playerTileColor  ="green"


# Runs the minimax algorithm and returns
# the move and score of each call.

def minimax(gameState, depth, player, opponent, scoreEvalAlg):
    availableMoves = BOARD_WIDTH
    for i in range(0, BOARD_WIDTH):
        if gameState[0][i] != 0:
            availableMoves -= 1

    if depth == 0 or availableMoves == 0:
        score = scoreEvalAlg(gameState, player, opponent)
        return None, score

    bestScore = None
    bestMove = None

    for i in range(0, BOARD_WIDTH):
        # If moves cannot be made on column, skip it
        if gameState[0][i] != 0:
            continue

        currentMove = [0, i]

        for j in range(0, BOARD_HEIGHT - 1):
            if gameState[j + 1][i] != 0:
                gameState[j][i] = player
                currentMove[0] = j
                break
            elif j == BOARD_HEIGHT - 2:
                gameState[j+1][i] = player
                currentMove[0] = j+1

        # Recursive minimax call, with reduced depth
        move, score = minimax(gameState, depth - 1,
                              opponent, player, scoreEvalAlg)

        gameState[currentMove[0]][currentMove[1]] = 0

        if player == COMPUTER_PLAYER:
            if bestScore == None or score > bestScore:
                bestScore = score
                bestMove = currentMove
        else:
            if bestScore == None or score < bestScore:
                bestScore = score
                bestMove = currentMove

    return bestMove, bestScore


def evaluateScore(gameState, player, opponent):
    score = checkWin(gameState)

    if score == player:
        return float("inf")
    elif score == opponent:
        return float("-inf")
    else:
        score = 0

    for i in range(0, BOARD_HEIGHT):
        for j in range(0, BOARD_WIDTH):
            if gameState[i][j] == 0:
                score += scoreOfCoordinate(gameState, i, j, player, opponent)

    return score


def scoreOfCoordinate(gameState, i, j, player, opponent):
    score = 0

    # Check vertical line
    score += scoreOfLine(
        gameState=gameState,
        i=i,
        j=j,
        rowIncrement=-1,
        columnIncrement=0,
        firstRowCondition=-1,
        secondRowCondition=BOARD_HEIGHT,
        firstColumnCondition=None,
        secondColumnCondition=None,
        player=player,
        opponent=opponent
    )

    # Check horizontal line
    score += scoreOfLine(
        gameState=gameState,
        i=i,
        j=j,
        rowIncrement=0,
        columnIncrement=-1,
        firstRowCondition=None,
        secondRowCondition=None,
        firstColumnCondition=-1,
        secondColumnCondition=BOARD_WIDTH,
        player=player,
        opponent=opponent
    )

    # Check diagonal /
    score += scoreOfLine(
        gameState=gameState,
        i=i,
        j=j,
        rowIncrement=-1,
        columnIncrement=1,
        firstRowCondition=-1,
        secondRowCondition=BOARD_HEIGHT,
        firstColumnCondition=BOARD_WIDTH,
        secondColumnCondition=-1,
        player=player,
        opponent=opponent
    )

    # Check diagonal \
    score += scoreOfLine(
        gameState=gameState,
        i=i,
        j=j,
        rowIncrement=-1,
        columnIncrement=-1,
        firstRowCondition=-1,
        secondRowCondition=BOARD_HEIGHT,
        firstColumnCondition=-1,
        secondColumnCondition=BOARD_WIDTH,
        player=player,
        opponent=opponent
    )

    return score


def scoreOfLine(
    gameState,
    i,
    j,
    rowIncrement,
    columnIncrement,
    firstRowCondition,
    secondRowCondition,
    firstColumnCondition,
    secondColumnCondition,
    player,
    opponent
):
    score = 0
    currentInLine = 0
    valsInARow = 0
    valsInARowPrev = 0

    # Iterate in one side of the line until a move from another
    # player or an empty space is found
    row = i + rowIncrement
    column = j + columnIncrement
    firstLoop = True
    while (
        row != firstRowCondition and
        column != firstColumnCondition and
        gameState[row][column] != 0
    ):
        if firstLoop:
            currentInLine = gameState[row][column]
            firstLoop = False
        if currentInLine == gameState[row][column]:
            valsInARow += 1
        else:
            break
        row += rowIncrement
        column += columnIncrement

    # Iterate on second side of the line
    row = i - rowIncrement
    column = j - columnIncrement
    firstLoop = True
    while (
        row != secondRowCondition and
        column != secondColumnCondition and
        gameState[row][column] != 0
    ):
        if firstLoop:
            firstLoop = False

            # Verify if previous side of line guaranteed a win on the
            # coordinate, and if not, continue counting to see if the
            # given coordinate can complete a line from in between.
            if currentInLine != gameState[row][column]:
                if valsInARow == 3 and currentInLine == player:
                    score += 1
                elif valsInARow == 3 and currentInLine == opponent:
                    score -= 1
            else:
                valsInARowPrev = valsInARow

            valsInARow = 0
            currentInLine = gameState[row][column]

        if currentInLine == gameState[row][column]:
            valsInARow += 1
        else:
            break
        row -= rowIncrement
        column -= columnIncrement

    if valsInARow + valsInARowPrev >= 3 and currentInLine == player:
        score += 1
    elif valsInARow + valsInARowPrev >= 3 and currentInLine == opponent:
        score -= 1

    return score


def bestMove(gameState, player, opponent, scoreEvalAlg):
    for i in range(0, BOARD_WIDTH):
        # If moves cannot be made on column, skip it
        if gameState[0][i] != 0:
            continue

        currentMove = [0, i]

        for j in range(0, BOARD_HEIGHT - 1):
            if gameState[j + 1][i] != 0:
                gameState[j][i] = player
                currentMove[0] = j
                break
            elif j == BOARD_HEIGHT - 2:
                gameState[j+1][i] = player
                currentMove[0] = j+1

        winner = checkWin(gameState)
        gameState[currentMove[0]][currentMove[1]] = 0

        if winner == COMPUTER_PLAYER:
            return currentMove[1]

    for i in range(0, BOARD_WIDTH):
        # If moves cannot be made on column, skip it
        if gameState[0][i] != 0:
            continue

        currentMove = [0, i]

        for j in range(0, BOARD_HEIGHT - 1):
            if gameState[j + 1][i] != 0:
                gameState[j][i] = opponent
                currentMove[0] = j
                break
            elif j == BOARD_HEIGHT - 2:
                gameState[j+1][i] = opponent
                currentMove[0] = j+1

        winner = checkWin(gameState)
        gameState[currentMove[0]][currentMove[1]] = 0

        if winner == HUMAN_PLAYER:
            return currentMove[1]

    move, score = minimax(gameState, SEARCH_DEPTH,
                          player, opponent, scoreEvalAlg)
    return move[1]

# check if someone has won

def checkWin(gameState):
    current = 0
    currentCount = 0
    computer_wins = 0
    opponent_wins = 0

    # Check horizontal wins
    for i in range(0, BOARD_HEIGHT):
        for j in range(0, BOARD_WIDTH):
            if currentCount == 0:
                if gameState[i][j] != 0:
                    current = gameState[i][j]
                    currentCount += 1
            elif currentCount == 4:
                if current == COMPUTER_PLAYER:
                    computer_wins += 1
                else:
                    opponent_wins += 1
                currentCount = 0
                break
            elif gameState[i][j] != current:
                if gameState[i][j] != 0:
                    current = gameState[i][j]
                    currentCount = 1
                else:
                    current = 0
                    currentCount = 0
            else:
                currentCount += 1

        if currentCount == 4:
            if current == COMPUTER_PLAYER:
                computer_wins += 1
            else:
                opponent_wins += 1
        current = 0
        currentCount = 0

    # Check vertical wins
    for j in range(0, BOARD_WIDTH):
        for i in range(0, BOARD_HEIGHT):
            if currentCount == 0:
                if gameState[i][j] != 0:
                    current = gameState[i][j]
                    currentCount += 1
            elif currentCount == 4:
                if current == COMPUTER_PLAYER:
                    computer_wins += 1
                else:
                    opponent_wins += 1
                currentCount = 0
                break
            elif gameState[i][j] != current:
                if gameState[i][j] != 0:
                    current = gameState[i][j]
                    currentCount = 1
                else:
                    current = 0
                    currentCount = 0
            else:
                currentCount += 1

        if currentCount == 4:
            if current == COMPUTER_PLAYER:
                computer_wins += 1
            else:
                opponent_wins += 1
        current = 0
        currentCount = 0

    # Check diagonal wins
    np_matrix = numpy.array(gameState)
    diags = [np_matrix[::-1, :].diagonal(i)
             for i in range(-np_matrix.shape[0]+1, np_matrix.shape[1])]
    diags.extend(np_matrix.diagonal(i)
                 for i in range(np_matrix.shape[1]-1, -np_matrix.shape[0], -1))
    diags_list = [n.tolist() for n in diags]

    for i in range(0, len(diags_list)):
        if len(diags_list[i]) >= 4:
            for j in range(0, len(diags_list[i])):
                if currentCount == 0:
                    if diags_list[i][j] != 0:
                        current = diags_list[i][j]
                        currentCount += 1
                elif currentCount == 4:
                    if current == COMPUTER_PLAYER:
                        computer_wins += 1
                    else:
                        opponent_wins += 1
                    currentCount = 0
                    break
                elif diags_list[i][j] != current:
                    if diags_list[i][j] != 0:
                        current = diags_list[i][j]
                        currentCount = 1
                    else:
                        current = 0
                        currentCount = 0
                else:
                    currentCount += 1

            if currentCount == 4:
                if current == COMPUTER_PLAYER:
                    computer_wins += 1
                else:
                    opponent_wins += 1
            current = 0
            currentCount = 0

    if opponent_wins > 0:
        return HUMAN_PLAYER
    elif computer_wins > 0:
        return COMPUTER_PLAYER
    else:
        return 0

# move function handled by GUI.
# AI move is made in same function

def move(move, tiles, remainingColumns, winner, gameOver):
    moveHeights[move - 1] += 1
    gameState[BOARD_HEIGHT - moveHeights[move - 1]][move] = HUMAN_PLAYER
    tiles[move, BOARD_HEIGHT + moveHeights[move - 1] - 7].create_oval(10, 5, 50, 45, fill= playerTileColor, outline="blue", width=1)
   
    if moveHeights[move - 1] == BOARD_HEIGHT:
        remainingColumns -= 1
    if remainingColumns == 0:
        gameOver = True
    if gameOver:
        return

    score = checkWin(gameState)
    if score == COMPUTER_PLAYER:
        winner = COMPUTER_PLAYER
        return
    elif score == HUMAN_PLAYER:
        winner = HUMAN_PLAYER
        messagebox.showinfo("Message", "Player wins")
        reset()
        return
    else:
        score = 0

    aiMove = bestMove(gameState, COMPUTER_PLAYER, HUMAN_PLAYER, evaluateScore)
    if aiMove == None:
        return

    moveHeights[aiMove - 1] += 1
    gameState[BOARD_HEIGHT - moveHeights[aiMove - 1]][aiMove] = COMPUTER_PLAYER
    tiles[aiMove, BOARD_HEIGHT + moveHeights[aiMove - 1] - 7].create_oval(10, 5, 50, 45, fill= compTileColor, outline="blue", width=1)

    if moveHeights[aiMove] == BOARD_HEIGHT:
        remainingColumns -= 1
    if remainingColumns == 0:
        gameOver = True
    if gameOver:
        return

    score = checkWin(gameState)
    print(score)
    if score == COMPUTER_PLAYER:
        winner = COMPUTER_PLAYER
        messagebox.showinfo("Message", "Computer wins")
        reset()
        return
    elif score == HUMAN_PLAYER:
        winner = HUMAN_PLAYER
        return
    else:
        score = 0

# Reset gamestate and variables for a new game

def reset():
    global gameState
    global gameOver
    global moveHeights
    global winner
    global remainingColumns
    gameState = [[0 for col in range(BOARD_WIDTH)] for row in range(BOARD_HEIGHT)]

    gameOver = False
    moveHeights = [0] * 7
    winner = 0
    remainingColumns = 7
    for i in range(7):
        for j in range(6):
            tiles[i, j].create_oval(10, 5, 50, 45, fill="black", outline="blue", width=1)


#********************GUI***********************
app = Tk()
app.title("Connect4")

buttons = {}
frame = Frame(app, borderwidth=1, relief="raised")
tiles = {}

winner = 0
gameOver = False
moveHeights = [0] * BOARD_WIDTH

for x in range(BOARD_WIDTH):
    handler = lambda x=x: move(x, tiles, remainingColumns, winner, gameOver)  # lambda
    button = Button(app, command=handler, font=font.Font(family="Helvetica", size=14), text=x+1)
    button.grid(row=0, column=x, sticky="WE")
    buttons[x] = button

frame.grid(row=1, column=0, columnspan=BOARD_WIDTH)

for i in range(7):
    for j in range(6):
        tile = Canvas(frame, width=60, height=50,
                      bg="navy", highlightthickness=0)
        val = BOARD_HEIGHT - j
        tile.grid(row=val, column=i+1)
        tiles[i, j] = tile


for i in range(7):
    for j in range(6):
        tiles[i, j].create_oval(10, 5, 50, 45, fill="black", outline="blue", width=1)

 
handler = lambda: reset()
restart = Button(app, command=handler, text='reset')
restart.grid(row=2, column=0, columnspan=BOARD_WIDTH+1, sticky="WE")

app.mainloop()
