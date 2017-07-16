How to use snake game:
1. create a fresh gameState object. Game field geometry and randomizer seed will be set at this time.
2. Step the game forward with run(turn). Use turn = -1 to turn left, 0 to continue straight ahead, or 1 to turn right. The return value will be -1 if the snake survives, otherwise it will return the score from that game.
3. Observe the world with look(). This fuinction will return the tuple of the visible grid and the relative position of the prey ([downrange, right]).
