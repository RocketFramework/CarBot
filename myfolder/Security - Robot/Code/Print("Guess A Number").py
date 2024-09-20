import math
import time

print("Welcome to B Number Quiz")

lower_bound = input("Enter Lower bound: ")
upper_bound = input("Enter Upper bound: ")

lower = int(lower_bound)
upper = int(upper_bound)


chances = (upper - lower)

print(f"you got {chances} chances to win the quiz")
time.sleep(1)

print("INSTRUCTIONS...")
print("You have to guess a number.B Number Quiz Will Provide "\
      "Accurate Detaills Weather the number is high or low."f"You got {chances} chances to win this B Quiz!")

guess_question = input("Guess your first number: ")

answer = upper - 1


guess = int(guess_question)
if guess == answer:
    print("YOU DID IT!!!")
            
elif guess > (1 + answer): 
    print("You are High!")
    
            
elif guess > answer:
    print("you are high")
            
elif guess < (answer - 1):
    print("You are too low!")
    
            
else:
    print("You are low!")
    
   
        
        
        
        
if guess == answer: 
    stopall()       

if chances > 2:
    print(f"WRONG! Try with this chance you got {chances - 1 } more chances to win the quiz")
    chances -= 1
    input("Guess your number: ")

#START    
if guess == answer:
    print("YOU DID IT!!!")
            
elif guess > (1 + answer): 
    print("You are High!")
   
            
elif guess > answer:
    print("you are high")
            
elif guess < (answer - 1):
    print("You are too low!")
    
            
else:
    print("You are low!")
    
#ENDING    
        
if chances == 1: 
    print(f"WRONG! Try with this chance you got {chances} more chances to win the quiz")
   
    input("Guess your number: ")
    
    
    #START    
if guess == answer:
    print("YOU DID IT!!!")
            
elif guess > (1 + answer): 
    print("You are High!")
    
            
elif guess > answer:
    print("you are high")
            
elif guess < (answer - 1):
    print("You are too low!")
    
            
else:
    print("You are low!")
   
#ENDING  


if chances == 0:
    print("YOU FAILED!!!")





 