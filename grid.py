import pygame
import os

letterX = pygame.image.load(os.path.join('res', 'x_cropped.png'))


class Grid:
    def __init__(self):
        self.pattern = {'A': [i for i in range(0, 9)], 'B': [i for i in range(0, 9)], 'C': [i for i in range(0, 9)]}
        self.gridlinesA = [((70, 0), (70, 210)),  # first square
                           ((140, 0), (140, 210)),
                           ((0, 70), (210, 70)),
                           ((0, 140), (210, 140))]

        # second sqaure
        self.gridlinesB = [((305, 0), (305, 210)),
                           ((375, 0), (375, 210)),
                           ((235, 70), (445, 70)),
                           ((235, 140), (445, 140))]
        # third square
        self.gridlinesC = [((540, 0), (540, 210)),
                           ((610, 0), (610, 210)),
                           ((470, 70), (680, 70)),
                           ((470, 140), (680, 140))]
        self.keys = self.pattern.keys()
        self.switch = False

    def draw(self, surface, player):
        if 'A' in self.keys:
            for line in self.gridlinesA:
                pygame.draw.line(surface, (255, 255, 255), line[0], line[1], 2)
        if 'B' in self.keys:
            for line in self.gridlinesB:
                pygame.draw.line(surface, (255, 255, 255), line[0], line[1], 2)
        if 'C' in self.keys:
            for line in self.gridlinesC:
                pygame.draw.line(surface, (255, 255, 255), line[0], line[1], 2)
        for key in self.keys:
            for i in range(len(self.pattern[key])):
                if self.pattern[key][i] == "X":
                    x, y = self.get_cell_value(key, i)
                    surface.blit(letterX, (y, x))
        if len(self.keys) == 0:
            surface.fill((0, 0, 0))
            font = pygame.font.SysFont("calibri", 40)
            text = font.render("Player " + str(player) + " Wins!", True, (0, 255, 0))
            surface.blit(text, (220, 100))

    def get_cell_value(self, board, pos):
        if board == 'A':
            return (pos // 3) * 70, (pos % 3) * 70
        if board == 'B':
            return ((pos // 3) * 70), (pos % 3) * 70 + 235
        if board == 'C':
            return ((pos // 3) * 70), (pos % 3) * 70 + 470

    def set_cell_value(self, x, y, board):
        pos = y * 3 + x
        if self.pattern[board][pos] == pos:
            self.pattern[board][pos] = "X"
            self.switch = True
        else:
            self.switch = False
        self.check(board, self.pattern)

    def check(self, key, pattern):
        # rows
        i = 0
        while i < 9:
            if pattern[key][i] == pattern[key][i + 1] == pattern[key][i + 2]:
                del pattern[key]
                return
            i += 3
        # column
        i = 0
        while i < 3:
            if pattern[key][i] == pattern[key][i + 3] == pattern[key][i + 6]:
                del pattern[key]
                return
            i += 1
        # diag
        if pattern[key][0] == pattern[key][4] == pattern[key][8]:
            del pattern[key]
            return
        # anti-diag
        if pattern[key][2] == pattern[key][4] == pattern[key][6]:
            del pattern[key]
            return
