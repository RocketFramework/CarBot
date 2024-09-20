import adventurelib as adl

import Game_Items

import Game_Characters

# ------------------------------------------------
"""
Module Game_Rooms written by Basilu Liyanage.
Includes:
    Game_Characters, Game_Items, Game_Rooms
    
    Home, Hamlet, Fork, Village, Blacksmith's Shop
    Wizard's Hut, Side Path, Cave Mouth and Giant's Cave
"""
# ------------------------------------------------


class GameArea(adl.Room):

    def __init__(self, description: str):

        super().__init__(description)

        self.locked_exits = {
            "north": False,
            "south": False,
            "east": False,
            "west": False,
        }

        self.items = adl.Bag()
        self.characters = adl.Bag()
        self.visited = False
        self.short_desc = ""
        self.title = ""


# ------------------------------------------------

home = GameArea("""
        You wake as the sun streams in through the single
        window into your small room. You lie on your feather bed which
        hugs the north wall, while the remains of last night's
        fire smolders in the center of the room.

        Remembering last night's discussion with the council, you
        throw back your blanket and rise from your comfortable
        bed. Cold water awaits you as you splash away the night's
        sleep, grab an apple to eat, and prepare for the day.
        """)

home.title = "Home"
home.short_desc ="You are at Tech Reteat"

# ------------------------------------------------

hamlet = GameArea("""
        From the center of your small hamlet, you can see every other
        home. It doesn't really even have an official name --- folks
        around here just call it Home.

        The council awaits you as you approach. Theron Windrider beckons you
        as you exit your home.
        """)
hamlet.title = "Hamlet"
hamlet.short_desc = "You are in Wildwood stronghold."

# ------------------------------------------------

fork = GameArea("""
        As you leave your hamlet, you realize your lack of pitiful equipment
        are certainly no match for whatever has been stealing
        the villages livestock.

        As you travel, you come across a fork in the path. The path of
        the livestock thief continues east. However, you know
        the village of Silvershadev lies to the west, where you may
        get some additional help.
        """)
fork.title = "Fork in road"
fork.short_desc = "You are at a fork in the road. The desitions you make is Life or Death! Choose Wisely."

# ------------------------------------------------

village = GameArea("""
        A short trek up the well-worn path brings you the village
        of Silvershade. Larger than your humble Home, Silvershade sits at
        the end of a supply route from the capitol. As such, it has
        amenities and capabilities not found in the smaller farming
        communities.

        As you approach, you hear the clang-clang of hammer on anvil,
        and inhale the unmistakable smell of the coal-fed fire of a
        blacksmith shop to your south.
        """)
village.title = "Silvershade"
village.short_desc = "You stand amidst the adventurous village of Silvershade, where opportunity and danger intertwine"

# ------------------------------------------------

blacksmith_shop = GameArea("""
        Entering the blacksmith's domain, the rhythmic clang of metal on metal fills the air, drowning out all other sounds.
        The dimly lit interior is thick with the smell of hot coals and sweat, a testament to the hard work being done within.
        Your eyes adjust to the flickering light of the furnace, revealing the blacksmith hard at work. With each strike of her hammer,
        sparks dance like fireflies in the dimness, illuminating her skilled hands as they shape molten metal into formidable weapons and sturdy armor.
        """)
blacksmith_shop.title = "Blacksmith Shop"
blacksmith_shop.short_desc = "You are in the blacksmith shop."

# ------------------------------------------------

side_path = GameArea("""
        Venturing down the path that veers away from the main road to Silvershade, you find yourself amidst a tangle of underbrush and shadowed trees.
        The air is heavy with the scent of damp earth and anticipation, as if the forest itself holds its breath in anticipation of your next move.
        Fresh tracks, large and ominous, cut a path through the undergrowth, leading southward.
        Whatever left them moves with purpose, dragging something heavy and mysterious behind it.
        Each step forward fills you with a mix of excitement and trepidation, as you follow the trail into the unknown.
        """)
side_path.title = "Side path"
side_path.short_desc = "You stand at the entrance of a mysterious side path, where fresh tracks beckon towards adventure"

# ------------------------------------------------

wizard_hut = GameArea("""
        The path opens into a shaded glen. A small stream wanders down the
        hills to the east and past an unassuming hut. In front of the hut,
        the local wizard Trent sits smoking a long clay pipe.
        """)
wizard_hut.title = "Wizard's Hut"
wizard_hut.short_desc = "You are at the wizard's hut."

# ------------------------------------------------

cave_mouth = GameArea("""
        The path from Trent's hut follows the stream for a while before
        turning south away from the water. The trees begin closing overhead,
        blocking the sun and lending a chill to the air as you continue.

        The path finally terminates at the opening of a large cave. The
        tracks you have been following mix and mingle with others, both
        coming and going, but all the same. Whatever has been stealing
        your neighbor's livestock lives here, and comes and goes frequently.
        """)
cave_mouth.title = "Cave Mouth"
cave_mouth.short_desc = "You are at the mouth of large cave."

# ------------------------------------------------

giant_cave = GameArea("""
        You take a few tentative steps into the cave. It feels much warmer
        and more humid than the cold sunless forest air outside. A steady
        drip of water from the rocks is the only sound for a while.

        You begin to make out a faint light ahead. You hug the wall and
        press on, as the light becomes brighter. You finally enter a
        chamber at least 20 meters across, with a fire blazing in the center.
        Cages line one wall, some empty, but others containing cows and
        sheep stolen from you neighbors. Opposite them are piles of the bones
        of the creatures unlucky enough to have already been devoured.

        As you look around, you become aware of another presence in the room.
        """)
giant_cave.title = "Cave of the Giant"
giant_cave.short_desc = "You stand in the heart of the Giant's Lair, where danger lurks in every shadow."

# ------------------------------------------------

home.south = hamlet
hamlet.south = fork
fork.west = village
fork.east = side_path
village.south = blacksmith_shop
side_path.south = wizard_hut
wizard_hut.west = cave_mouth
cave_mouth.south = giant_cave

hamlet.locked_exits["south"] = True
wizard_hut.locked_exits["west"] = True

home.items.add(Game_Items.apple)
fork.items.add(Game_Items.cloak)
cave_mouth.items.add(Game_Items.slug)

hamlet.characters.add(Game_Characters.theron_windrider)
blacksmith_shop.characters.add(Game_Characters.bram_ironsmith)
wizard_hut.characters.add(Game_Characters.elias_swiftblade)
giant_cave.characters.add(Game_Characters.blunt_grimson)

