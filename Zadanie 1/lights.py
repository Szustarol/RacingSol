#!/usr/bin/python3

import time
import curses

class State:
    def __init__(self, pedestrianColor, roadColor, delay, skippable, name):
        """
        Create light a state machine state.
        Keyword arguments:
        pedestrianColor -- color of the pedestrian light in this state.
        roadColor -- color of the road light in this state.
        delay -- time to be spent in this state.
        skippable -- if this state is skippable by a keypress
        name -- name of this state
        """
        self.pedestrianColor = pedestrianColor
        self.roadColor = roadColor
        self.delay = delay
        self.skippable = skippable
        self.name = name


# Potrzebne do wykrywania kliknięcia
cursesScr = curses.initscr()
cursesScr.scrollok(1)

def waitDelay(delay):
    """Wait for @delay seconds. Curses scr has to be initialised"""
    global cursesScr
    curses.flushinp()
    cursesScr.timeout(delay*1000)
    cursesScr.getch()

if __name__ == "__main__":

    states = [
        State("zielony", "czerwony", 10, False, "Stan 1"),
        State("czerwony", "zielony", 20, True, "Stan 2"),
        State("czerwony", "żółty", 2, False, "Stan 3")
    ]

    stateIndex = 0

    waitDelay(0)
    # Wait for initial key press to start the loop
    print("Press any key to start.\r")
    waitDelay(-1)

    print("Starting state machine. Press Ctrl-C to stop.\r")

    startTime = time.time()

    while True:
        
        currentState = states[stateIndex]

        # Print state info
        print("[{:.2f}]<{}>: Światło pieszego: {}, światło drogowe: {}.\r".format(
                time.time()-startTime, currentState.name,
                currentState.pedestrianColor, currentState.roadColor
            )
        )

        # if delay is skippable wait for key input
        if currentState.skippable:
            waitDelay(currentState.delay)
        else:
            time.sleep(currentState.delay)

        stateIndex = (stateIndex+1)%len(states)
