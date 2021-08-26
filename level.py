import pygame
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from settings import tile_size, screen_width
from player import Player
from particles import ParticleEffect
from support import import_csv_layout, import_cut_graphics
from decoration import Sky

class Level:
    def __init__(self,level_data,surface):
        # Level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = -4
        self.current_x = 0

        # Terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        # Grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')

        # Crates setup
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout,'crates')

        # Coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')

        # Foreground palms
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg palms')

        # Background palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout,'bg palms')

        # Enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

        # Constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraints')

        # Decoration
        self.sky = Sky(8)


        # Dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
    
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == 'crates':
                        sprite = Crate(tile_size,x,y)
                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size,x,y,'graphics\coins\gold')
                        else:
                            sprite = Coin(tile_size,x,y,'graphics\coins\silver') 
                    if type == 'fg palms':
                        if val == '0':
                            sprite = Palm(tile_size,x,y,'graphics/terrain/palm_small',38)
                        else:
                            sprite = Palm(tile_size,x,y,'graphics/terrain/palm_large',64)
                    if type == 'bg palms':
                        sprite = Palm(tile_size,x,y,'graphics/terrain/palm_bg',64)
                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)
                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)
                    sprite_group.add(sprite)



        return sprite_group

    # def create_jump_particles(self,pos):
    #     if self.player.sprite.facing_right:
    #         pos -= pygame.math.Vector2(10,5)
    #     else:
    #         pos += pygame.math.Vector2(10,-5)
    #     jump_particle_sprite = ParticleEffect(pos, 'jump')
    #     self.dust_sprite.add(jump_particle_sprite)

    # def get_player_on_ground(self):
    #     if self.player.sprite.on_ground:
    #         self.player_on_ground = True
    #     else:
    #         self.player_on_ground = False
    
    # def create_landing_dust(self):
    #     if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
    #         if self.player.sprite.facing_right:
    #             offset = pygame.math.Vector2(10,15)
    #         else:
    #             offset = pygame.math.Vector2(-10,15)
    #         fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
    #         self.dust_sprite.add(fall_dust_particle)


    # Talvez apagavel
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
                    player_sprite = Player((x,y), self.display_surface,self.create_jump_particles)
                    self.player.add(player_sprite)

    # def scroll_x(self):
    #     player = self.player.sprite
    #     player_x = player.rect.centerx
    #     direction_x = player.direction.x

    #     if player_x < (screen_width / 4) and direction_x < 0: # Precisa ter passado de 1/4 da tela e estar se movendo para a esquerda
    #         self.world_shift = 5
    #         player.speed = 0
    #     elif player_x > screen_width - (screen_width / 4) and direction_x > 0: # Precisa ter passado de 3/4 da tela e estar se movendo para a direita
    #         self.world_shift = -5
    #         player.speed = 0
    #     else:
    #         self.world_shift = 0
    #         player.speed = 5

    # def horizontal_movement_collision(self):
    #     player = self.player.sprite
        
    #     player.rect.x += player.direction.x * player.speed
    #     # Testes de colisão horizontal
    #     for sprite in self.tiles.sprites():
    #         if sprite.rect.colliderect(player.rect):
    #             if player.direction.x < 0:
    #                 player.rect.left = sprite.rect.right
    #                 player.on_left = True
    #                 self.current_x = player.rect.left
    #             elif player.direction.x > 0:
    #                 player.rect.right = sprite.rect.left
    #                 player.on_right = True
    #                 self.current_x = player.rect.right

    #     if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
    #         player.on_left = False
    #     if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
    #         player.on_right = False
    
    # def vertical_movement_collision(self):
    #     player = self.player.sprite
    #     player.apply_gravity()

    #     for sprite in self.tiles.sprites():
    #         if sprite.rect.colliderect(player.rect):
    #             if player.direction.y > 0:
    #                 player.rect.bottom = sprite.rect.top
    #                 player.direction.y = 0 # Reseta a gravidade
    #                 player.on_ground = True
    #             elif player.direction.y < 0:
    #                 player.rect.top = sprite.rect.bottom
    #                 player.direction.y = 0 # Evita que "grude" no teto
    #                 player.on_ceiling = True
        
    #     if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
    #         player.on_ground = False
    #     if player.on_ceiling and player.direction.y > 0:
    #         player.on_ceiling = False

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse_speed()

    def run(self):
       # Dust Particles
        # self.dust_sprite.update(self.world_shift)
        # self.dust_sprite.draw(self.display_surface)
       
        

        # Sky
        self.sky.draw(self.display_surface)
        
        #   Level tiles
        # Bg Palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # Terrain tiles
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface) 

        # Enemies
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        
        # Crate tiles
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface) 

        # Grass tiles
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface) 

        # Coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # Fg Palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        


      

        # self.tiles.draw(self.display_surface)
        # self.scroll_x()

        # # Player
        # self.player.update()
        # self.horizontal_movement_collision()
        # self.get_player_on_ground()
        # self.vertical_movement_collision()
        # self.create_landing_dust()
        # self.player.draw(self.display_surface)
        
