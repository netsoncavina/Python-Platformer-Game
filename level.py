import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player

class Level:
    def __init__(self,level_data,surface):
        # Level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
    
    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        # Encontrando onde o "X" está
        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                if cell=='X':
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < (screen_width / 4) and direction_x < 0: # Precisa ter passado de 1/4 da tela e estar se movendo para a esquerda
            self.world_shift = 5
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0: # Precisa ter passado de 3/4 da tela e estar se movendo para a direita
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def run(self):
        # Level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        # Player
        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()
