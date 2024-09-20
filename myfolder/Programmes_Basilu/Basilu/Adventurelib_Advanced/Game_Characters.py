import adventurelib as adl

# ------------------------------------------------
""" 
Module Game_Characters written by Basilu Liyanage.
cc
"""
# ------------------------------------------------

adl.Item.greeting = ""
adl.Item.context = ""

# ------------------------------------------------

theron_windrider = adl.Item("Theron Windrider", "theron", "windrider")
theron_windrider.description = """
        Theron Windrider, with silver-streaked hair and stormy sea-colored eyes, exudes wisdom and strength.
        His weathered face hints at countless adventures. Draped in a cloak of azure and emerald, he carries a staff topped with a glowing crystal,
        symbolizing his authority. His deep, melodic voice offers guidance and insight, while his fire for adventure remains undimmed.
        Theron is a trusted advisor and formidable ally, always ready to face challenges with unwavering integrity and vast knowledge.
        """
theron_windrider.greeting = ("""Greetings, Maxwell. I have some important information for you. Would you like to hear it?""")
theron_windrider.context = "counsellor"

# ------------------------------------------------

bram_ironsmith = adl.Item("Bram Ironsmith", "bram", "ironsmith")
bram_ironsmith.description = """
        Bram Ironsmith is a robust and imposing figure, his muscles honed from years at the forge.
        His bronzed skin and calloused hands reflect his dedication to his craft. With piercing blue eyes and a thick, iron-gray beard,
        he wears a scarred leather apron over a simple tunic. Known for his exceptional skill and integrity,
        Bram's workshop resonates with the steady clang of hammer on anvil.
        """
bram_ironsmith.greeting = ("""Maxwell Nightshade, welcome. I have forged a new sword for you,
                        tempered with the finest steel and imbued with the strength of a thousand battles. Would you like to have it?""")
bram_ironsmith.context = "blacksmith"

# ------------------------------------------------

elias_swiftblade = adl.Item("Elias Swiftblade", "elias", "swiftblade")
elias_swiftblade.description = """
        Elias Swiftblade is a tall, slender figure draped in flowing robes of deep blue and silver,
        embroidered with arcane symbols. His long, silver hair cascades down his back, and his sharp, green eyes seem to pierce through to your very soul.
        His presence is both commanding and serene, exuding an aura of ancient wisdom and potent magic.
        Around his neck hangs an amulet glowing faintly with magical energy, a testament to his prowess in the mystical arts.
        """
elias_swiftblade.greeting = ("""Ah, Maxwell Nightshade. I see you have a fine new sword. I am Elias Swiftblade,
                          and I can enchant it with powerful magic. Would you like to see its true potential unlocked?""")
elias_swiftblade.context = "wizard"

# ------------------------------------------------

blunt_grimson = adl.Item("Blunt Grimson", "blunt", "grimson", "hungary giant")
blunt_grimson.description = """
        Blunt Grimson is a towering giant, standing nearly twice the height of a man, with muscles rippling beneath his rough,
        leathery skin. His eyes burn with a fierce, malevolent light, and his unruly hair falls in tangled locks around his brutish face.
        Clad in piecemeal armor cobbled together from his plunder, he wields a massive club,
        scarred from countless battles. His presence is as intimidating as a storm, casting a shadow over the land he terrorizes.
        """
blunt_grimson.greeting = ("""Maxwell Nightshade, you dare challenge me? I, Blunt Grimson, have taken your livestock and will now take your life.
                       Prepare to fight!""")
blunt_grimson.context = "giant"

