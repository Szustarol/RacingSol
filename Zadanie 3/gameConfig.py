#!/usr/bin/python3

import json
import random

class GameConfig:
    def __init__(self, mapWidth, mapHeight, positions, frequency, 
                minNeighbors, spawnNeighbors, overCrowdedNeighbors):
        """Holds the starting game configuration"""
        assert mapHeight > 0 and mapWidth > 0, "Map dimensions must be strictly positive."
        assert overCrowdedNeighbors > spawnNeighbors > minNeighbors > 0, "Invalid game rules"

        for position in positions:
            try:
                l, r = position
                int(l), int(r)
            except:
                print("Invalid position specification!")
                exit(0)

        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.frequency = frequency
        self.spawnNeighbors = spawnNeighbors
        self.overCrowdedNeighbors = overCrowdedNeighbors
        self.minNeighbors = minNeighbors
        self.positions = [
            (posX % mapWidth, posY % mapHeight) for posX, posY in positions
        ] # Ensure position is in valid coordinate range

    def saveToFile(self, file):
        with open(file, "w") as f:
            json.dump(self, f, default=vars)

    @classmethod
    def fromJson(cls, path):
        try:
            with open(path, "r") as f:
                j = json.loads(f.read())
            return cls(**j)
        except BaseException as e:
            print("Invalid input JSON file format.")
            print(e)
            exit(0)

    @classmethod
    def random(cls, width, height, nPoints, frequency):
        points = [
            (random.randint(0, width), random.randint(0, height))
            for _ in range(nPoints)
        ]
        return cls(width, height, points, frequency, 2, 3, 4)

    