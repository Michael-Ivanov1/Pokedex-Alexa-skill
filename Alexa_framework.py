from flask import Flask, render_template
from flask_ask_098 import Ask, statement, question, session
import json
import requests
import time
import unidecode

# input_name = input("enter a pokemon name ").lower()
# poke = requests.get("https://pokeapi.co/api/v2/pokemon/" + input_name)

app = Flask(__name__)
ask = Ask(app, "/pokedex")



class Game:

    def __init__(self, name, move):
        self.temp = None
        self.move = move
        # self.game_version = game_version
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

        if self.temp:
            for x in self.temp["version_group_details"]:

                if self.game_version == x["version_group"]["name"]:

                    if not x["level_learned_at"] == 0:

                        return self.name + " learns" + self.print_name + " at level " + str(x["level_learned_at"])

                    else:

                        return self.name + " learns" + self.print_name + "by " + x["move_learn_method"][
                            "name"]

                else:

                    return self.name + " can't learn" + self.print_name + " in this game"

        else:
            for x in poke.json()["moves"]:
                if self.move == x["move"]["name"]:
                    self.temp = x
                    return self.how_learn()

        return self.name + " cannot learn" + self.print_name


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


@app.route('/')
def homepage():
    return "hi there, how ya doing?"


@ask.launch
def start_skill():
    welcome_message = "Hello, welcome to Michael's pokedex skill"
    return question(welcome_message)


@ask.intent("TypeIntent", convert={'Pokemon': str})
def share_headlines(Pokemon):
    type = Pokemon

    poke = get_type(type)

    headline_msg = "This pokemon's type is {}".format(poke)
    return question(headline_msg)


@ask.intent("MoveIntent", convert={'Pokemon': str, 'Move': str})
def moves(Pokemon, Move):
    a = Game(Pokemon, Move)
    return question(a.moves_learned())


@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)


if __name__ == '__main__':
    app.run(debug=True)
