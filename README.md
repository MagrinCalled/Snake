First part is a classical Snake game one can can play. Second part is implementation of machine learning to the game to train an ai agent to play the game.
This is done in two approches:
- first approch is really simple and naive, the game state is only the direction of danger (up, down, left, right), direction of the food and current direction as one hot inputs.
We can see that it is pretty basic but it quickly to high scores (as high as arround 110 with less than 1_000 games) but the main bottleneck of this approch is the fact that because
no information is given to the agent regarding relative position of the tail, walls etc. it won't be able to derive a strategy and will keep getting trapped by its own tail.

- second approch is more complete with an 11 by 11 grid centered at the snake's head with encoded environement (0 for empty cell, -1 for wall or body and +1 for food), a reward system that
encitivize movement towards the apple, that also should promote safe paths (I implemented a function called "reachable_space()" but it didn't yield to significant changes to the agent behavior).
The agent in that second model with 512 neurons in the hidden layer is greatly suboptimal comparing to the first. Indeed the first model is 11 features for 256 neurones and a highest score of
around 110 after 1_000 games and the second one with 130 features and 512 neurones is only at a highest score of around 100 after 4_300 games.
Maybe this is because the number of neurones/layer is complete not adapted to the number of features. This would be interesting to see I might add a third model with the same features reward
system as the second one but with a 130 x 512 x 256 x 3 structure with two hidden layers. For now enjoy the code !!
