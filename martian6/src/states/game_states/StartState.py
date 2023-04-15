"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class StartState.
"""
import pygame

from gale.animation import Animation
from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import Text, render_text
from gale.timer import Timer

import settings


class StartState(BaseState):
    def arrive(self):
        self.tweening = False
        self.martian_animation = Animation([settings.FRAMES["martian"][3]])

    def enter(self) -> None:
        self.title = Text(
            "Super Martian - SE",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH,
            settings.VIRTUAL_HEIGHT // 4,
            (117, 225, 20),
            shadowed=True,
        )
        self.title_end_x = settings.VIRTUAL_WIDTH // 2 - self.title.rect.width // 2
        
        self.martian_x = -16
        self.martian_end_x = settings.VIRTUAL_WIDTH // 2 - 8
        self.martian_texture = settings.TEXTURES["martian"]
        self.martian_animation = Animation(settings.FRAMES["martian"][9:], 0.15)

        self.tweening = True

        InputHandler.register_listener(self)
        pygame.mixer.music.load(settings.BASE_DIR / "sounds" / "music_intro.ogg")
        pygame.mixer.music.play()
        Timer.tween(
            5,
            [
                (self.title, {"x": self.title_end_x}),
                (self, {"martian_x": self.martian_end_x}),
            ],
            on_finish=self.arrive,
        )

    def exit(self) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        InputHandler.unregister_listener(self)

    def update(self, dt: float) -> None:
        self.martian_animation.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((25, 130, 196))
        self.title.render(surface)
        surface.blit(
            self.martian_texture,
            (self.martian_x, settings.VIRTUAL_HEIGHT // 2 - 10),
            self.martian_animation.get_current_frame(),
        )

        if not self.tweening:
            render_text(
                surface,
                "press ENTER",
                settings.FONTS["small"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2 + 25,
                (197, 195, 198),
                center=True,
                shadowed=True,
            )

            render_text(
                surface,
                f"Developers: @DrSlamp - @Coabest",
                settings.FONTS["small"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2 + 75,
                (255, 60, 255, 64),
                shadowed=True,
                center=True,
        )
        


    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            if self.tweening:
                Timer.clear()
                self.title.x = self.title_end_x
                self.martian_x = self.martian_end_x
                self.arrive()
            else:
                self.state_machine.change("play")
"""
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "2" and input_data.pressed:
            if self.tweening:
                Timer.clear()
                self.title.x = self.title_end_x
                self.martian_x = self.martian_end_x
                self.arrive()
            else:
                self.state_machine.change("play1")
"""