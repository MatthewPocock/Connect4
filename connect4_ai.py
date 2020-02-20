import pygame
import sys
import time
import copy
import numpy as np
import random
import math


def createGame():
    return np.zeros((6, 7))


def checkWin(board):
    for ix, iy in np.ndindex(board.shape):
        if board[ix, iy] != 0:

            if iy <= board.shape[1] - 4:
                if board[ix, iy] == board[ix, iy+1] == board[ix, iy+2] == board[ix, iy+3]:
                    return board[ix, iy]

            if ix <= board.shape[0] - 4:
                if board[ix, iy] == board[ix+1, iy] == board[ix+2, iy] == board[ix+3, iy]:
                    return board[ix, iy]

            if iy <= board.shape[1] - 4 and ix <= board.shape[0] - 4:
                if board[ix, iy] == board[ix+1, iy+1] == board[ix+2, iy+2] == board[ix+3, iy+3]:
                    return board[ix, iy]

            if iy + 4 >= board.shape[1] and ix <= board.shape[0] - 4:
                if board[ix, iy] == board[ix+1, iy-1] == board[ix+2, iy-2] == board[ix+3, iy-3]:
                    return board[ix, iy]

    if np.count_nonzero(board) == board.size:
        return 0

    return False


def addMove(board, player, col):
    tmpBoard = copy.deepcopy(board)
    for i in range(board.shape[0]-1, -1, -1):
        if tmpBoard[i, col] == 0:
            tmpBoard[i, col] = player
            return tmpBoard


def getEmptyPositions(board):
    remainingMoves = []
    for ix, iy in np.ndindex(board.shape):
        if board[ix, iy] == 0:
            remainingMoves.append((ix, iy))
    return remainingMoves


def getPossibleMoves(board):
    possibleMoves = []
    for col in range(board.shape[1]):
        for row in range(board.shape[0]-1, -1, -1):
            if board[row, col] == 0:
                possibleMoves.append((row, col))
                break
    return possibleMoves


def checkColFull(board, col):
    if board[0, col] == 0:
        return False
    else:
        return True


def minimax(board, maximisingPlayer, depth, alpha, beta):

    if depth == 0 and board.tobytes() in cachedPositions:
        return None, cachedPositions[board.tobytes()]

    if checkWin(board) is not False or depth == 0:
        return None, getValue(board)

    if maximisingPlayer:
        value = -math.inf
        moveValues = {}
        for move in getPossibleMoves(board):
            moveValues[move] = minimax(addMove(board, 1, move[1]), False, depth-1, alpha, beta)[1]
            if depth == 1:
                cachedPositions[addMove(board, 1, move[1]).tobytes()] = moveValues[move]
            value = max(moveValues[move], value)
            alpha = max(alpha, value)
            if alpha >= beta and depth < 2:
                break
        maxV = max(moveValues.values())
        return random.choice([key for key, value in moveValues.items() if value == maxV]), maxV

    else:
        value = math.inf
        moveValues = {}
        for move in getPossibleMoves(board):
            moveValues[move] = minimax(addMove(board, 2, move[1]), True, depth-1, alpha, beta)[1]
            if depth == 1:
                cachedPositions[addMove(board, 2, move[1]).tobytes()] = moveValues[move]
            value = min(moveValues[move], value)
            beta = min(beta, value)
            if alpha >= beta and depth < 2:
                break
        minV = min(moveValues.values())
        return random.choice([key for key, value in moveValues.items() if value == minV]), minV


def getValue(board):
    result = checkWin(board)
    if result == 0:
        return countWins(board, 1) - countWins(board, 2)
    elif result == 1:
        return 100
    elif result == 2:
        return -100


def countWins(board, player):
    tmpBoard = copy.copy(board)
    tmpBoard[tmpBoard == 0] = player
    count = 0
    for ix, iy in np.ndindex(board.shape):
        if tmpBoard[ix, iy] == player:
            if iy <= board.shape[1] - 4:
                if tmpBoard[ix, iy] == tmpBoard[ix, iy+1] == tmpBoard[ix, iy+2] == tmpBoard[ix, iy+3]:
                    count += 1
            if iy <= tmpBoard.shape[1] - 4 and ix <= tmpBoard.shape[0] - 4:
                if tmpBoard[ix, iy] == tmpBoard[ix+1, iy+1] == tmpBoard[ix+2, iy+2] == tmpBoard[ix+3, iy+3]:
                    count += 1
            if iy + 4 >= tmpBoard.shape[1] and ix <= tmpBoard.shape[0] - 4:
                if tmpBoard[ix, iy] == tmpBoard[ix+1, iy-1] == tmpBoard[ix+2, iy-2] == tmpBoard[ix+3, iy-3]:
                    count += 1
    return count


def colPos(x):
    return x[0] // 100 * 100, 0


def gamePos(x):
    return x[0] // 100, 0


def windowPos(position):
    return [position[1] * 100, position[0] * 100 + 100]


def redrawWindow(board, window):
    background = pygame.image.load("board.png")
    redCoin = pygame.image.load("redCoin.png")
    yellowCoin = pygame.image.load("yellowCoin.png")
    window.fill((255, 255, 255), (0, 100, 700, 700))
    window.blit(background, (0, 100))

    for ix, iy in np.ndindex(board.shape):
        if board[ix, iy] == 1:
            window.blit(redCoin, windowPos([ix, iy]))

        elif board[ix, iy] == 2:
            window.blit(yellowCoin, windowPos([ix, iy]))

    pygame.display.update()


def redrawHeader(turn, window):
    redCoin = pygame.image.load("redCoin.png")
    window.fill((255, 255, 255), (0, 0, 700, 100))

    if turn == 1:
        mousex, mousey = pygame.mouse.get_pos()
        window.blit(redCoin, colPos((mousex, mousey)))

    pygame.display.update()


def displayWinner(board, window):
    window.fill((255, 255, 255), (0, 0, 700, 100))
    font = pygame.font.Font('freesansbold.ttf', 50)

    if checkWin(board) == 0:
        print('draw')
        text = font.render("draw", True, (0, 0, 0))
        window.blit(text, (287, 25))

    else:
        print("Player " + str(int(checkWin(board))) + " wins")
        text = font.render(("Player " + str(int(checkWin(board))) + " Wins!!"), True, (0, 0, 0))
        window.blit(text, (175, 25))

    pygame.display.update()


def main():
    game = createGame()

    pygame.init()
    pygame.display.set_caption("Connect 4")
    screen = pygame.display.set_mode((game.shape[0] * 100 + 100, game.shape[1] * 100))
    pygame.display.update()

    turn = 0

    while checkWin(game) is False:

        redrawWindow(game, screen)

        if turn % 2 == 0:  # player turn
            redrawHeader(1, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
                    if pressed1:
                        pos = gamePos(pygame.mouse.get_pos())

                        if checkColFull(game, pos[0]):
                            print("error: cannot move here")
                            continue

                        game = addMove(game, 1, pos[0])
                        print(game)
                        redrawWindow(game, screen)
                        turn += 1
                        break

        else:  # ai turn
            redrawHeader(2, screen)
            selection = minimax(game, False, 5, -math.inf, math.inf)[0]
            game = addMove(game, 2, selection[1])
            redrawWindow(game, screen)
            turn += 1

    displayWinner(game, screen)
    time.sleep(4)
    print(game)



cachedPositions = {}
main()
