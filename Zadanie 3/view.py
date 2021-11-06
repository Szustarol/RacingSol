#!/usr/bin/python3

import pygame

pygame.init()

class View:

    def __init__(self, gameConfig, blockSizePx = 15):
        """Initialises the main game view with @width and @height blocks, each of size @blockSizePx"""
        self.topOffset = 30 # Offset of the board from the top of the screen
        self.width = gameConfig.mapWidth
        self.height = gameConfig.mapHeight
        self.blockSizePx = blockSizePx
        self.surfaceWidth = self.width*blockSizePx
        self.surfaceHeight = self.height*blockSizePx + self.topOffset
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.eventQueue = []

        #PyGame surface
        self.surface = pygame.display.set_mode(
            (self.width*blockSizePx, self.height*blockSizePx+self.topOffset)
        )
        pygame.display.flip()

    def keysPressed(self):
        keys = []
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                keys.append(evt.key)
        return keys

    def drawFrame(self, gameState, calcTime = 0, totalTime = 0):
        # White background
        pygame.draw.rect(self.surface, (255, 255, 255),
            pygame.Rect(0, 0, self.surfaceWidth, self.surfaceHeight))

        # Print calc time and draw time
        calcTextSurface = self.font.render("Czas obliczeń: {:.0f} μs.".format(calcTime*1e6), True, (0,0,0))
        totalTextSurface = self.font.render("Czas symluacji: {:.2f} s.".format(totalTime), True, (0,0,0))
        self.surface.blit(calcTextSurface, (5,3))
        self.surface.blit(totalTextSurface, (self.surfaceWidth-totalTextSurface.get_width()-5,3))


        # Draw each element
        for (y, x) in gameState.getPositions():
            pygame.draw.rect(
                self.surface, (150, 150, 150),
                pygame.Rect(
                    x*self.blockSizePx, y*self.blockSizePx+self.topOffset,
                    self.blockSizePx, self.blockSizePx
                )
            )

        # Small frame for elements
        for wIdx in range(self.width):
            for hIdx in range(self.height):
                pygame.draw.rect(self.surface, (100,100,100), 
                    pygame.Rect(
                        wIdx*self.blockSizePx, self.topOffset+hIdx*self.blockSizePx,
                        self.blockSizePx, self.blockSizePx
                    ),
                    1
                )

        # Thick outside frame
        pygame.draw.rect(self.surface, (0,0,0),
            pygame.Rect(0, self.topOffset, self.surfaceWidth, self.surfaceHeight), 2)

        pygame.display.flip()
