def send_message(s):
    print(s)

def read_message():
    user_input = input()
    return user_input

# Define welcome text
welcome = "Welcome To ChatBot Quizes"
send_message(welcome)

# Define question and answer
# Add more questions to make your chatbot more fun!
trivia_quiz = [
    {
		"question": "How many years are there in a millennium? ",
		"answer": "1000"
    },
    {
		"question": "What is 1000/4",
		"answer": "250"
    },
	{
		"question": "How many years are there in a century? ",
		"answer": "100"
    },
    {
		"question": "What famous ship sank in the year 1912?",
		"answer": "The Titanic"
    },
    {
		"question": "Who painted the Mona Lisa?",
		"answer": "Leonardo da Vinci"
    }
]

count = 0
for t in trivia_quiz:
    send_message(t["question"])
    response = read_message()
    if response == t["answer"]:
        # Define text when the user answer correctly
        send_message("Correct!")
        count += 1
    else:
        # Define text when the user didn't answer correctly
        send_message("Oh You got is wrong the correct answer is%s" % 
                      t["answer"])
 
 # Define text with the number of correct answer     
send_message("Total correct answer count is %d" % count)

# Define text at the end of chat based on how many
# correct answers user got
if count < 2:
    send_message("Good But try to Improving ")
elif count < 4:
    send_message("Well Done!")
else:
    send_message("Great you did it!!")


