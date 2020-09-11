from flask import Flask, render_template
from flask_ask_098 import Ask, statement, question, session
import requests
import json

app = Flask(__name__)
ask = Ask(app, "/pokedex")

g_move = None
g_poke = None
g_type = None
g_skill = None


# This takes all of the types of a pokemon and finds the effectiveness/weakness to and from each pokemon
class PokemonType:

    def __init__(self, type, name):
        self.double_damage_from, self.double_damage_to, self.half_damage_to, self.half_damage_from = [], [], [], []
        self.no_damage_from, self.no_damage_to = [], []
        self.quad_damage_to, self.quad_damage_from, self.quarter_damage_to, self.quarter_damage_from = [], [], [], []

        self.name = name
        self.types = self.self_get_type() if not type else type
        self.damage_to()
        self.damage_from()

    def self_get_type(self):

        poke = requests.get("https://pokeapi.co/api/v2/pokemon/" + self.name)
        type_array = []
        for x in range(len(poke.json()["types"])):
            type_array.append(poke.json()["types"][x]["type"]["name"])

        return type_array

    def damage_to(self):

        for t in self.types:
            if len(self.types) != 2:
                t = self.types
            d = requests.get("https://pokeapi.co/api/v2/type/" + t)
            d = d.json()["damage_relations"]

            for x in d["double_damage_to"]:
                if [x][0]["name"] in set(self.double_damage_to):
                    self.double_damage_to.remove([x][0]["name"])
                    self.quad_damage_to.append([x][0]["name"])
                elif [x][0]["name"] in set(self.double_damage_from):
                    self.double_damage_from.remove([x][0]["name"])
                else:
                    self.double_damage_to.append([x][0]["name"])

            for x in d["half_damage_to"]:
                if [x][0]["name"] in set(self.half_damage_to):
                    self.half_damage_to.remove([x][0]["name"])
                    self.quarter_damage_to.append([x][0]["name"])
                elif [x][0]["name"] in set(self.double_damage_to):
                    self.double_damage_to.remove([x][0]["name"])
                else:
                    self.half_damage_to.append([x][0]["name"])

            for x in d["no_damage_to"]:
                if [x][0]["name"] in set(self.half_damage_to):
                    self.half_damage_to.remove([x][0]["name"])
                if [x][0]["name"] in set(self.double_damage_to):
                    self.double_damage_from.remove([x][0]["name"])
                self.no_damage_to.append([x][0]["name"])
            if len(self.types) != 2:
                break

    def damage_from(self):

        for t in self.types:
            if len(self.types) != 2:
                t = self.types
            d = requests.get("https://pokeapi.co/api/v2/type/" + t)
            d = d.json()["damage_relations"]

            for x in d["double_damage_from"]:
                if [x][0]["name"] in set(self.double_damage_from):
                    self.double_damage_from.remove([x][0]["name"])
                    self.quad_damage_from.append([x][0]["name"])
                elif [x][0]["name"] in set(self.half_damage_from):
                    self.half_damage_from.remove([x][0]["name"])
                else:
                    self.double_damage_from.append([x][0]["name"])

            for x in d["half_damage_from"]:
                if [x][0]["name"] in set(self.half_damage_from):
                    self.half_damage_from.remove([x][0]["name"])
                    self.quarter_damage_from.append([x][0]["name"])
                elif [x][0]["name"] in set(self.double_damage_from):
                    self.double_damage_from.remove([x][0]["name"])
                else:
                    self.half_damage_from.append([x][0]["name"])

            for x in d["no_damage_from"]:
                if [x][0]["name"] in set(self.half_damage_from):
                    self.half_damage_from.remove([x][0]["name"])
                if [x][0]["name"] in set(self.double_damage_from):
                    self.double_damage_from.remove([x][0]["name"])
                self.no_damage_from.append([x][0]["name"])
            if len(self.types) != 2:
                break


# This class contains the info for pokemon moves: whether they can learn them, and if they can by which method
class Poke_move:

    def __init__(self, name, move, generation):
        self.temp = None
        self.move = move
        self.gen = generation
        self.name = name
        self.print_name = ""
        self.name_split()
        self.poke = requests.get("https://pokeapi.co/api/v2/pokemon/" + name)

    def name_split(self):
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
                return "Yes"

        return "Nope"

    def how_learn(self):
        if self.moves_learned() == "Yes":
            if self.temp:

                # a is the placeholder json so I don't have to type out the entire json text for every check
                a = None
                b = self.temp["version_group_details"]

                # This checks if the game said is in the game list for the pokemon (an aloan pokemon can't be in pearl)
                name1 = self.gen + "-"
                name2 = "-" + self.gen

                for c in b:
                    if self.gen in c["version_group"]["name"] or name1 in c["version_group"]["name"] or name2 in \
                            c["version_group"]["name"]:
                        a = c
                        break
                if not a:
                    return "Please enter a valid game"

                if not a["level_learned_at"] == 0:

                    return self.name + " learns " + self.print_name + " at level " + str(a["level_learned_at"])

                else:

                    return self.name + " learns " + self.print_name + " by " + a["move_learn_method"][
                        "name"]

            else:
                for x in self.poke.json()["moves"]:
                    if self.move == x["move"]["name"]:
                        self.temp = x
                        return self.how_learn()
        else:
            return self.name + " can't learn " + self.print_name + " in this game."


# if the move or name is more than one word, this returns the move with a dash in between the two letters
# this is the format that the json reads
def name_split(Move):
    if len(Move.split(" ")) > 1:
        Move = Move.split(" ")
        move = Move[0] + "-" + Move[1]
    else:
        move = Move

    return move


# This is a outer-class skill because it can be called often.
def get_type(name):
    name = name.split("'s")[0]

    poke = requests.get("https://pokeapi.co/api/v2/pokemon/" + name)
    type_array = []
    for x in range(len(poke.json()["types"])):
        type_array.append(poke.json()["types"][x]["type"]["name"])

    if len(type_array) > 1:
        return type_array[0] + " and " + type_array[1]
    else:
        return type_array[0]


# When the link is opened in a browser, this message appears.
@app.route('/')
def homepage():
    return "Welcome to Michael's pokedex skill. This is meant for use with Amazon Alexa, you shouldn't be googling this."


@ask.launch
def start_skill():
    welcome_message = "Hello, welcome to Michael's pokedex skill"
    return question(welcome_message)


@ask.intent("TypeIntent", convert={'Pokemon': str})
def TypeIntent(Pokemon):
    poke = get_type(Pokemon)

    return question(Pokemon + "'s type is {}".format(poke))


@ask.intent("IDIntent", convert={'Pokemon': str})
def pokemon_ID(Pokemon):
    name = Pokemon.split("'s")[0]

    poke = requests.get("https://pokeapi.co/api/v2/pokemon/" + name)

    i = poke.json()["id"]

    return question(Pokemon + " 's ID is {}".format(i))


# returns whether a pokemon can learn a certain move
@ask.intent("MoveIntent", convert={'Pokemon': str, 'Move': str})
def boolean_move(Pokemon, Move):
    move = name_split(Move)
    a = Poke_move(Pokemon, move, None)
    return question(a.moves_learned())


@ask.intent("Howlearnmoveintent", convert={'Pokemon': str, 'Move': str})
def how_move(Pokemon, Move):
    global g_poke, g_move, g_skill

    g_skill = "how_learn()"
    g_poke = Pokemon
    g_move = name_split(Move)

    return question("Which game are you playing?")


@ask.intent("DescriptionIntent", convert={'Pokemon': str, "Generation": str})
def pokemon_description(Pokemon, Generation):
    global g_skill, g_poke

    if not Generation:
        g_skill, g_poke = "description", Pokemon.split("'s")[0]
        return question("what game are you playing")

    name = Pokemon.split("'s")[0]

    poke = requests.get("https://pokeapi.co/api/v2/pokemon-species/" + name)

    x = "Please repeat the generation"
    for a in poke.json()["flavor_text_entries"]:
        if a["language"]["name"] == "en" and a["version"]["name"] == Generation:
            x = a["flavor_text"].replace("\\n", " ")

    return question(x)


# As of now, there are two instances to where a generation is needed to specify a skill
# I created a global variable to see which of the two skills needs to be called
@ask.intent("gameversionintent", convert={'Generation': str})
def game_version(Generation):
    global g_poke, g_move, g_skill

    if Generation == "sword" or Generation == "shield":
        Generation = "ultra sun"

    if g_skill == "description":

        poke = requests.get("https://pokeapi.co/api/v2/pokemon-species/" + g_poke)

        msg = "Please repeat the generation"
        for a in poke.json()["flavor_text_entries"]:
            if a["language"]["name"] == "en" and a["version"]["name"] == Generation:
                msg = a["flavor_text"].replace("\\n", " ")

        return question(msg)
    else:
        Gen = name_split(Generation)
        print(Gen)
        a = Poke_move(g_poke, g_move, Gen)

        return question(a.how_learn())



