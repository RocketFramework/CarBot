import random  # getting acces with random
import time  # getting acess with time

# defineng some_Words. PYTHON RECOGNISES THIS AS ONE SINGLE WORD.
some_Word = "apple,bannana,orange,strawberry,raspberry,melon,lemon,guava,grape,blackberry,blueberry,pineapple,jackfruit,cashew,coconut,dragonfruit,papaya,apricot,mango"

some_Word = some_Word.split(
    ","
)  # Python spilts that single word with the ",". and groups them into groups named arrays. NOW FOR PYTHON IT IS NOT ONE WORD
selectedword = ''
selectedword = random.choice(
    some_Word
)  # python randomly picks up a word from arrays. THIS IS WHY WE INPORTED RANDOM

resultword = "_ " * len(
    selectedword
)  # defines "input_word as ("_" multiplyed by the number of letters in the word)" len is called the number of letters in the word

print(
    "Welcome to the word guessing game!!!"
)  # python prints "Welcome to the word guessing game!!!"
 # python prints "Guess the word, HINT!,IT IS A NAME OF A FRUIT!"
user_input = input("Are you a first time tryer?")
if user_input == "yes" or "YES":
    print("Since this is your first ttime WGG will help you. Here is a hint! Try'",random.choice(selectedword),"' as your first try.GOOD LUCK!!!")
    print(
    "Guess the word, HINT!,IT IS A NAME OF A FRUIT!"
) 
elif user_input == "no" or "NO":
    print("Well then try to see weather you can win alone. GOOD LUCK!!!")
    print(
    "Guess the word, HINT!,IT IS A NAME OF A FRUIT!"
) 
else:
    print("WGG Couldn't understand your response! Please answer YES or NO.")
    
print(resultword)  # python prints the input word which was defined already.


chances = len(selectedword) + 2
entered_result = ''   

while ("_" in resultword) and (
    chances != 0
):  # this command works whenever only when "_" are there in the input word
    guess_input = input(
        "Enter a letter to guess: "
    )  # defines that guess_input is same as the input from the user. NOT WHAT PYTHON SENDS or ask
    chances -= 1
    
    if guess_input in entered_result:
        print("WRONG YOU ALREADY ENTERED IT!!! TRY AGAIN YOU HAVE", chances ,"MORE CHANCES")   

    if (
        len(guess_input) == 1 and guess_input.isalpha()
    ):  # this command works only when the length of guess_input = 1 and guess input is in alphebeticle form
        temp_result = (
            # pyhton creates a variable called result and it has no spesific value.
            ""
        )
        for selected_letter, resulted_letter in zip(
            selectedword, resultword
        ):  # python defines the actual letter an word and guessed letter as resultword. ZIP MEANS THAT IT MAKES MULTIPLE DIGITS INTO A SINGLE DIGIT (the first digit of the word)
            if (
                selected_letter == guess_input
            ):  # in line 20 python created a variable called actual-letter. here it checks weather it is same as guess_input
                temp_result += (
                    guess_input + " "
                )  # python increeses the variable result by (the variable sctual letter + '') so for example if the value of result = a b c d and actual letter was e it changes the result an a b c d e
            elif (
                (resulted_letter != "_") and not (resulted_letter == ' ')
            ):  # this command works only if guessed letter is not = to '_'
                temp_result += (
                    resulted_letter + " "
                )  # python increeses the variable result by (the variable guessed_letter + '') so for example if the value of result = a b c and guess was d it changes the result an a b c d

            # if(resulted_letter != '_':) and (selected_letter == guess_input:) was not true.
            else:
                temp_result += "_ "   # python increeses the variable result by "_"
        print(
            temp_result
        )  # python prints result. HERE IN PRINT WE DONT WRITE AS print("result") if we do so,It will just print the word result. so we write as print(result) so it will print the value of the variable result
        if guess_input in selectedword:
            entered_result += guess_input 
            
        if guess_input in selectedword and guess_input not in entered_result:
            print("Well done you're correct")
      
        resultword = temp_result.replace(
            " ", ""
        )  # this command replaces the value of replaces the value of result by removing all the spaces in it. IT REPLACES RESULT TO ITS ORIGINAL STATE
    # this command says that if (len(guess_input) == 1 and guess_input.isalpha():) was not true.
        entered_result += guess_input 
    else:
        print("Invalid input.")  # python will print "Invalid input."
    if chances == 0 and resultword != selectedword:
        print("YOU ARE FAILED, YOU HAVE 0 MORE CHANCES!")
    if guess_input not in selectedword:
        print("Wrong try again you have", chances ,"more chances")
    elif guess_input not in entered_result:
        print("TRY AGAIN")
        
    if resultword == selectedword:
        
        print("congladuations. YOU PASSED THE WORD GUESSING GAME. YOU ARE LEFT WITH", chances ,"EXTRA CHANCES!!!")


    
    
