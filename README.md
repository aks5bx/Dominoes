# Dominoes

## Introduction 

The variant of Dominoes known as "Mexican Train" (more information [here](https://en.wikipedia.org/wiki/Mexican_Train)) was introduced to me by my girlfriend's family this Christmas (Christmas 2022). After playing a few rounds, I realized that I was making decisions about the game rather algorithmically. More specifically, I was making them in a way that perhaps lent itself to an interest data project. 

So, this repository contains my attempt to create a program (you can call it AI, Machine Learning, fancy statistics, whatever you want) to optimally play Dominoes! 

## Repository Setup 

- I define classes and objects in `domino.py`

## Domino Classes and Objects

### Domino 

The class `Domino` defines the structure of a domino. Notably, it has the following attributes: 
- `top` (int): value of the top of the domino 
- `bottom` (int): value of the bottom of the domino 
- `double` (bool): whether or not the domino has the same top and bottom value 
- `total` (int): total sum of dots (top and bottom)

I also note here that the `double` attribute is useful because playing a double means you get an extra turn. However, I do not add that functionality into the program (for now). 

### Player 

The class `Player` defines a single player (can be the user or a CPU). Each player keeps track of:
- `domino_lst` (list): list of dominoes in player's posession 
- `train_queue` (list): a pre-made train constructed from dominoes within `domino_lst` 

Each `Player` must join a `Game`, where they participate using the `play_turn()` method that belongs to `Player`

### GamePlay

The class `GamePlay` defines the necessary objects to keep track of for a single round of the game. This includes: 
- `round_num` (int): round number 
- `pool` (list): list of dominoes that can be drawn/dealt 
- `train_dict` (dict): dictionary of tuples of the format `{player_num : (list(Domino), Bool)}`; the list of dominoes represents the dominoes that have been played as part of a player's train and the Bool represents whether or not the train is public

### Game 

The class `Game` is responsible for keeping track of the game writ large. Notably, while the class `GamePlay` handles the active changes to a single round, the class `Game` is primarily responsible for keeping track of meta-game information. This chiefly includes: 
- `score_dict` (dict): dictionary of scores in the format `{player_num : score (int)}`