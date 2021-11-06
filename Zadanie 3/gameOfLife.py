#!/usr/bin/python3

import gameConfig
import gameState
import view
import sys
import pygame
import time

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No config file specified, generating random map.")
        config = gameConfig.GameConfig.random(40, 40, 120, 1)
    else:
        config = gameConfig.GameConfig.fromJson(sys.argv[1])

    state = gameState.GameState(config)

    mainView = view.View(config)
    mainView.drawFrame(state)

    # For limiting frames on a single thread
    # I use a timer, so keypresses can be detected.
    frameStartTime = time.time()
    startTime = time.time()
    while True:
        frameTime = time.time()
        # If enough time has elapsed for a new frame to be drawn
        if frameTime-frameStartTime > config.frequency:
            frameStartTime = frameTime
            progressTime = state.progress()
            mainView.drawFrame(state, calcTime = progressTime, totalTime=time.time()-startTime)
        
        # End if ESC is pressed
        keysPressed = mainView.keysPressed()
        if pygame.K_ESCAPE in keysPressed:
            break
        