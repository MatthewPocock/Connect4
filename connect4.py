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
    yellowCoin = pygame.image.load("yellowCoin.png")
    window.fill((255, 255, 255), (0, 0, 700, 100))

    if turn == 1:
        mousex, mousey = pygame.mouse.get_pos()
        window.blit(redCoin, colPos((mousex, mousey)))

    if turn == 2:
        mousex, mousey = pygame.mouse.get_pos()
        window.blit(yellowCoin, colPos((mousex, mousey)))

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

        if turn % 2 == 0:  # player 1 turn
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

        else:  # player 2 turn
            redrawHeader(2, screen)

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

                        game = addMove(game, 2, pos[0])
                        print(game)
                        redrawWindow(game, screen)
                        turn += 1

    displayWinner(game, screen)
    time.sleep(4)
    print(game)



cachedPositions = {}
main()
