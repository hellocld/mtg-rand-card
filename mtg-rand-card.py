#!/usr/bin/python

import sys
import requests

api_url = "https://api.scryfall.com"
ep_random = "/cards/random"


# Display card data
def print_card(card, set_code, url):
# -Name
# -Cost
    if "mana_cost" in card:
        name_line = "{} | {}"
        print(name_line.format(card["name"], card["mana_cost"]))
    else:
        print(card["name"])
# -Typeline
# -Set
    if "type_line" in card:
        type_line = "{} - {}"
        print(type_line.format(card["type_line"], set_code))
    else:
        print(set_code)
# -Rules
    if "oracle_text" in card:
        print(card["oracle_text"])
# -Power/Toughness
    if "power" in card and "toughness" in card:
        pt = "({}/{})"
        print(pt.format(card["power"], card["toughness"]))
# -Flavortext
    if "flavor_text" in card:
        print(card["flavor_text"])
# -Scryfall URL
    print(url)


def main():
    # Grab a random card from Scryfall
    card_response = requests.get(api_url + ep_random)

    if not card_response.ok:
        print("Error acquiring card!")
        print(card_response.reason)
        return

    card_dict = card_response.json()
    # Check if it's multiface or not
    if "card_faces" in card_dict:
        for face in card_dict["card_faces"]:
            print_card(face, card_dict["set"], card_dict["scryfall_uri"])
    else:
        print_card(card_dict, card_dict["set"], card_dict["scryfall_uri"])

if __name__ == '__main__':
    sys.exit(main())


