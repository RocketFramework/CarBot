import random
import numpy as np
import math

print("The 2048 game is a simple game made by python.")
print("The player has to press one of the commands (w , s , a , d),")
print("In that case the number in that cell goes to the extreem cell in that direction,")
print("while adding up to any number with the same value of it!.")
input("Enter any key to continue: ")
print()  
print("Commands are as follows : ")
print("'W' or 'w' : Move Up")
print("'S' or 's' : Move Down")
print("'A' or 'a' : Move Left")
print("'D' or 'd' : Move Right")
print()
print("Good Luck!!!")
print()


def get_random_integer(min=0, max=3):
    return random.randint(min, max)

def display_board(board):
    for num in board:
        print(num)

def move_up(board): #DONE
    for a in range(4):
        board[0][a] = board[0][a] + board[1][a] + board[2][a] + board[3][a]
    for c in range(1,4):
        board[c] =[0, 0, 0, 0]
    board[get_random_integer(min=1)] [get_random_integer()] = 2
    display_board(board)

def move_down(board): #DONE 
    for i in range(4):
        board[3][i] = board[0][i] + board[1][i] + board[2][i] + board[3][i]
    for k in range(3):
        board[k] =[0, 0, 0, 0]
    board[get_random_integer(max=2)] [get_random_integer()] = 2
    display_board(board)

def move_left(board): #DONE 
    for v in range(4):
        board[v][0] = board[v][0] + board[v][1] + board[v][2] + board[v][3]
    for f in range(4):
        for c in range(1,4):
            board[f][c] = 0
    board[get_random_integer()] [get_random_integer()] = 2
    display_board(board)

def move_right(board): #DONE 
    temp =0
    for i in range(4):
        for j in range(4):
            temp += board[i][j] 
        board[i][3] = temp
        temp = 0
    for z in range(3):
        for h in range(4):
            board[h][z] = 0
    board[get_random_integer()] [get_random_integer()] = 2
    display_board(board)
        
board = [[0 for _ in range(4)] for _ in range(4)] 
board[get_random_integer()] [get_random_integer()] = 2
display_board(board)

keys = ['w', 's', 'a', 'd', 'W', 'S', 'A', 'D']   
key = input("Enter a command: ")

while key in keys:
    if key == 'w' or 'W' == True:
        move_up(board)
        key = input("Enter a command: ")
    elif key == 's' or 'S' == True:
        move_down(board)
        key = input("Enter a command: ")
    elif key == 'a' or 'A' == True:
        move_left(board)
        key = input("Enter a command: ")
    elif key == 'd' or 'D' == True:
        move_right(board)
        key = input("Enter a command: ") 
        
    elif board[0][0] == '2' and board[0][1] == '4' and board[0][2] == '4' and board[0][3] == '8':
        print("YOU WON THE 2048 GAME")
        break   
    elif board[1][0] == '2' and board[1][1] == '4' and board[1][2] == '4' and board[1][3] == '8':
        print("YOU WON THE 2048 GAME")
        break
    elif board[2][0] == '2' and board[2][1] == '4' and board[2][2] == '4' and board[2][3] == '8':
        print("YOU WON THE 2048 GAME")
        break
    elif board[3][0] == '2' and board[3][1] == '4' and board[3][2] == '4' and board[3][3] == '8':
        print("YOU WON THE 2048 GAME")
        break

if key != 'w' or  's' or 'a' or 'd' or 'W' or 'S' or 'A' or 'D':
    print("The command you entered is not valid!")
    print("GAME OVER!!!")
    