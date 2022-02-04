#!/usr/bin/python

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print
from rich import box
import requests

api_url = "https://api.scryfall.com"
ep_random = "/cards/random"

# Styles
st_rarity = {
    "common": "bold white on black",
    "uncommon": "bold white on grey50",
    "rare": "bold black on gold1",
    "special": "bold black on purple",
    "mythic": "bold black on orange_red1",
    "bonus": "bold black on yellow3"
}

st_link = "link {}"


# Display card data
def get_card(card, set_code, rarity) -> Panel:
    grid = Table.grid(expand=False)
    grid.width = 40
    grid.add_column()
    grid.add_row(get_title(card))
    grid.add_row(get_typeline(card, set_code, rarity))
    grid.add_row(get_rules(card))
    fptl = get_flavor_pt(card)
    if fptl is not None:
        grid.add_row(fptl)
    panel = Panel(grid, expand=False)
    return panel


def get_color_ident(card) -> str:
    if "colors" not in card or len(card["colors"]) == 0:
        return "none"
    if len(card["colors"]) > 1:
        return "gold1"
    color = card["colors"][0]
    if color == "W":
        return "cornsilk1"
    if color == "U":
        return "blue1"
    if color == "B":
        return "purple4"
    if color == "R":
        return "red3"
    if color == "G":
        return "green4"
    return "none"


def colorize_text(text) -> str:
    return text.replace("{W}", "{[cornsilk1]W[/cornsilk1]}").replace("{U}", "{[blue1]U[/blue1]}").replace("{B}", "{[purple4]B[/purple4]}").replace("{R}", "{[red3]R[/red3]}").replace("{G}", "{[green4]G[/green4]}")


def get_title(card) -> Panel:
    title = Table.grid(expand=False)
    title.width = 36
    title.add_column(style="bold")
    if "mana_cost" in card:
        title.add_column(justify="right")
        title.add_row(card["name"], colorize_text(card["mana_cost"]))
    else:
        title.add_row(card["name"])
    panel = Panel(title, expand=False)
    panel.border_style = get_color_ident(card)
    return panel


def get_typeline(card, set_code, rarity) -> Panel:
    typeline = Table.grid(expand=False)
    typeline.width = 36
    typeline.add_column()
    typeline.add_column(justify="center", style=st_rarity[rarity])
    typeline.add_row(card["type_line"], set_code)
    panel = Panel(typeline, expand=False)
    panel.border_style = get_color_ident(card)
    return panel


def get_rules(card) -> Panel:
    if "oracle_text" in card:
        return Panel(colorize_text(card["oracle_text"]), width=40, border_style=get_color_ident(card))
    else:
        return Panel("", width=40, border_style=get_color_ident(card))

def get_flavor_pt(card) -> Panel:
    grid = Table.grid(expand=False)
    grid.width = 36
    grid.add_column(justify="right")
    if "flavor_text" in card:
        grid.add_row(card["flavor_text"], style="italic")
    if "power" in card and "toughness" in card:
        pt = "({}/{})"
        grid.add_row(pt.format(card["power"], card["toughness"]), style="bold")
    if "loyalty" in card:
        loyal = "[{}]"
        grid.add_row(loyal.format(card["loyalty"]), style="bold")

    panel = Panel(grid, expand=False)
    panel.border_style = get_color_ident(card)
    return panel



def main():
    # Grab a random card from Scryfall
    card_response = requests.get(api_url + ep_random)

    if not card_response.ok:
        print("Error acquiring card!")
        print(card_response.reason)
        return
    console = Console()
    card_dict = card_response.json()
    # Check if it's multiface or not
    if "card_faces" in card_dict:
        grid = Table.grid(expand=False, padding=2)
        cells = []
        for face in card_dict["card_faces"]:
            grid.add_column(vertical="middle")
            cells.append(get_card(face, card_dict["set"], card_dict["rarity"].strip()))
        grid.add_row(*cells)
        console.print(grid)
    else:
        console.print(get_card(card_dict, card_dict["set"], card_dict["rarity"].strip()))

    console.print(card_dict["scryfall_uri"], style=st_link.format(card_dict["scryfall_uri"]))

if __name__ == '__main__':
    sys.exit(main())


