import adventurelib as adl

# ------------------------------------------------

""" 
Module Game_Items written by Basilu Liyanage.
Includes:
    apple, slug, steel sword              
    cloak, wooden sword,
""" 

# ------------------------------------------------

adl.Item.color = "undistinguished"
adl.Item.description = "a generic thing"
adl.Item.edible = False
adl.Item.wearable = False

# ------------------------------------------------

apple = adl.Item("small red apple", "apple")
apple.color = "red"
apple.description = "A small, ripe, red apple with smooth, shiny skin and a sweet, juicy interior."
apple.edible = True
apple.wearable = False

# ------------------------------------------------

cloak = adl.Item("cotton cloak", "cloak")
cloak.color = "black"
cloak.description = "The cloak: midnight-black, whispers tales of heroes, conceals its wearer in mystery."
cloak.edible = False
cloak.wearable = True

# ------------------------------------------------

slug = adl.Item("slimy brown slug", "slug")
slug.color = "slimy brown"
slug.description = "The slug: a slow, slimy creature, leaves a glistening trail behind."
slug.edible = True
slug.wearable = False

# ------------------------------------------------

wooden_sword = adl.Item("wooden sword", "sword")
wooden_sword.color = "brown"
wooden_sword.description = "The wooden practice sword: a sturdy training tool, light and balanced for honing skills."
wooden_sword.edible = False
wooden_sword.wearable = False
wooden_sword.damage = 4
wooden_sword.bonus = 0

# ------------------------------------------------

steel_sword = adl.Item("steel sword", "sword")
steel_sword.color = "steely grey"
steel_sword.description = "The steel sword: gleaming with menace, a formidable weapon in skilled hands."
steel_sword.edible = False
steel_sword.wearable = False
steel_sword.damage = 10
steel_sword.bonus = 0
