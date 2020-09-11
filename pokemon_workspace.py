import requests




# def get_type():
#     type_array = []
#     for x in range(len(poke.json()["types"])):
#         type_array.append(poke.json()["types"][x]["type"]["name"])
#     return type_array
#     # on the alexa response read out each element of the list
#
#
# class Game:
#
#     def __init__(self, move, game_version):
#         self.temp = None
#         self.move = move
#         self.game_version = game_version
#         self.name = input_name
#         self.print_name = ""
#         self.name_split()
#
#     def name_split(self):
#         for a in self.move.split("-"):
#             self.print_name += " " + a
#
#     def moves_learned(self):
#
#         # Can this pokemon learn this move
#         # What level does this pokemon learn this move
#         # Returns a boolean of whether the pokemon can learn a certain move
#         # Go to move then find pokemon or go to pokemon and find move?
#         # Locally cache the specific move as an object to answer the question of when the pokemon learns that move
#
#         if self.temp:
#             return True
#
#         for x in poke.json()["moves"]:
#             if self.move == x["move"]["name"]:
#                 self.temp = x
#                 return True
#
#         return False
#
#     def how_learn(self):
#
#         if self.temp:
#             for x in self.temp["version_group_details"]:
#
#                 if self.game_version == x["version_group"]["name"]:
#
#                     if not x["level_learned_at"] == 0:
#
#                         return self.name + " learns" + self.print_name + " at level " + str(x["level_learned_at"])
#
#                     else:
#
#                         return self.name + " learns" + self.print_name + "by " + x["move_learn_method"][
#                             "name"]
#
#                 else:
#
#                     return self.name + " can't learn" + self.print_name + " in this game"
#
#         else:
#             for x in poke.json()["moves"]:
#                 if self.move == x["move"]["name"]:
#                     self.temp = x
#                     return self.how_learn()
#
#         return self.name + " cannot learn" + self.print_name


class PokemonType:

    def __init__(self):
        self.double_damage_from, self.double_damage_to, self.half_damage_to, self.half_damage_from = [], [], [], []
        self.no_damage_from, self.no_damage_to = [], []
        self.quad_damage_to, self.quad_damage_from, self.quarter_damage_to, self.quarter_damage_from = [], [], [], []
        self.types = get_type()
        self.damage_to()
        self.damage_from()

    def damage_to(self):

        for t in self.types:
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

    def damage_from(self):

        for t in self.types:
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


# def how_evolve():
#     species = requests.get(poke.json()["species"]["url"])
#
#     evo_chain = requests.get(species.json()["evolution_chain"]["url"])
#
#     name_check = evo_chain.json()["chain"]["species"]["name"]
#     evo_chain = evo_chain.json()["chain"]["evolves_to"]
#
#     while name_check != input_name:
#         name_check = evo_chain[0]["species"]["name"]
#         evo_chain = evo_chain[0]["evolves_to"]
#
#     if not evo_chain:
#         return "Pokemon cannot evolve"
#
#     evo_list = {}
#
#     evo_dict = evo_chain[0]["evolution_details"][0].items()
#
#     for key, value in evo_dict:
#         if value:  # if there exist a value for the certain key
#             evo_list.update({key: value})
#
#     return evo_list
#
#
# y = Game("tail-whip", "diamond-pearl")
#
# print(y.how_learn())
