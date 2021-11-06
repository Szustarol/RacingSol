#!/usr/bin/python3

import numpy as np
from scipy import signal
import time

class GameState:
    def __init__(self, config):
        self.state = np.zeros((config.mapHeight,config.mapWidth))

        # How many neighboors are needed for a cell to die, or to "spawn"
        self.minNeighbors = config.minNeighbors
        self.spawnNeighbors = config.spawnNeighbors
        self.overCrowdedNeighbors = config.overCrowdedNeighbors
        
        self.linearKernel = np.ones((3,3))
        self.linearKernel[1, 1] = 0

        for posX, posY in config.positions:
            self.state[posY, posX] = 1

    def getPositions(self):
        """Returns the positions of elements as a list"""
        return np.argwhere(self.state != 0)

    def progress(self):
        """Returns calculation time in seconds."""
        # A step in a game of life can be written as a linear filter (a convolution)
        # of the input image with a 3x3 linear Kernel of the form:
        # 1 1 1
        # 1 0 1
        # 1 1 1
        # Then, a nonlinear transformation is applied - all pixels for which the
        # convolution result is in range [0, minNeighbors) are always set to zero,
        # points in range [minNeighbors, spawnNeighbors) are left as is, and points
        # in range [spawnNeighbors, overCrowdedNeighbors) are always set to one.
        # Points in range [overCrowdedNeighbors, 8], cells die - always set to zero.
        # Thanks to the usage of a convolution this can be a really fast process.
        
        calcStartTime = time.time()
        mask = signal.convolve2d(self.state, self.linearKernel, boundary="wrap", fillvalue=0, mode="same")
        self.state[(mask < self.minNeighbors) | (mask >= self.overCrowdedNeighbors)] = 0
        self.state[(mask >= self.spawnNeighbors) & (mask < self.overCrowdedNeighbors)] = 1
        return time.time()-calcStartTime
