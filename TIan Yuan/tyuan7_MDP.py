import random
from collections import defaultdict
import numpy as np

class mdp_board:
    def __init__(self, row, colums, wall_string, terminal_states_string):
        self.row = row
        self.colums = colums
        self.list = [1, 2, 3, 4]
        self.board = [[ 0 for x in range(colums)] for y in range(row)]
        wall_temp = wall_string.split()
        wall = []
        for i in wall_temp:
            if i != ',':
                wall.append(int(i))

        while (wall):
            x = wall.pop(0)
            y = wall.pop(0)
            self.board[4-y][x-1 ] = '-'
        
        terminal_states_temp = terminal_states_string.split()
        terminal_states = []
        for i in terminal_states_temp:
            if i != ',':
                terminal_states.append(int(i))
        
        while (terminal_states):
            x = terminal_states.pop(0)
            y = terminal_states.pop(0)
            z = terminal_states.pop(0)
            self.board[4-y][x-1] = z
        

    def state_move (self, state, action):
        if state == '-':
            return state
        i = 0
        j = 0
        for i in range(self.row):
            for j in range(self.colums):
                if self.board[i][j] == state:
                    break;
                    
        if action == 'U':
             if i > 0:
                 return i - 1, j
        if action == 'R':
            if j < self.colums - 1:
                return i, j + 1
        if action == 'L':
            if j > 0:
                return i, j - 1
        if action == 'D':
            if i < self.row - 1:
                return i + 1, j
                
        
    def print_board(self):
        for x in range(self.row):
            for y in range(self.colums):
                print(self.board[x][y], end =" ")
            print("")
            

class mdp_class:
    def __init__(self, board, actions, transition_probabilities_string, reward_string, discount_rate_string):
        self.board = board
        self.actions = actions
        
        transition_probabilities_string = transition_probabilities_string.split()
        self.transition = []
        for i in range(4):
            self.transition.append(float(transition_probabilities_string[i]))
         
        self.reward = float(reward_string)
        self.reward_board = [[ 0 for x in range(self.board.colums)] for y in range(self.board.row)]
        for i in range(self.board.row):
            for j in range(self.board.colums):
                if self.board.board[i][j] == 0:
                    self.reward_board[i][j] = self.reward
                else:
                    self.reward_board[i][j] = self.board.board[i][j]
                    
        self.gamma = float(discount_rate_string)
        
        
    
    def R(self, state):
        for i in range(self.board.row):
            for j in range(self.board.colums):
                if self.board.board[i][j] == state:
                    return self.reward_board[i][j]
    
    def T(self, state, action):
        if action == 'U':
            return self.transition[0], self.board.state_move(state, action)
        
        if action == 'R':
            return self.transition[1], self.board.state_move(state, action)
        
        if action == 'L':
            return self.transition[2], self.board.state_move(state, action)
        
        if action == 'D':
            return self.transition[3], self.board.state_move(state, action)
    
    def actions(self, state):
        x, y = state
        if self.board[x][y] == '-':
            return [None]
        else:
            return ['U', 'R', 'L', 'D']
        
    def duplication(self):
        new_board = [[ 0 for x in range(self.board.colums)] for y in range(self.board.colums)]
        for i in range(self.board.row):
            for j in range(self.board.colums):
                new_board[i][j] = self.board.board[i][j]
        
        return new_board
        
def value_iteration(mdp, epsilon):
    U = mdp.duplication()

    while 1:
        U1 = U.copy()
        delta = 0
        for s in mdp.board.board:
            for a in mdp.actions(s):
                for (p, s1) in mdp.T(s, a):
                    U1[s]
            

        if delta <= epsilon * (1 - mdp.gamma) / mdp.gamma:
            return U    



def main():
    with open("mdp_input.txt", "r") as file:
        lines = file.read()
        
        test = lines.split(":")[1].strip()
        size_string = test[: test.find('\n')]
            
        test = lines.split(":")[2].strip()
        wall_string = test[: test.find('\n')]
        
        test = lines.split(":")[3].strip()
        terminal_states_string = test[: test.find('\n')]
        
        test = lines.split(":")[4].strip()
        reward_string = test[: test.find('\n')]
        
        test = lines.split(":")[5].strip()
        transition_probabilities_string = test[: test.find('\n')]
        
        test = lines.split(":")[6].strip()
        discount_rate_string = test[: test.find('\n')]
        
        test = lines.split(":")[7].strip()
        epsilon_string = test[:]
        

        print("(" + size_string[0] + ", " + size_string[2] + ", ", end = "")
        print("[", end = "")
        wall_temp = wall_string.split()
        xy = 0
        for i in wall_temp:
            if i != ',':
                
                if xy%2 == 0:
                    print ("x= " + i, end = " ")
                    xy = xy + 1
                elif xy%2 == 1:
                    if i == wall_temp[-1]:
                        print ("y= " + i, end = "")
                    else: 
                        print ("y= " + i + ", ", end = "")
                    xy = xy + 1
        print ("], {", end = "")
        
        terminal_states_temp = terminal_states_string.split()
        terminal_states_temp.reverse()
        xyz = 0
        while xyz < len(terminal_states_temp) - 1:
            if terminal_states_temp[xyz] != ',':
                print ("x= " + terminal_states_temp[xyz+2], end = " ")
                print ("y= " + terminal_states_temp[xyz+1], end = "")
                z = float(terminal_states_temp[xyz])
                z = str(z)
                if terminal_states_temp[xyz + 2] == terminal_states_temp[-1]:
                    print (": " + z + "}, ", end = "")
                else: 
                    print (": " + z + ",", end = " ")
                xyz = xyz + 3
            xyz = xyz + 1
        
        print (reward_string + ", ", end = "")
        
        print ("'" + transition_probabilities_string + "', ", end = "")
        
        print (discount_rate_string + ",", end = " ")
        
        print (epsilon_string + ")")
        
        print ("################ VALUE ITERATION ###########################")
        print ("")
        
        board =  mdp_board(int(size_string[2]), int(size_string[0]), wall_string, terminal_states_string)
        mdp = mdp_class(board, ['U', 'R', 'L', 'D'], transition_probabilities_string, reward_string, discount_rate_string)
        
        epsilon = float(epsilon_string)
        
        value_iteration(mdp, epsilon)
        
        
        # board.print_board()

if __name__ == "__main__":
    main()
    