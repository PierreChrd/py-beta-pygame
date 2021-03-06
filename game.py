import pygame,pytmx,pyscroll
from player import Player

class Game:
    def __init__(self):
        # création fenetre
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("MMO - Beta")

        # charger la map.tmx
        tmx_data = pytmx.util_pygame.load_pygame('assets/carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        self.map = 'world'

        # générer un joueur
        player_spawn_point = tmx_data.get_object_by_name("spawnpoint")
        self.player = Player(player_spawn_point.x, player_spawn_point.y)

        #définir  une liste qui stock les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5)
        self.group.add(self.player)
            
        # définir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)


    def handle_input(self):
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation("up")
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation("down")
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation("left")
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation("right")


    def switch_house(self):
        # charger la map.tmx
        tmx_data = pytmx.util_pygame.load_pygame('assets/house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #définir  une liste qui stock les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5)
        self.group.add(self.player)

        # définir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # récuperer le point de spawn dans la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20


    def switch_world(self):
        # charger la map.tmx
        tmx_data = pytmx.util_pygame.load_pygame('assets/carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #définir  une liste qui stock les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5)
        self.group.add(self.player)

        # définir le rectangle de collision pour quitter la maison
        exit_house = tmx_data.get_object_by_name('exit_house')
        self.exit_house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        # récuperer le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 20


    def update(self):
        self.group.update()

        # vérifier l'entrer dans la maison
        if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'

        # vérifier l'entrer dans la maison
        if self.map == 'house' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = 'world'

        
        #vérification de lacollision:
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()


    def run(self):
        clock = pygame.time.Clock()

        # boucle du jeu
        running = True

        while running:

            # sauvegarde de la premiere position du joueur (pour les collisions)
            self.player.save_location()
            # enclanchement de hande_input
            self.handle_input()
            # actualisation de la position initiale du joueur
            self.update()
            # centrer la camera sur le joueur
            self.group.center(self.player.rect.center)
            # dessin de la carte
            self.group.draw(self.screen)
            pygame.display.flip() # actualiser

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # permet de définir le nombre de fps du jeu
            clock.tick(60)
        
        pygame.quit()