# Tian Yuan
# UIC: 659401557
# Netid: tyuan7
# Assignment 4: 15 puzzle is a sliding puzzle game with numbered squares arranged in 4X4 grid with one tile missing 
#               by iterative deepening depth first search

import time
import psutil
import os
import math
from collections import deque

# board class to make the board and move 0 in the board
class board:
    # initialize board
    def __init__(self, input_list):
        length_list = len(input_list)                   # the length of input list
        self.board_size = int(math.sqrt(length_list))   # the size of the board
        self.list = input_list                          # the board
    
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
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
    
    def get_state(self):
        return self.state.list
        
# to get the expended node of the 0
def child_node(node):
    children = []
    
    # get new baord and update the parent, action of the node
    up_child_state = node.state.move('U')
    up_child_node = Node(up_child_state, node, 'U', None)
    children.append(up_child_node)
    
    down_child_state = node.state.move('D')
    down_child_node = Node(down_child_state, node, 'D', None)
    children.append(down_child_node)
    
    left_child_state = node.state.move('L')
    left_child_node = Node(left_child_state, node, 'L', None)
    children.append(left_child_node)
    
    right_child_state = node.state.move('R')
    right_child_node = Node(right_child_state, node, 'R', None)
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

# iterative deepening Search
def ids(node, depth, reached, expand):
    # set the cutoff value
    cutoff_occurred = False
    # add the node into reached set make sure we will not reach it again
    reached.add(node)
    
    # check if we reach the goal state
    if final_state_check (node.get_state()):
        return node
    
    # if depth reach the limit, return cutoff
    elif depth == 0 :
        return 0
    
    # get next level
    else:
        expand = expand + 1
        depth = depth - 1
        children = child_node(node)
        # check children node
        for i in children :
            # make sure we will not reach repeated node 
            if i not in reached :
                result = ids(i, depth, reached, expand)
                
                # if we reach the last node, it is cutoff
                if result == 0:
                    cutoff_occurred = True
                elif result != -1:
                    return result
    # if cutoff occurred return cutoff
    if cutoff_occurred == True :
        return 0
    # esle return failure
    else:
        return -1

# iterative deepening depth first search
def iddfs(node):
    reached = set()
    depth = 0
    expand = 0
    # main loop for depth
    while True:
        result = ids(node, depth, reached, expand)
        
        # if it is neither failure or cutoff, we good
        if (result != -1) and (result != 0) :
            path = move_back_track(result)
            path.reverse()
            return path, len(reached)

        depth = depth + 1

    
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
    node = Node(state, None, None, None)
    
    # get the moves and number of nodes expanded
    answer = iddfs(node)
    
    # print moves and number of nodes expanded
    path = ''
    for i in answer[0]:
        path = path + i
        
    print ("Moves: %s" % path)    
    print ("Number of Nodes expanded: %d" % answer[1])
  
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
