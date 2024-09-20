import random

Greetings = list()
Greetings.append(f"hi")
Greetings.append(f"hey")
Greetings.append(f"hello")
Greetings.append(f"howdy")
Greetings.append(f"morning")
Greetings.append(f"hey there")
Greetings.append(f"what's up?")
Greetings.append(f"how's it going?")
Greetings.append(f"nice to see you")
Greetings.append(f"nice to meet you")
Greetings.append(f"salutations")
Greetings.append(f"how do you do?")
Greetings.append(f"greetings")
Greetings.append(f"good day")
Greetings.append(f"hello, explorebgt")
Greetings.append(f"nice to meet you")
Greetings.append(f"pleasure to meet you")
Greetings.append(f"how are you today?")
Greetings.append(f"it's a pleasure to meet you")
Greetings.append(f"hey, friend!")
Greetings.append(f"what's new?")
Greetings.append(f"how's everything?")
Greetings.append(f"nice to see you!")
Greetings.append(f"long time no see!")
Greetings.append(f"how have you been?")


Greetings_Time = list()
Greetings_Time.append(f"good morning")
Greetings_Time.append(f"good afternoon")
Greetings_Time.append(f"good evening")
Greetings_Time.append(f"have a nice evening!")

Greetings_Day = list()
Greetings_Day.append(f"happy monday!")
Greetings_Day.append(f"happy tuesday!")
Greetings_Day.append(f"happy wednesday!")
Greetings_Day.append(f"happy thursday!")
Greetings_Day.append(f"happy friday!")
Greetings_Day.append(f"happy saturday!")
Greetings_Day.append(f"happy sunday!")
Greetings_Day.append(f"have a great day!")
Greetings_Day.append(f"happy new year!")
Greetings_Day.append(f"merry christmas!")
Greetings_Day.append(f"happy holidays!")
Greetings_Day.append(f"happy thanksgiving!")
Greetings_Day.append(f"happy halloween!")
Greetings_Day.append(f"happy easter!")

#______________________________________________________

Reply_Greeting= "Hey! How's it going?, Hi there! What's up?, Hey! What are you up to?, Hello! How may I help you today?, Hey friend! What's new with you?, Hello! How can I brighten your day?, Good day! How may I assist you?, Hello! What's happening?, Sup? Need anything?, Hey there! Got a question?,"

Reply_Greeting = Reply_Greeting.split(',')

Greeting = random.choice(Reply_Greeting)



def Intelligent_Output(user_text):
    
    if user_text in Greetings:
        return Greeting


