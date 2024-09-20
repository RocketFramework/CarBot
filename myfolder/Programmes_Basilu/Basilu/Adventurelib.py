import adventurelib as adl

bedroom = adl.Room("""

You find yourself in the sanctuary of your bedroom,
where the bed beckons with its tousled sheets and the dresser stands stoically in the corner,
while a desk basks in the gentle glow of the window's embrace.
""")


front_porch = adl.Room("""
                       
The weathered boards of your front porch greet you with a familiar creak,
as though whispering tales of days gone by. Beneath your feet, the welcome mat extends its greeting,
inviting you to step forward into the embrace of home.
""")


living_room = adl.Room("""
                       
In the luminous expanse of the living room, tranquility reigns supreme. The TV rests in silent repose, 
while the radiant sun streams through the parted curtains,
casting a warm glow upon the space.
""")


bedroom.south = living_room
living_room.east = front_porch

living_room.locked = {"east": True}
bedroom.locked = {}
front_porch.locked = {}

start_point = bedroom


def living_room_unlock(start_point):
    if start_point == living_room:
        print("With a satisfying click, you unlock the door.")
        start_point.locked["east"] = False
    else:
        print("You fumble with the key, but there's no lock to be found. You were unable to unlock the door ")


key = adl.Item("a front door key", "key")
key.use_item = living_room_unlock

bedroom.contents = adl.Bag()
living_room.contents = adl.Bag()
front_porch.contents = adl.Bag()

bedroom.contents.add(key)

store = adl.Bag()


@adl.when("move DIRECTION")
@adl.when("north", direction="north")
@adl.when("south", direction="south")
@adl.when("east", direction="east")
@adl.when("west", direction="west")
@adl.when("n", direction="north")
@adl.when("s", direction="south")
@adl.when("e", direction="east")
@adl.when("w", direction="west")


def move(direction: str):
    global start_point
    
    next_room = start_point.exit(direction)
    if next_room:
        if direction in start_point.locked and start_point.locked[direction]:
            print(f"The {direction} is blocked by a locked door. Seek another path to continue the adventure!")
        else:
            start_point = next_room
            print(f"You head {direction}.")
            look()
    else:
        print(f"Unfortunately, you're unable to go {direction}.")

def look():
    adl.say(start_point)
    for item in start_point.contents:
        print(f"As you explore, you discover {item} lying here, waiting to be found.")
        
    print(f"The following exits are available: {', '.join(start_point.exits())}")
    
@adl.when("look at ITEM")
@adl.when("inspect ITEM")

def look_at(item: str):
    obj = store.find(item)
    if not obj:
        print(f"Unfortunately! You're missing {item}.")
    else:
        print(f"It's an {obj}.")

@adl.when("take ITEM")
@adl.when("get ITEM")
@adl.when("pickup ITEM")

def get(item: str):
    global start_point
    
    obj = start_point.contents.take(item)
    
    if not obj:
        print(f"Unfortunately, There is no {item} here. ")
    else:
        print(f"Excitedly, you've uncovered {item}!")
        store.add(obj)
        
@adl.when("unlock door", item="key")
@adl.when("use ITEM")

def use(item: str):
    obj = store.take(item)
    if not obj:
        print(f"Unfortunately, You don't have {item}")
        
    else:
        obj.use_item(start_point)

if __name__ == "__main__":
    look()
    adl.start()