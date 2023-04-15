"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""
from typing import Dict, Any

import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Camera import Camera
from src.GameLevel import GameLevel
from src.Player import Player



class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level", 1)
        self.camera = enter_params.get(
            "camera", Camera(0, 0, settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        )
        self.game_level = enter_params.get("game_level")
        if self.game_level is None:
            self.game_level = GameLevel(self.level, self.camera)
            pygame.mixer.music.load(settings.BASE_DIR / "sounds/music_grassland.ogg")
            pygame.mixer.music.play(loops=-1)

        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")
        if self.player is None:
            self.player = Player(0, settings.VIRTUAL_HEIGHT - 66, self.game_level)
            self.player.change_state("idle")

        self.timer = enter_params.get("timer", 30)
        self.time_bonus = enter_params.get("time_bonus", 4)
        #Flags
        self.flag = enter_params.get("flag",False) 
        self.time_bonus_flag = enter_params.get("time_bonus_flag",False) 


        def countdown_timer():
            self.timer -= 1
            # self.a1 = 20

            if 0 < self.timer <= 5:
                settings.SOUNDS["timer"].play()

            if self.timer == 0:
                self.player.change_state("dead")
        
            if self.player.score >= 10:
                 print("tiene 10 monedas")
                 
        def bonus_countdown_timer():
            self.time_bonus -= 1
            # print(self.time_bonus)
            if self.time_bonus < 1:
                self.time_bonus_flag = False
                 
                

        Timer.every(1, countdown_timer)
        # if self.time_bonus_flag: 
        Timer.every(1, bonus_countdown_timer)
        InputHandler.register_listener(self)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)
        Timer.clear()

    def update(self, dt: float) -> None:
        if self.player.is_dead:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.state_machine.change("game_over", self.player)

        self.player.update(dt)
    
        if self.player.y >= self.player.tilemap.height:
            self.player.change_state("dead")

        
            

        if self.player.score >= 3000:
           
           self.state_machine.change("play1")

        if self.player.coins_counter[68] == 4: #win 

           self.state_machine.change("play1")

      

        self.camera.x = max(
            0,
            min(
                self.player.x + 8 - settings.VIRTUAL_WIDTH // 2,
                self.tilemap.width - settings.VIRTUAL_WIDTH,
            ),
        )
        self.camera.y = max(
            0,
            min(
                self.player.y + 10 - settings.VIRTUAL_HEIGHT // 2,
                self.tilemap.height - settings.VIRTUAL_HEIGHT,
            ),
        )

        self.game_level.update(dt)

        for creature in self.game_level.creatures:
            if self.player.collides(creature):
                self.player.change_state("dead")

        for item in self.game_level.items:
            if not item.in_play or not item.collidable:
                continue 
                
            if self.player.collides(item):
                if item.consumable:
                    item.on_consume(self.player)
                if item.collidable:
                    item.on_collide(self.player)
                if item.collidable and not item.consumable:
                    self.game_level.items[-2].collidable = False 
                    self.game_level.items[-2].consumable = False
                    self.game_level.items[68].in_play = True
                

      

    def render(self, surface: pygame.Surface) -> None:
        world_surface = pygame.Surface((self.tilemap.width, self.tilemap.height))
        self.game_level.render(world_surface)
        self.player.render(world_surface)
        surface.blit(world_surface, (-self.camera.x, -self.camera.y))

        

        render_text(
            surface,
            f"LEVEL {self.level} - Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Keys: {self.player.coins_counter[68]}",
            settings.FONTS["small"],
            15,
            15,
            (255, 255, 0),
            shadowed=True,
        )
        b1 = f" "
        
        
        if self.player.score >= 40:
            if self.time_bonus_flag:
                b1 = f"+20 •  "
            else:
                b1 = f" "

       

                
             
        # little power up ;)  add +20 seconds, time remain.       
        if (self.player.score >= 40) and not self.flag:
            self.timer = self.timer + 20
            self.flag = True
            self.time_bonus = 4 
            self.time_bonus_flag = True
            
               
        render_text(
            surface,
            f"Time :{b1}{ self.timer }",
            settings.FONTS["verysmall"],
            settings.VIRTUAL_WIDTH - 100,
            5,
            (255, 255, 255),
            shadowed=True,
        
           
        )
        
        
    

        render_text(
            surface,
            f"Find 4 keys or  ",
            settings.FONTS["verysmall"],
            settings.VIRTUAL_WIDTH // 2,
            2,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f" DIE",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2+ 70,
            2,
            (255, 0, 0),
            shadowed=True,
        )
        

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "pause",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                timer=self.timer,
                time_bonus=self.time_bonus,
                time_bonus_flag = self.time_bonus_flag,
                flag = self.flag,
            )
