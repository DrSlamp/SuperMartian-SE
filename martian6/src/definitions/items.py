"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition for items.
"""
from typing import Dict, Any

import random

from gale.timer import Timer

import settings
from src.GameItem import GameItem

from src.Player import Player


def pickup_coin(
    coin: GameItem, player: Player, points: int, color: int, time: float, time1: float
) -> None:
    settings.SOUNDS["pickup_coin"].stop()
    settings.SOUNDS["pickup_coin"].play()
    player.score += points
    player.coins_counter[color] += 1
    Timer.after(time, lambda: coin.respawn())
    Timer.after(time1, lambda: coin.despawn())


def pickup_green_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 1, 62, random.uniform(2, 4), random.uniform(2, 6) )


def pickup_blue_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 5, 61, random.uniform(5, 8), 10000)


def pickup_red_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 20, 55, random.uniform(10, 18), 10000)


def pickup_yellow_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 50, 54, random.uniform(20, 25), 10000)

def pickup_yellow_key(coin: GameItem, player: Player):
        for _ in range(3):
            pickup_coin(coin, player, 1, 68, 1, 1)
        


def pickup_block_key(coin: GameItem, player: Player):
    print("sacando llave")
    pickup_coin(coin,player,1, 62, 0.001, 4)
   
    
   
     #coin.despawn()
    




ITEMS: Dict[str, Dict[int, Dict[str, Any]]] = {
    "coins": {
        62: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_green_coin,
        },
        61: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_blue_coin,
        },
        55: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_red_coin,
        },
        54: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_yellow_coin,
        },
         68: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_yellow_key,
        },
         34: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=True, left=False),
            "consumable": True,
            "collidable": True,
            "on_collide": pickup_block_key,
        },
         

    }
}



