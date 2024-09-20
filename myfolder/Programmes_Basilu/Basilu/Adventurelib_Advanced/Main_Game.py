"""Complete Game Written In Adventurelib
   by Basilu Liyanage,
   Module: Main-Gaame
"""

import adventurelib as adl

import Game_Rooms

import Game_Items

from random import randint

import sys


present_location = Game_Rooms.home
present_location.visited = False

hit_points = 20
giant_hit_points = 50

inventory = adl.Bag()

@adl.when("inventory")
@adl.when("inventor")
@adl.when("invento")
@adl.when("invent")
@adl.when("inven")
@adl.when("inve")
@adl.when("inv")
@adl.when("in")
@adl.when("i")
def list_inventory():
    
    if inventory:
        print("You have the following items with you:")
        for item in inventory:
            print(f"  - {item.description}")
    else:
        print("Unfortunately, You have nothing in your inventory.")
        
@adl.when("look at ITEM")
def look_at(item: str):
    
    global inventory, present_location
    
    obj = present_location.items.find(item)
    
    if not obj:
        obj = inventory.find(item)
        
        if not obj:
            print(f"You Don't have {item} anywhere.")
            
        else:
            print(f"You've Got {item} with You.")
            
    else:
        print(f"You see {item}.")
        
@adl.when("describe ITEM")
def describe(item: str):
    
    global inventory, present_location
    
    obj = current_room.items.find(item)
    
    if not obj:
        obj = inventory.find(item)
        
        if not obj:
            print(f"Unfortunately, You havent got the {item} anywhere.")
            
        else:
            print(f"Luckly, You have {obj.description}.")
            
    else:
        print(f"You see {obj.description}.")
        
@adl.when("take ITEM")
@adl.when("get ITEM")
@adl.when("pickup ITEM")
@adl.when("pick up ITEM")
@adl.when("grab ITEM")
def take_item(item: str):
    
    global present_location
    
    obj = present_location.items.take(item)
    
    if not obj:
        print(f"You don't Have {item} here.")
        
    else:
        print(f"Now You have {obj.description}.")
        inventory.add(obj)
        
@adl.when("eat ITEM")
def eat(item: str):
    
    global inventory
    
    obj = inventory.find(item)
    
    if not obj:
        print(f"You don't have {item}.")
        
    elif obj.edible:
        print(f"You love every bite of {obj.description}.")
        inventory.take(item)
        
    else:
        print(f"How should we go about consuming {obj.description}?")
        
@adl.when("wear ITEM")
@adl.when("put on ITEM")
@adl.when("dress up ITEM")
@adl.when("dress ITEM")
def wear(item: str):
    
    global inventory
    
    obj = inventory.find(item)
    
    if not obj:
        print(f"You don't have {item}.")
        
    elif obj.wearable:
        print(f"The {obj.description} makes a wonderful adventurus look!")

    else:
        print(
            f"""
            This is no time for avant garde adventure dress choices!
            Wear a {obj.description}? Really?
            """)
        
        
@adl.when("talk to CHARACTER")
@adl.when("talk with CHARACTER")
def talk_to(character: str):
    
    global present_location
    
    char = present_location.characters.find(character)
    
    if not char:
        print(f"Sorry, {character} was not found.")


    else:

        adl.set_context(char.context)
        adl.say(char.greeting)
        
@adl.when("yes", context="counsellor")

def yes_elder():
    
    global present_location
    
    adl.say("""
    It is not often one of our number leaves, and rarer still if they leave
    to defend our Home. Go with our blessing, and our hope for a successful
    journey and speedy return. To help, we bestow three gifts.

    The first is one of knowledge. There is a blacksmith in one of the
    neighboring villages. You may find help there.

    Second, seek a wizard who lives as a hermit, who may be persuaded to
    give aid. Be wary, though! The wizard does not give away his aid for
    free. As he tests you, remember always where you started your journey.

    Lastly, we don't know what dangers you may face. We are peaceful people,
    but do not wish you to go into the world undefended. Take this meager
    offering, and use it well! Good Luck
    """)
    
    inventory.add(Game_Items.wooden_sword)
    present_location.locked_exits["south"] = False
    
@adl.when("thank you", context="counsellor")
@adl.when("thanks", context="counsellor")
def thank_elder():
    adl.say("It is we who should thank you. Go with our love and hopes!")
    
    
@adl.when("yes", context="blacksmith")
def yes_blacksmith():
    
    global present_location
    
    adl.say("""
        I can see you've not a lot of money. Usually, everything here
        if pretty expensive, but I just might have something...

        There's this steel sword here, if you want it. Don't worry --- it
        doesn't cost anything! It was dropped off for repair a few weeks
        ago, but the person never came back for it. It's clean, sharp,
        well-oiled, and will do a lot more damage than that
        fancy sword-shaped club you've got. I need it gone to clear some room.

        If you want, we could trade even up --- the wooden sword for the
        steel one. I can use yours for fire-starter. Sounds Like A Deal?
        """)
    adl.set_context("blacksmith.trade")
    
@adl.when("yes", context="blacksmith.trade")
def trade_swords_yes():
    
    print("Great!")
    inventory.take("wooden sword")
    inventory.add(Game_Items.steel_sword)
    
    
@adl.when("no", context="blacksmith.trade")
def trade_swords_no():
    print("Well, that's all I have within your budget for free. Good luck!")
    adl.set_context(None)
    
    
@adl.when("yes", context="wizard")
def yes_wizard():
    
    global current_room

    adl.say(
        """
    I can make your weapon more powerful than it is, but only if
    you can answer my riddle:

     I’m full of holes....
     but strong as steel....
     What am I?.... 
    """
    )
    
    adl.set_context("wizard.riddle")

@adl.when("chain", context="wizard.riddle")
@adl.when("a chain", context="wizard.riddle")
@adl.when("a steel chain", context="wizard.riddle")
@adl.when("steel chain", context="wizard.riddle")
def answer_riddle():
    
    adl.say("You are smarter than you believe yourself to be! Behold!")
    
    obj = inventory.find("sword")
    obj.bonus = 2
    obj.description += ", which glows with eldritch light"
    
    adl.set_context(None)
    present_location.locked_exits["west"] = False
    
@adl.when("fight CHARACTER", context="giant")
def fight_giant(character: str):
    
    global giant_hit_points, hit_points

    sword = inventory.find("sword")
    
    player_attack = randint(1, sword.damage + 1) + sword.bonus
    print(f"You swing your {sword}, as Fast as you can doing {player_attack} damage!")
    
    giant_hit_points -= player_attack
    
    if giant_hit_points <= 0:
        end_game(victory=True)
        
    print_giant_condition()
    print()
    
    
    giant_attack = randint(0, 5)
    
    if giant_attack == 0:
        print("Luckly The giant's arm whistles harmlessly over your head!")
        
    else:
        print(
            f"""
            The giant swings his mighty fist,
            and does {giant_attack} damage!
            """
        )
        hit_points -= giant_attack
        
        
    if hit_points <= 0:
        end_game(victory=False)

    print_player_condition()
    print()


def print_giant_condition():

    if giant_hit_points < 10:
        print("The giant staggers, his eyes unfocused.")
    elif giant_hit_points < 20:
        print("The giant's steps become more unsteady.")
    elif giant_hit_points < 30:
        print("The giant sweats and wipes the blood from his brow.")
    elif giant_hit_points < 40:
        print("The giant snorts and grits his teeth against the pain.")
    else:
        print("The giant smiles and readies himself for the attack")
        
        
def print_player_condition():
    
    if hit_points < 4:
        print("Your eyes lose focus on the giant as you sway unsteadily.")
    elif hit_points < 8:
        print("""
            Your footing becomes less steady
            as you swing your sword sloppily.
            """)
        
    elif hit_points < 12:
        print("""
            Blood mixes with sweat on your face
            as you wipe it from your eyes.
            """)
        
    elif hit_points < 16:
        print("You bite down as the pain begins to make itself felt. Good Luck for the fight.")
        
    else:
        print("You charge into the fray valiantly!")
        
        
def end_game(victory: bool):
    
    if victory:
        adl.say("""
        The giant collapses to his knees as the last of his strength drains away.
        With a final, desperate swing, he lunges at you, but you deftly dodge the blow.
        His momentum carries him forward, and he crashes face down into the dirt.
        His last breath escapes his lips as he succumbs to your attack.
        You are victorious! Your name will be sung for generations!
        """)
        
    else:
        adl.say("""
        The giant's mighty fist slams into your head, and the final sound you hear is the sickening crunch of bones in your neck.
        You spin and tumble to the ground, your sword clattering away as the giant's laughter fills the air. 
        Through fading vision, you see the giant step toward you, his massive foot poised to crush you.

        Oblivion claims you before you can feel anything more...

        You have been defeated! The giant is free to ravage your town!
        """)
        
@adl.when("flee", context="giant")
def flee():
    adl.say("""
    As you turn to run, the giant reaches out and catches your tunic.
    He lifts you off the ground, grabbing your dangling sword-arm
    as he does so. A quick twist, and your sword tumbles to the ground.
    Still holding you, he reaches his hand to your throat and squeezes,
    cutting off your air supply.

    The last sight you see before blackness takes you are
    the rotten teeth of the evil grin as the giant laughs
    at your puny attempt to stop him...

    You have been defeated! The giant is free to ravage your town!
    """)
    
    sys.exit()
    
@adl.when("goodbye")
@adl.when("bye")
@adl.when("adios")
@adl.when("later")
def goodbye():


    if adl.get_context() == "giant":

        print("No! The giant steps in front of you, blocking your exit!")

    else:

        adl.set_context(None)
        print("Fare thee well, traveler!")

@adl.when("look")
def look():
    
    global present_location
    
    if not present_location.visited:
        adl.say(present_location)
        present_location.visited = True
        
    else:
        print(present_location.short_desc)


    for item in present_location.items:
        print(f"There is {item.description} here.")
        
@adl.when("describe")
def describe_room():
    
    adl.say(present_location)
    
    for item in present_location.items:
        print(f"There is {item.description} here.")
        

@adl.when("go DIRECTION")
@adl.when("north", direction="north")
@adl.when("south", direction="south")
@adl.when("east", direction="east")
@adl.when("west", direction="west")
@adl.when("n", direction="north")
@adl.when("s", direction="south")
@adl.when("e", direction="east")
@adl.when("w", direction="west")
def go(direction: str):
    
    global present_location
    
    next_room = present_location.exit(direction)
    
    if next_room:

        if (direction in present_location.locked_exits and present_location.locked_exits[direction]):
            print(f"You can't go {direction} --- the door is locked.")
            
        else:
            current_context = adl.get_context()
            
            if current_context == "giant":
                adl.say("""
                    Your way is currently blocked.
                    Or have you forgotten the giant you are fighting?
                    """)
            else:
                
                if current_context:
                    print("Fare thee well, traveler!")
                    adl.set_context(None)

                present_location = next_room
                print(f"You go {direction}.")
                look()
                
    else:
        print(f"You can't go {direction}.")
        
def prompt():
    
    global present_location
    
    exits_string = get_exits(present_location)
    
    if adl.get_context() == "giant":
        prompt_string = f"HP: {hit_points} > "
        
    else:
        prompt_string = f"({present_location.title}) > "

    return f"""({exits_string}) {prompt_string}"""


def no_command_matches(command: str):
    
    if adl.get_context() == "wizard.riddle":
        adl.say("That is not the correct answer. Begone! from My sight")
        adl.set_context(None)
        present_location.locked_exits["west"] = False
        
    else:
        print(f"What do you mean by '{command}'?")
        
        
def get_exits(room):
    exits = room.exits()

    exits_string = ""
    
    for exit in exits:
        exits_string += f"{exit[0].upper()}|"

    return exits_string[:-1]

if __name__ == "__main__":

    adl.set_context(None)


    adl.prompt = prompt


    adl.no_command_matches = no_command_matches


    look()


    adl.start()


    
        
    
