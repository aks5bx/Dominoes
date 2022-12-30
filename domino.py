import pandas as pd 
import numpy as np 
import random 
import networkx as nx 

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
        return '[' + str(self.top) + ' | ' + str(self.bottom) + ']'
    
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

    def info(self, all_dominoes=False, verbose=False):
        d_lst = self.domino_list

        if all_dominoes and verbose:
            print('My Dominoes: ')
            for d in d_lst:
                print(d)
            print('--' * 25)

        elif not all_dominoes and verbose:
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
        elif self.game.train_dict[train_num][0][-1].bottom != play_domino.top:
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
                self.game.train_dict[train_num] = (self.game.train_dict[train_num][0], False)

            return 1 

        else:
            return 0 

    def draw(self):
        new_dominoes_lst = self.game.deal_to_one(1)

        if len(new_dominoes_lst) == 0:
            return None 

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

        G = nx.DiGraph()
        start_domino = self.game.train_dict[self.player_num][0][-1]
        
        dominoes = [start_domino] + dominoes

        # Create a graph where each domino is a node, and edges connect dominoes that can be chained together
        for domino in dominoes:
            other_dominoes = [d for d in dominoes if d != domino]
            for other in other_dominoes:
                if domino.bottom == other.top:
                    G.add_edge(domino, other, weight=1)

        cycles = nx.simple_cycles(G)
        longest_cycle = []

        for cycle in iter(cycles):
            ## A train cycle only counts if the start of the cycle is the train start domino
            if cycle[0].top == start_domino.top and cycle[0].bottom == start_domino.bottom:
                if len(cycle) > len(longest_cycle):
                    longest_cycle = cycle
        
        dominoes = dominoes[1:]
        if len(longest_cycle) > 0: 
            longest_cycle = longest_cycle[1:]
        else:
            train_domino = None
            for domino in dominoes:
                if domino.top == start_domino.bottom and (train_domino is None or domino.total > train_domino.total):
                    train_domino = domino
            
            if train_domino is not None:
                longest_cycle = [train_domino]
                    
        self.train_queue = longest_cycle
        print('Longest Cycle : ', longest_cycle)
        return longest_cycle

    def play_my_train(self):
        train_num = self.player_num
        play_domino = self.train_queue.pop(0)

        play_attempt = self.play_domino(play_domino, train_num)

        return play_attempt, play_domino

    def play_highest_domino(self):
        sorted_dominoes = self.sort_dominoes()
        for big_domino in sorted_dominoes:
            for train_num in range(0, self.game.num_players + 1):
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
        for train_num in range(0, self.game.num_players + 1):
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


    def play_turn(self, my_train = True, highest_domino = False, CPU = False):
        print('')
        print('--' * 25)
        print('--' * 25)
        if not CPU:
            print('MY TURN')
        else:
            print('CPU ', self.player_num, ' TURN')
        print('')

        print('>>>> Start Turn: My Dominoes <<<<')
        print(self.domino_list)
        print('')

        play_result = -1

        self.make_train(self.domino_list)

        ## Priority is to play on your own train
        if my_train and len(self.train_queue) > 0: 
            attempt1, play_domino = self.play_my_train()
            if attempt1 == 1:
                play_result = 1
                print('Played ', play_domino, ' on my train')
        elif my_train:
            print('Could not play my train, trying another train')
            play_result, played_domino , played_train = self.play_highest_domino()
            if play_result == 1:
                print('Played on another train: ', played_domino, ' on train ', played_train)

        ## Priority is to play on another train
        if (not my_train) and highest_domino:
            play_result, played_domino, train_num = self.play_highest_domino()
            if play_result == 1:
                print('Played on another train: ', played_domino, ' on train ', train_num)
            else:
                print('Could not play on another train, trying my train')
                play_result = self.play_my_train()

        if play_result < 1:
            print('Could not play on another train OR my train...drawing a domino')
            drawn_domino = self.draw()
            if drawn_domino is not None:
                print('Drew a domino ', drawn_domino)
                play_result, played_domino, train_num = self.play_drawn_domino(drawn_domino)
                if play_result == 1:
                    print('Played drawn domino on train: ', train_num)
                else:
                    print('')
                    print('Could not play drawn domino on any train - setting it to public')
                    self.game.train_dict[self.player_num] = (self.game.train_dict[self.player_num][0], True)
            else:
                print('No more dominoes to draw...passing turn')

        print('')
        print('TURN COMPLETE')
        print('')
        print('>>>> End Turn: My Dominoes <<<<')
        print(len(self.domino_list))
        print('--' * 25)   
        print('--' * 25)

        if len(self.domino_list) == 0:
            print('Player ', self.player_num, ' has won the round!')
            return 1
        else:
            return 0 

       
class GamePlay():
    def __init__(self, num_players, round_num):
        self.num_players = num_players
        self.domino_round = 13 - round_num

        self.start_domino = Domino(self.domino_round, self.domino_round)
        self.pool = []
        for top_num in range(13):
            for bottom_num in range(13):
                if top_num == self.domino_round and bottom_num == self.domino_round:
                    continue
                domino_add = Domino(top_num, bottom_num)
                self.pool.append(domino_add)

        random.shuffle(self.pool)

        # Train is a dictionary of tuples with the format (list of dominoes , whether or not in play)
        train_dict = {0: ([self.start_domino], True)}
        for i in range(num_players):
            player_num = i + 1 
            train_dict[player_num] = ([self.start_domino], False)
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
    def __init__(self, num_players, num_dominoes, current_round=1):
        ## Params
        self.nd = num_dominoes
        self.num_players = num_players
        self.current_round = current_round
        self.gameplay_round = GamePlay(num_players, self.current_round)
        self.my_player = Player(None, 1)
        self.players = {1 : self.my_player}
        self.score_dict = {1: 0}
        ## Gameplay Setup
        my_dominoes = self.gameplay_round.deal_to_one(num_dominoes)

        ## Player Setup 
        self.my_player.join_game(self.gameplay_round)
        self.my_player.add_dominoes(my_dominoes)

        print('--' * 25)
        print('SETUP COMPLETE')
        print('--' * 25)

    def add_CPU(self, player_num):
        if len(self.players.keys()) == self.num_players:
            print('Max players reached')
            return

        player = Player(None, player_num)
        player.join_game(self.gameplay_round)
        player.add_dominoes(self.gameplay_round.deal_to_one(self.nd))
        self.players[player_num] = player
        self.score_dict[player_num] = 0

        print('Added Player ', player_num, ' to the game')

    def make_turn_CPUs(self):
        for player_num in self.players.keys():
            if player_num == 1:
                continue
            else:
                result = self.players[player_num].play_turn(CPU=True)
                if result == 1:
                    print('Player ', player_num, ' has won the round!')
                    return 1

        return 0         

    def play_round(self):
        keep_playing = True 
        while keep_playing: 
            result = self.my_player.play_turn()
            if result == 1:
                keep_playing = False
            else:
                result = self.make_turn_CPUs()
                if result == 1:
                    keep_playing = False
            
            self.current_state(True)


    def next_round(self):
        self.current_round += 1
        self.gameplay_round = GamePlay(self.num_players, self.current_round)
        for player_num in self.players.keys():
            self.players[player_num].join_game(self.gameplay_round)
            self.players[player_num].add_dominoes(self.gameplay_round.deal_to_one(self.nd))

    def score(self, show = True):
        for player_num in self.score_dict.keys():            
            dominoes_left = self.players[player_num].domino_list
            points_left = 0
            for domino in dominoes_left:
                points_left += domino.total

            self.score_dict[player_num] += points_left 

        if show:
            print('SCORES')
            for player_num in self.score_dict.keys():
                print('Player ', player_num, ' : ', self.score_dict[player_num])

        return self.score_dict[1]

    def current_state(self, trains = False):
        print('')
        print('--' * 25)
        print('--' * 25)
        print('CURRENT GAME STATUS')
        print('')

        print('Current Round: ', self.current_round)
        print('')
        if trains:
            print('Current Train Statuses: ')
            for train_num in range(0, self.num_players + 1):
                if train_num == self.my_player.player_num:
                    print('*MY* Train ', train_num, ' tail: ', self.gameplay_round.train_dict[train_num][0][-1])
                else:
                    print('Train ', train_num, ' tail: ', self.gameplay_round.train_dict[train_num][0][-1])

            print('')

        print('My Player')
        print('Dominoes Left :', len(self.my_player.domino_list))
        print('--' * 25)
        print('--' * 25)

def pipeline():
    game = Game(4, 12)
    game.add_CPU(2)
    game.add_CPU(3)
    game.add_CPU(4) 

    game.play_round()
    my_score = game.score()

    return my_score


def main():
    game = Game(6, 12)
    game.add_CPU(2)
    game.add_CPU(3)
    game.add_CPU(4)
    game.add_CPU(5)
    game.add_CPU(6)
    game.current_state(trains = True)
    game.play_round()
    my_score = game.score()


if __name__ == '__main__':
    main()