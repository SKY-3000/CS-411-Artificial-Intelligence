# Tian Yuan
# UIC: 659401557
# Netid: tyuan7
# Assignment 5: 15 puzzle is a sliding puzzle game with numbered squares arranged in 4X4 grid with one tile missing 
#               by A * search

import time
import psutil
import os
import math
from collections import deque
from queue import PriorityQueue

FOUND = -1
NOT_FOUND = -2
infinity = math.inf
misplaced_method = 1
Manhattan_Distance_method = 2
final_node = None

# board class to make the board and move 0 in the board
class board:
    # initialize board
    def __init__(self, input_list):
        length_list = len(input_list)                   # the length of input list
        self.board_size = int(math.sqrt(length_list))   # the size of the board
        self.list = input_list                          # the board
    
    def get_baord(self):
        return self.list
    
    # move the 0 to up, down, left or right and return a new board
    def move(self, action):
        new_board = self.list[:]
        empty_index = new_board.index('0')
        
        # move to up
        if action == 'U':
            if empty_index - self.board_size >= 0:
                tmp = new_board[empty_index - self.board_size]
                new_board[empty_index - self.board_size] = new_board[empty_index]
                new_board[empty_index] = tmp
                
        # move to down
        if action == 'D':
            if empty_index + self.board_size <= 15:
                tmp = new_board[empty_index + self.board_size]
                new_board[empty_index + self.board_size] = new_board[empty_index]
                new_board[empty_index] = tmp
        
        # move to left
        if action == 'L':
            if empty_index - 1 >= 0:
                tmp = new_board[empty_index - 1]
                new_board[empty_index - 1] = new_board[empty_index]
                new_board[empty_index] = tmp
        
        # move to right
        if action == 'R':
            if empty_index + 1 <= 15:
                # print(empty_index)
                tmp = new_board[empty_index + 1]
                new_board[empty_index + 1] = new_board[empty_index]
                new_board[empty_index] = tmp
        
        # return a new board
        return board(new_board)  
                    
# Node class to svae the state as a node could with parent, action and path_cost
class Node:
    def __init__(self, state, parent, action, path_cost, method_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.method_cost = method_cost
    
    def get_state(self):
        return self.state.list
    
    def get_state_str(self):
        string = ""
        for i in self.state.list:
            string = string + i
        return string
        
    def get_path_cost(self):
        return self.path_cost
    
    def get_method_cost(self):
        return self.method_cost
    
    # set a new way to compare for < operator
    def __lt__(self, other):
        return self.get_method_cost() + self.get_path_cost() < other.get_method_cost() + other.get_path_cost()
    
# to get the expended node and updata the path_cost and method_cost by misplace method
def misplaced_child_node(node):
    children = []
    
    # get new baord and update the parent, action of the node
    up_child_state = node.state.move('U')
    up_child_node = Node(up_child_state, node, 'U', 1 + node.get_path_cost(), number_of_misplaced_tiles(up_child_state))
    children.append(up_child_node)
    
    down_child_state = node.state.move('D')
    down_child_node = Node(down_child_state, node, 'D', 1  + node.get_path_cost(), + number_of_misplaced_tiles(down_child_state))
    children.append(down_child_node)
    
    left_child_state = node.state.move('L')
    left_child_node = Node(left_child_state, node, 'L', 1 + node.get_path_cost(), number_of_misplaced_tiles(left_child_state))
    children.append(left_child_node)
    
    right_child_state = node.state.move('R')
    right_child_node = Node(right_child_state, node, 'R', 1 + node.get_path_cost(), number_of_misplaced_tiles(right_child_state))
    children.append(right_child_node)
    
    return children

# to get the expended node and updata the path_cost and method_cost by manhatton distance method
def manha_dist_child_node(node):
    children = []
    
    # get new baord and update the parent, action of the node
    up_child_state = node.state.move('U')
    up_child_node = Node(up_child_state, node, 'U', 1 + node.get_path_cost(), Manhattan_Distance(up_child_state))
    children.append(up_child_node)
    
    down_child_state = node.state.move('D')
    down_child_node = Node(down_child_state, node, 'D', 1  + node.get_path_cost(), + Manhattan_Distance(down_child_state))
    children.append(down_child_node)
    
    left_child_state = node.state.move('L')
    left_child_node = Node(left_child_state, node, 'L', 1 + node.get_path_cost(), Manhattan_Distance(left_child_state))
    children.append(left_child_node)
    
    right_child_state = node.state.move('R')
    right_child_node = Node(right_child_state, node, 'R', 1 + node.get_path_cost(), Manhattan_Distance(right_child_state))
    children.append(right_child_node)
    
    return children

# the function to check if the state is our goal state
def final_state_check(board):
    final_board = [ '1', '2', '3', '4', 
                    '5', '6', '7', '8', 
                    '9', '10', '11', '12', 
                    '13', '14', '15', '0']
    
    if board == final_board:
        return True
    else:
        return False

# the function to back track the node, and get the path 
def move_back_track(node):	
	move = []
    # when the node still have parent, save the action into list and get the parent node
	while(node.parent):
		move.append(node.action)
		node = node.parent
	return move

# calculate the number of misplaced tiles for the board
def number_of_misplaced_tiles (state):
    board = state.get_baord()
    final_board = [ '1', '2', '3', '4', 
                    '5', '6', '7', '8', 
                    '9', '10', '11', '12', 
                    '13', '14', '15', '0']
    misplaced = 0
    for i in range(16):
        if board[i] == final_board[i]:
            continue
        else:
            misplaced = misplaced + 1
            
    return misplaced
        
# calculate the manhattan distance for the board
def Manhattan_Distance(state):
    board = state.get_baord()
    final_board = [ '1', '2', '3', '4', 
                    '5', '6', '7', '8', 
                    '9', '10', '11', '12', 
                    '13', '14', '15', '0']
    manha_dist= 0
    for i in range(16):
        if board[i] == '0':
            continue
        else:
            if board[i] == final_board[i]:
                continue
            else:
                board_index = board.index(board[i])
                final_index = final_board.index(board[i])
                manha_dist = int(abs(final_index - board_index) / 4 + abs(final_index - board_index) % 4) + manha_dist
    return manha_dist

# call ida_star function to do the Iterative Deepening A * search
def ida_star(root, method):
    # check the method that we use 
    if method == misplaced_method:
        bound = number_of_misplaced_tiles(root.state)
    elif method == Manhattan_Distance_method: 
        bound = Manhattan_Distance(root.state)
    
    # put the root into list to check
    path = [root]
    
    # the number of expand node 
    expand = 0
    
    # the while loop that increase the bound to do the search 
    while 1:
        t, final_path, expand = search(path, 0, bound, method, expand)
        
        # if the function found the solution then return the solution
        if t == FOUND:
            return final_path, expand
        if t == infinity:
            return NOT_FOUND
        bound = t

# the actual search funciton 
def search(path, g, bound, method, expand):
    # to get the node which is the last of the list
    node = path[-1]
    
    # check the method that we use 
    if method == misplaced_method:
        f = g + number_of_misplaced_tiles(node.state)
    elif method == Manhattan_Distance_method:
        f = g + Manhattan_Distance(node.state)
    
    # if f greater than bound, return the f 
    if f > bound:
        return f, None, expand
    
    # check if we achive the goal state
    if final_state_check(node.state.get_baord()):
        final_path = move_back_track(node)
        final_path.reverse()
        return FOUND, final_path, expand
    
    min = infinity
    
   # check the method that we use, then caculate the distance or misplaced of current node 
    if method == misplaced_method:
        children = misplaced_child_node(node)
    elif method == Manhattan_Distance_method:
        children = manha_dist_child_node(node)
    
    # get the children of the current node, and move blank sqaure
    for succ in children:
        # expand one more node
        expand = expand + 1
        # if path do not have the succ, add it into path list and do the search function
        if succ not in path:
            path.append(succ)
            t, final_path, expand = search(path, g + 1, bound, method, expand)
            if t == FOUND:
                return FOUND, final_path, expand
            if t < min:
                min = t
            path.pop()
            
    return min, None, expand

# main function: take input and return the output
def main():
    # get the started memory 
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024
    
    # start excution time
    start_time = time.time()

    # start to get input , and split it to a list
    input_number = input("Input: ")
    input_number_list = input_number.split();
    
    # make the input list into board
    state = board(input_number_list)
    
    # create the node for the board
    node = Node(state, None, None, 0, 0)      

    # choose which method we want to use
    method_call = misplaced_method
    # method_call = Manhattan_Distance_method
    
    # to call the ids * search fucntion
    result = ida_star(node, method_call)
    
    # print the moves and the node the function expanded
    if result[0] == NOT_FOUND:
        print("NOT FOUND")
    else:
        orig_path = result[0]
        path = ''
        for i in orig_path:
             path = path + i
        print("Moves: %s" % path)
        print ("Number of Nodes expanded: %d" % result[1])
  
    # end excution time and print
    end = time.time()
    print("Time Taken: %s " % (end - start_time))
    
    # get the end memory 
    end_memory = process.memory_info().rss / 1024
    
    # get the momeory used and print 
    print("Memory Used: %d kb" % (end_memory - start_memory))
    
# call main function
if __name__ == "__main__":
    main()
