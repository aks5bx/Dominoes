import pandas as pd 
import numpy as np 
import torch 
import random 

class Domino():
    def __init__(self, top, bottom):
        self.top = top 
        self.bottom = bottom 

        if top == bottom:
            self.double = True
        else:
            self.double = False

        self.total = top + bottom

    def __repr__(self):
        return str(self.top) + ' | ' + str(self.bottom)
    
    def visualize(self):

        top = str(self.top)
        bottom = str(self.bottom)

        if len(top) == 1:
            top = ' ' + top
        if len(bottom) == 1:
            bottom = ' ' + bottom

        print(' -----')
        print('|     |')
        print('| ', str(self.top), ' |')
        print('|     |')
        print(' -----')
        print('|     |')
        print('| ', str(self.bottom), ' |')
        print('|     |')
        print(' -----')


class Player():
    def __init__(self, domino_lst=None, player_num=1):
        if domino_lst is not None:
            self.domino_list = domino_lst
            self.num_of_dominoes = len(domino_lst)
        else:
            self.domino_list = []
            self.num_of_dominoes = 0
        
        self.game = None 
        self.player_num = player_num
        self.train_queue = []

    def info(self):
        d_lst = self.domino_list
        print('--' * 25)   
        print('Number of dominoes: ', self.num_of_dominoes)
        print('Currently Playing?  ', self.game is not None)
        print('--' * 25)   

    def join_game(self, gameplay):
        self.game = gameplay

    def add_dominoes(self, domino_lst):
        self.domino_list += domino_lst
        self.num_of_dominoes += len(domino_lst)
    
    def valid_play(self, play_domino, train_num):
        if self.game.train_dict[train_num][1] == False and self.player_num != train_num:
            return False
        elif self.game.train_dict[train_num][0][-1][1] != play_domino.top:
            return False 
        else:
            return True 
    
    def play_domino(self, play_domino, train_num):
        # play domino should be a tuple of (top, bottom) 
        if self.valid_play(play_domino, train_num):
            self.game.train_dict[train_num][0].append(play_domino)
            self.domino_list.remove(play_domino)
            self.num_of_dominoes -= 1

            # if you play on your own train, your train is private 
            if self.player_num == train_num:
                self.game.train_dict[train_num][1] = False

            return 1 

        else:
            return 0 

    def draw(self):
        new_dominoes_lst = self.game.deal_to_one(1)
        self.domino_list += [new_dominoes_lst[0]]
        return new_dominoes_lst[0]

    def get_my_train(self, last = False):
        if last:
            return self.game.train_dict[self.player_num][0][-1]
        else:
            return self.game.train_dict[self.player_num][0]

    def sort_dominoes(self):
        sorted_dominoes = sorted(self.domino_list, key=lambda x: x.total, reverse=True)
        return sorted_dominoes 

    def make_train(self, dominoes):

        '''
        INPUT: dominoes - list of type Domino 
        OUTPUT: longest train - list of type Domino 
        '''

        # Create a graph where each domino is a node, and edges connect dominoes that can be chained together
        graph = {}
        for domino in dominoes:
            graph[domino] = []
            other_dominoes = [d for d in dominoes if d != domino]

            for other in other_dominoes:
                if domino.bottom == other.top:
                    graph[domino].append(other)

        # Find the longest chain of connected dominoes using a depth-first search
        def dfs(graph, node, visited, train):
            visited.add(node)
            train.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(graph, neighbor, visited, train)

        # Initialize the longest train with the first domino
        longest_train = [self.get_my_train(last=True)]

        # Iterate through the remaining dominoes and find the longest train starting from each one
        for domino in dominoes:
            train = []
            visited = set()
            dfs(graph, domino, visited, train)
            if len(train) > len(longest_train):
                longest_train = train

        self.train_queue = longest_train
        return longest_train

    def play_my_train(self):
        train_num = self.player_num
        play_domino = self.train_queue.pop(0)

        play_attempt = self.play_domino(play_domino, train_num)

        return play_attempt

    def play_highest_domino(self):
        sorted_dominoes = self.sort_dominoes()
        for big_domino in sorted_dominoes:
            for train_num in range(1, self.game.num_players + 1):
                if train_num == self.player_num:
                    continue
                else:
                    play_attempt = self.play_domino(big_domino, train_num)
                    if play_attempt == 1:
                        return play_attempt, big_domino, train_num

        for big_domino in sorted_dominoes:
            play_attempt = self.play_domino(big_domino, self.player_num)
            if play_attempt == 1:
                return play_attempt, big_domino, train_num

        return 0, None, None 

    def play_drawn_domino(self, drawn):
        for train_num in range(1, self.game.num_players + 1):
            if train_num == self.player_num:
                continue
            else:
                play_attempt = self.play_domino(drawn, train_num)
                if play_attempt == 1:
                    return play_attempt, drawn, train_num

        play_attempt = self.play_domino(drawn, self.player_num)

        if play_attempt == 1:
            return play_attempt, drawn, train_num
        else:
            return 0, None, None


    def play_turn(self, my_train = True, highest_domino = False):
        play_result = -1

        ## Priority is to play on your own train
        if my_train and len(self.train_queue) > 0: 
            attempt1 = self.play_my_train()
            if attempt1 == 1:
                play_result = 1
                print('Played on my train')
            else:
                print('Could not play my train, trying another train')
                play_result = self.play_highest_domino()

        ## Find another train 
        if not my_train and highest_domino:
            play_result, played_domino, train_num = self.play_highest_domino()
            if play_result == 1:
                print('Played on another train: ', played_domino, ' on train ', train_num)
            else:
                print('Could not play on another train, trying my train')
                play_result = self.play_my_train()
        
        if play_result < 1:
            print('Could not play on another train OR my train...drawing a domino')
            drawn_domino = self.draw()
            print('Drew a domino')
            play_result, played_domino, train_num = self.play_drawn_domino(drawn_domino)
            if play_result == 1:
                print('Played drawn dmoino on train: ', train_num)
            else:
                print('Could not play drawn domino on any train')
            
       
class GamePlay():
    def __init__(self, num_players, round_num):
        self.num_players = num_players
        self.domino_round = 13 - round_num

        start_domino = Domino(self.domino_round, self.domino_round)
        self.pool = []
        for top_num in range(13):
            for bottom_num in range(top_num, 13):
                if top_num == self.domino_round and bottom_num == self.domino_round:
                    continue
                domino_add = Domino(top_num, bottom_num)
                self.pool.append(domino_add)

        random.shuffle(self.pool)

        # Train is a dictionary of tuples with the format (list of dominoes , whether or not in play)
        train_dict = {0: ([start_domino], True)}
        for i in range(num_players):
            player_num = i + 1 
            train_dict[player_num] = ([start_domino], False)
        self.train_dict = train_dict

    def deal_to_one(self, num_dominoes):
        random.shuffle(self.pool)
        deal_dominoes = self.pool[:num_dominoes]
        self.pool = self.pool[num_dominoes:]

        return deal_dominoes

    def deal_to_all(self, num_dominoes):
        deal_lst = []
        for i in range(self.num_players):
            deal_lst.append(self.deal_to_one(num_dominoes))

        # Returns list of list of dominoes 
        return deal_lst

    
class Game():
    def __init__(self, num_players, num_dominoes):
        ## Params
        self.num_players = num_players
        self.current_round = 1
        self.gameplay_round = GamePlay(num_players, self.current_round)
        self.my_player = Player(None, 1)

        ## Gameplay Setup
        my_dominoes = self.gameplay_round.deal_to_one(num_dominoes)

        ## Player Setup 
        self.my_player.join_game(self.gameplay_round)
        self.my_player.add_dominoes(my_dominoes)

        print('--' * 25)
        print('SETUP COMPLETE')
        print('--' * 25)

    def current_state(self):
        print('CURRENT GAME STATUS')
        print('')

        print('Current Round: ', self.current_round)
        print('')
        print('Current Train Statuses: ')
        for train_num in range(1, self.num_players + 1):
            if train_num == self.my_player.player_num:
                print('*MY* Train ', train_num, ' tail: ', self.gameplay_round.train_dict[train_num][0][-1])
            else:
                print('Train ', train_num, ' tail: ', self.gameplay_round.train_dict[train_num][0][-1])

        print('')

        print('My Player')
        print('Dominoes Left :', self.my_player.num_of_dominoes)
        print('--' * 25)

def main():
    game = Game(4, 7)
    game.current_state()

    game.my_player.play_turn()


if __name__ == '__main__':
    main()