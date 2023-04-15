"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PauseState.
"""
from typing import Dict, Any

import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings


class PauseState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.camera = enter_params["camera"]
        self.game_level = enter_params["game_level"]
        self.tilemap = self.game_level.tilemap
        self.player = enter_params["player"]
        self.timer = enter_params["timer"]
        self.flag = enter_params["flag"]
        self.time_bonus = enter_params["time_bonus"]
        self.time_bonus_flag = enter_params["time_bonus_flag"]
        

        InputHandler.unregister_listener(self.player.state_machine.current)
        InputHandler.register_listener(self)
        pygame.mixer.music.pause()

    def exit(self) -> None:
        InputHandler.unregister_listener(self)
        InputHandler.register_listener(self.player.state_machine.current)
        pygame.mixer.music.unpause()

    def render(self, surface: pygame.Surface) -> None:
        world_surface = pygame.Surface((self.tilemap.width, self.tilemap.height))
        self.game_level.render(world_surface)
        self.player.render(world_surface)
        surface.blit(world_surface, (-self.camera.x, -self.camera.y))

        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.timer}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 60,
            5,
            (255, 255, 255),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        
        if input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "play",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                timer=self.timer,
                time_bonus=self.time_bonus,
                time_bonus_flag = self.time_bonus_flag,
                flag = self.flag,
            )
       
        elif input_id == "pause" and input_data.pressed:
                self.state_machine.change(
                "play1",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                timer=self.timer,
                time_bonus=self.time_bonus,
                time_bonus_flag = self.time_bonus_flag,
                flag = self.flag,
            )