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


# A star search algorithm by number_of_misplaced_tiles methd
def A_star_search_with_misplaced(node):
    frontier = PriorityQueue()
    frontier.put((node.get_path_cost() + node.get_method_cost(), node))
    reached = {}
    expand = 0
    
    while (frontier):
        _, current_node = frontier.get()
        expand = expand + 1
        
        if final_state_check (current_node.get_state()):
            return current_node, expand
        children = misplaced_child_node(current_node)
        for i in children:
            # if the node is not expolred, add it into deque 
            if (i not in reached) or (i.get_path_cost() + i.get_method_cost() < reached[i.get_state_str()].get_path_cost() + reached[i.get_state_str()].get_method_cost()):
                reached[i.get_state_str()] = i
                frontier.put((i.get_path_cost() + i.get_method_cost(), i))
                
    return -1, -1

# A star search algorithm by Manhattan_Distance methd
def A_star_search_with_Manhattan_distance(node):
    frontier = PriorityQueue()
    frontier.put((node.get_path_cost() + node.get_method_cost(), node))
    reached = {}
    expand = 0
    
    while (frontier):
        _, current_node = frontier.get()
        expand = expand + 1
        
        if final_state_check (current_node.get_state()):
            return current_node, expand
        children = manha_dist_child_node(current_node)
        for i in children:
            if (i not in reached) or (i.get_path_cost() + i.get_method_cost() < reached[i.get_state_str()].get_path_cost() + reached[i.get_state_str()].get_method_cost()):
                reached[i.get_state_str()] = i
                frontier.put((i.get_path_cost() + i.get_method_cost(), i))
                
    return -1, -1

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
    misplaced_node = Node(state, None, None, 0, number_of_misplaced_tiles (state))        
    
    misplaced_answer = A_star_search_with_misplaced(misplaced_node)
    
    if misplaced_answer == -1:
        print ("Do not have solution")
    else:
        orig_path = move_back_track(misplaced_answer[0])
        orig_path.reverse()
        path = ''
        for i in orig_path:
            path = path + i
            
        print ("Moves: %s" % path)    
        print ("Number of Nodes expanded: %d" % misplaced_answer[1])
        
        
    Manhattan_Distance_node = Node(state, None, None, 0, Manhattan_Distance(state))    
        
    Manhattan_Distance_answer = A_star_search_with_Manhattan_distance(Manhattan_Distance_node)
    
    if Manhattan_Distance_answer == -1:
        print ("Do not have solution")
    else:
        orig_path = move_back_track(Manhattan_Distance_answer[0])
        orig_path.reverse()
        path = ''
        for i in orig_path:
            path = path + i
        print ("Moves: %s" % path)    
        print ("Number of Nodes expanded: %d" % Manhattan_Distance_answer[1])
        
  
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
