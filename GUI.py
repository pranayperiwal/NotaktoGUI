import pygame
from grid import Grid
import copy
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '350,100'

surface = pygame.display.set_mode((680, 250))
pygame.display.set_caption("Notakto")
pygame.init()

running = True
font = pygame.font.SysFont("calibri", 20)
grid = Grid()


def bestmove():
    bestscore = -999
    for key in grid.keys:
        for i in range(9):
            copyp = copy.deepcopy(grid.pattern)
            if copyp[key][i] != "X":
                copyp[key][i] = "X"
                score = minimax(key, copyp, 0, False, 2, -999, 999)
                if score > bestscore:
                    bestscore = score
                    move = key, i
    return move


scores = {1: 10, 2: -10}


def minimax(key, copyp, depth, isMaximizing, player, alpha, beta):
    grid.check(key, copyp)
    if len(grid.pattern) > 1:
        if depth == 4:
            return scores[player]
    elif len(copyp) == 0:
        return scores[player]

    keys = copyp.keys()
    if (isMaximizing):
        bestscore = -999
        for key in keys:
            for i in range(9):
                new = copy.deepcopy(copyp)
                if new[key][i] != "X":
                    new[key][i] = "X"
                    score = minimax(key, new, depth + 1, False, 2, alpha, beta)
                    bestscore = max(score, bestscore)
                    alpha = max(alpha, bestscore)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return bestscore
    else:
        bestscore = 999
        for key in keys:
            for i in range(9):
                new = copy.deepcopy(copyp)
                if new[key][i] != "X":
                    new[key][i] = "X"
                    score = minimax(key, new, depth + 1, True, 1, alpha, beta)
                    bestscore = min(score, bestscore)
                    beta = min(beta, bestscore)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return bestscore


player = count = 1
while running:
    surface.fill((0, 0, 0))
    text = font.render("Player " + str(player) + "'s move", True, (255, 255, 255))
    surface.blit(text, (10, 220))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player == 2:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if pos[0] <= 210:
                        grid.set_cell_value(pos[0] // 70, pos[1] // 70, 'A')
                    elif 235 <= pos[0] <= 445:
                        grid.set_cell_value((pos[0] - 235) // 70, pos[1] // 70, 'B')
                    elif 470 <= pos[0] <= 680:
                        grid.set_cell_value((pos[0] - 470) // 70, pos[1] // 70, 'C')
            player = 1
            break
        if player == 1:
            player = 2
            if count <= 2:
                count += 1
                if 'A' in grid.keys:
                    if grid.pattern['A'][4] == 4:
                        grid.set_cell_value(1, 1, 'A')
                        break
                    if grid.pattern['A'][0] == 0:
                        grid.set_cell_value(0, 0, 'A')
                        break
            if count == 3:
                count += 1
                if 'C' in grid.keys:
                    if grid.pattern['C'][4] == 4:
                        grid.set_cell_value(1, 1, 'C')
                        break
            key, number = bestmove()
            y, x = grid.get_cell_value(key, number)
            if key == 'A':
                grid.set_cell_value(x // 70, y // 70, key)
            if key == 'B':
                grid.set_cell_value((x - 235) // 70, y // 70, key)
            if key == 'C':
                grid.set_cell_value((x - 470) // 70, y // 70, key)

    if len(grid.pattern) == 0:
        running = False
    grid.draw(surface, player)
    pygame.display.flip()
