import os
import pygame

from effects.weapon_effects import Weapon
from effects.magic_effects import MagicPlayer
from effects.particle_effects import AnimationPlayer

from configs.game.weapon_config import weapon_data
from configs.game.spell_config import magic_data


class CombatHandler:

    def __init__(self):

        # Setup Combat
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        self.current_attack = None

        # Spell and Weapon Rotation
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]

        # Damage Timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 300

        # Import Sounds
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         asset_path = os.path.join(
#             script_dir, '../../..', 'assets', 'audio')
#
#         self.weapon_attack_sound = pygame.mixer.Sound(
#             f"{asset_path}/sword.wav")
#         self.weapon_attack_sound.set_volume(0.2)

    def create_attack_sprite(self, player):
        self.current_attack = Weapon(
            player, [player.visible_sprites, player.attack_sprites])

    def delete_attack_sprite(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic_sprite(self, player, style, strength, cost):
        print(style)
        if style == 'heal':
            self.magic_player.heal(player, strength, cost, [
                                   player.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(
                player, cost, [player.visible_sprites, player.attack_sprites])
