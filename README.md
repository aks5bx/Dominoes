# Dominoes

## Introduction 

The variant of Dominoes known as "Mexican Train" (more information [here](https://en.wikipedia.org/wiki/Mexican_Train)) was introduced to me by my girlfriend's family this Christmas (Christmas 2022). After playing a few rounds, I realized that I was making decisions about the game rather algorithmically. More specifically, I was making them in a way that perhaps lent itself to an interest data project. 

So, this repository contains my attempt to create a program (you can call it AI, Machine Learning, fancy statistics, whatever you want) to optimally play Dominoes! 

## Repository Setup 

### Structure 
- I define classes and objects in `domino.py`
- I define neural network structures in `domino_bot.py`

### Environment 

_I use Python Version 3.8.2_

The required packages can be installed using `pip install -r requirements.txt`

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

## Simple Testing 

In order to ensure that multi-player functionality works properly, I include a brief test in the `main()` method within `domino.py`. The method is included below. Note that the randomness of the dealing will create a unique game each time the py file is run. 

```
def main():
    game = Game(4, 12)
    game.add_CPU(2)
    game.add_CPU(3)
    game.add_CPU(4)
    game.current_state()
    game.make_round()
    game.current_state()
    game.score()
```

## Learning 

### Levers to Pull 

When setting up a learning mechanism, I first had to define the options that my program could learn to optimize. I settled on the following options and I include a brief explanation for why each was chose. 

#### Play Train: Mine or Others 

The first option is whether to prioritize playing on your train on playing on someone else's train (if you can). Intuitively, if you train is public, you should probably play on your train if you can (to turn it back to private). Otherwise, you may as well play on someone else's train (if you can) and retain the option to play on your train for later. 

Of course, this is all intuition that we hope our program can learn from repitition. 

#### Build Train: Longest or Heaviest 

The other major option comes when we actually conceptualize our train. We can either prioritize building the longest train we can OR we can prioritize building the "heaviest" train (the train that carries the most total points). Prioritizing the longest train reduces the expected value of the number of times you will have to draw a new tile (because you are instead playing tiles yourself). However, prioritizing the heaviest train ensures that if you don't win, you have at least gotten rid of points that would otherwise count against you. 

The challenge here is for our program to learn when to choose which strategy. 

### Inputs 

We want to give our program information on the status of the game in order to allow it to make an informed decision. However, we want to localize this information to information that a player would reasonably know during the course of the game (we do not, for example, implement "counting dominoes").

We equip our program with the following information: 
- Number of dominoes it has left 
- Number of dominoes the player in the lead (lead as in fewest number of dominoes left) has 
- Total point value of dominoes it has left 
- Whether it is in the lead 
- Whether its train is public 
- Current round number 