import random

characters = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9"
characters = characters.split(' ')

def Generate_API_Key(characters, length=40):
    API_Key = ''.join(random.choice(characters) for _ in range(length))
    return API_Key

API_Key = Generate_API_Key(characters)
print(f"BGT-{API_Key}")

    
