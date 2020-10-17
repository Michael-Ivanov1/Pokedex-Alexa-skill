import requests
import json

g_move = None
g_poke = None
g_skill = None


# This class contains the info for pokemon moves: whether they can learn them, and if they can by which method
class PokeMove:

    def __init__(self, name, move, generation):

        self.temp = None
        self.move = move
        self.gen = generation
        self.name = name
        self.print_name = ""
        self.printName()
        self.poke = requests.get("https://pokeapi.co/api/v2/pokemon/" + name)

    def printName(self):
        for a in self.move.split("-"):
            self.print_name += " " + a

    def moves_learned(self):

        # Can this pokemon learn this move
        # What level does this pokemon learn this move
        # Returns a boolean of whether the pokemon can learn a certain move
        # Go to move then find pokemon or go to pokemon and find move?
        # Locally cache the specific move as an object to answer the question of when the pokemon learns that move

        if self.temp:
            return "Yes"

        for x in self.poke.json()["moves"]:
            if self.move == x["move"]["name"]:
                self.temp = x
                return "Absolutely"

        return "Nope"

    def how_learn(self):
        self.moves_learned()
        gen = self.gen
        if self.gen == "sword" or self.gen == "shield":
            self.gen = "ultra-sun"

        if self.temp:

            # a is the placeholder json so I don't have to type out the entire json text for every check
            a = None
            b = self.temp["version_group_details"]

            # This checks if the game said is in the game list for the pokemon (an aloan pokemon can't be in sinnoh)
            name1 = self.gen + "-"
            name2 = "-" + self.gen

            for c in b:
                if self.gen in c["version_group"]["name"] or name1 in c["version_group"]["name"] or name2 in \
                        c["version_group"]["name"]:
                    a = c
                    break
            if not a:
                return self.name + " can't learn" + self.print_name + " in " + gen

            if not a["level_learned_at"] == 0:

                return self.name + " learns" + self.print_name + " at level " + str(
                    a["level_learned_at"]) + " in " + gen

            else:

                return self.name + " learns" + self.print_name + " by " + a["move_learn_method"]["name"] + " in " + gen

        else:
            return self.name + " can't learn" + self.print_name


# if the move or name is more than one word, this returns the move with a dash in between the two letters
# this is the format that the json reads
def name_split(Move):
    if len(Move.split(" ")) > 1:
        Move = Move.split(" ")
        move = Move[0] + "-" + Move[1]
    else:
        move = Move

    return move


def name_join(Name):
    Name = Name.split(" ")
    str = ""
    if len(Name) == 2:
        for a in Name:
            str += a
        return str
    else:
        return Name[0]


# This is a outer-class skill because it can be called often.
def get_type(name):
    name = name.split("'s")[0]

    if name == "Pikachū":
        name = "pikachu"

    poke = requests.get("https://pokeapi.co/api/v2/pokemon/" + name)
    type_array = []
    for x in range(len(poke.json()["types"])):
        type_array.append(poke.json()["types"][x]["type"]["name"])

    if len(type_array) > 1:
        return type_array[0] + " and " + type_array[1]
    else:
        return type_array[0]


def TypeIntent(A):
    if A == "Pikachū":
        A = "pikachu"

    poke = get_type(A)
    name = A.split("'s")[0]
    return name + " is a {}".format(poke) + " type Pokemon"


def pokemon_ID(Poke_Id):
    if Poke_Id == "Pikachū":
        Poke_Id = "pikachu"

    name = Poke_Id.split("'s")[0]
    poke = requests.get("https://pokeapi.co/api/v2/pokemon/" + name)
    if not poke:
        return "Please repeat the pokemon"

    i = poke.json()["id"]

    return name + "'s ID is {}".format(i)


def boolean_move(Poke, Move):
    if Poke == "Pikachū":
        Poke = "pikachu"
    move = name_split(Move)
    a = PokeMove(Poke, move, None)
    return a.moves_learned()


def how_move(Poke, Move):
    global g_poke, g_move

    g_poke = Poke.split("'s")[0]

    g_move = name_split(Move)

    return g_poke, g_move


def pokemon_description(Description):
    global g_skill, g_poke

    g_skill, g_poke = "description", Description.split("'s")[0]

    return g_skill, g_poke


# As of now, there are two instances to where a generation is needed to specify a skill
# I created a global variable to see which of the two skills needs to be called

def game_version(Generation, g_poke, g_move, g_skill):
    Gen_list = ["soul silver", "heart gold", "leaf green", "fire red"]
    name = Generation
    if Generation == "sword" or Generation == "shield":
        Generation = "ultra-sun"

    if Generation in Gen_list:
        Gen = name_join(Generation)
    else:
        Gen = name_split(Generation)

    if g_poke == "Pikachū":
        g_poke = "pikachu"

    if g_skill == "description":

        poke = requests.get("https://pokeapi.co/api/v2/pokemon-species/" + g_poke)

        for a in poke.json()["flavor_text_entries"]:
            if a["language"]["name"] == "en" and a["version"]["name"] == Gen:
                return a["flavor_text"].replace("\\n", " ")

        for b in reversed(poke.json()["flavor_text_entries"]):
            if b["language"]["name"] == "en":
                return b["flavor_text"].replace("\\n", " ")

    else:

        print(Gen)
        a = PokeMove(g_poke, g_move, Gen)
        return a.how_learn()
