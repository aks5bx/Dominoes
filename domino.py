import pandas as pd 
import numpy as np 
import torch 

class Domino():
    def __init__(self, top, bottom):
        self.top = top 
        self.bottom = bottom 

        if top == bottom:
            self.double = True
    
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
    def __init__(self, domino_lst=None, domino_df=None, player_num=1):
        if domino_lst is not None:
            self.num_of_dominoes = len(domino_lst)
            df = pd.DataFrame(np.zeros((self.num_of_dominoes, 3)), columns=['top','bottom', 'double'])

            for i in range(self.num_of_dominoes):
                df.loc[i:i,'top':'double']= domino_lst[i][0], domino_lst[i][1], domino_lst[i][0] == domino_lst[i][1]

            self.domino_df = df

        if domino_df is not None:
            self.domino_df = domino_df
            self.num_of_dominoes = len(domino_df)
        
        self.game = None 
        self.player_num = player_num

    def info(self):
        df = self.domino_df
        print('--' * 25)   
        print('Number of dominoes: ', self.num_of_dominoes)
        print('Number of doubles: ', df['double'].sum())
        print('FULL DATAFRAME: ')
        print(self.domino_df)
        print('--' * 25)   

    def join_game(self, gameplay):
        self.game = gameplay
    
    def valid_play(self, play_domino, train_num):
        if self.game.train_dict[train_num][1] == False and self.player_num != train_num:
            return False
        elif self.game.train_dict[train_num][0][-1][1] != play_domino.top:
            return False 
        else:
            return True 
    
    def play(self, play_domino, train_num):
        if self.valid_play(play_domino, train_num):
            self.game.train_dict[train_num][0].append((play_domino.top, play_domino.bottom))
            self.domino_df.drop(self.domino_df[(self.domino_df.top == play_domino.top) & (self.domino_df.bottom == play_domino.bottom)].index, inplace=True)
            self.num_of_dominoes -= 1

            if self.player_num == train_num:
                self.game.train_dict[train_num][1] = False

        else:
            print('Invalid play')

    def draw(self):
        new_domino = self.game.deal_to_one(1)
        new_top = new_domino['top'].values[0]
        new_bottom = new_domino['bottom'].values[0]
        new_double = new_domino['double'].values[0]

    def build_my_train(self):
        # Either longest train or train with most total points 

    def strategize(self, my_train = True, highest_domino = False):
        if my_train and len(self.train_queue) > 0: 
            train_num = self.player_num

       







class GamePlay():
    def __init__(self, num_players, round_num):
        self.num_players = num_players
        self.domino_round = 13 - round_num

        zero_to_12 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
        top_nums = []
        bottom_nums = []
        for i in range(13):
            top_nums += [i] * (13 - i)
            bottom_nums += zero_to_12[i:]

        pool_df = pd.DataFrame({'top': top_nums,'bottom': bottom_nums})
        pool_df['double'] = pool_df['top'] == pool_df['bottom']
        pool_df.drop(pool_df[(pool_df.top == self.domino_round) & (pool_df.bottom == self.domino_round)].index, inplace=True)
        self.pool = pool_df.sample(frac = 1)

        # Train is a dictionary of tuples (dominoes (top,bottom), whether or not they are in play)
        train_dict = {0: ([(self.domino_round, self.domino_round)], True)}
        for i in range(num_players):
            player_num = i + 1 
            train_dict[player_num] = ([(self.domino_round, self.domino_round)], False)
        self.train_dict = train_dict

    def deal_to_one(self, num_dominoes):
        deal_df = self.pool.iloc[:num_dominoes]
        self.pool = self.pool.iloc[num_dominoes:]

        return deal_df

    def deal_to_all(self, num_dominoes):
        deal_lst = []
        for i in range(self.num_players):
            deal_lst.append(self.deal_to_one(num_dominoes))

        # Returns list of dataframes
        return deal_lst

    




def main():
    domino = Domino(2, 3)
    domino.visualize()

if __name__ == '__main__':
    main()