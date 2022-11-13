import pygame
import random
from pygame.constants import USEREVENT
from handle_score import write_score

from pygame.time import set_timer
from wall import Wall

import json

import sys, os
script_dir = sys.path[0]

#Sprite loading
spaceship = os.path.join(script_dir, './assets/sprite/spaceship.png')
spaceship_accelerate = os.path.join(script_dir, './assets/sprite/spaceship_accelerate.png')
multishot = os.path.join(script_dir, './assets/sprite/multishot.png')
ricochet = os.path.join(script_dir, './assets/sprite/ricochet.png')

wall_x = os.path.join(script_dir, './assets/sprite/wall_x.png')
wall_y = os.path.join(script_dir, './assets/sprite/wall_y.png')

enemy = os.path.join(script_dir, './assets/sprite/enemy.png')
enemy2 = os.path.join(script_dir, './assets/sprite/enemy2.png')

coin = os.path.join(script_dir, './assets/sprite/coin.png')
boost = os.path.join(script_dir, './assets/sprite/boost.png')

bkg_sprite = os.path.join(script_dir, './assets/sprite/bkg.png')
projectile = os.path.join(script_dir, './assets/sprite/projectile.png')
projectile2 = os.path.join(script_dir, './assets/sprite/projectile_2.png')

#Audio loading 
blaster_sound = os.path.join(script_dir, './assets/audio/blaster_sound.mp3') 
explosion_sound = os.path.join(script_dir, './assets/audio/explosion_sound.mp3')

#Audio play function 
def blast():
    blast = pygame.mixer.Sound(blaster_sound)
    blast.play()
def explosion():
    explosion = pygame.mixer.Sound(explosion_sound)
    explosion.play()

#Open settings.json
with open('settings.json', 'r') as f:
    settings = json.load(f)
wall_prop = settings["wall_properties"]
em1_range = settings["enemy_1_shoot_range"]

pygame.init()

screen_rect = pygame.Rect((0, 0), (800, 600))
myfont = pygame.font.SysFont("monospace", 16)
screen = pygame.display.set_mode((800, 600))

state = [pygame.image.load(spaceship).convert_alpha(), pygame.image.load(spaceship_accelerate).convert_alpha(),pygame.image.load(multishot).convert_alpha(),pygame.image.load(ricochet).convert_alpha()]

#The wall props are : x_len, y_len, x_pos, y_pos in that order 

list_wall = []
for wall in wall_prop:
    list_wall.append(Wall(wall, wall_x, wall_y))
wall_group = pygame.sprite.Group()
        
for wall in list_wall:
    wall_group.add(wall)


#    ------------------------- GAME CLASSES -------------------------


# ------------------------- Shooter1 (attack by shooting) -------------------------

class Shooter(pygame.sprite.Sprite):
    def __init__(self, PLAYER):
        super().__init__()
        #self.image = pygame.Surface((32, 32))
        self.image = pygame.image.load(enemy).convert_alpha()
        self.org_image = self.image.copy()
        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.rect = self.image.get_rect(center=(random.randint(0,800), random.randint(0,600)))
        self.pos = pygame.Vector2(self.rect.center)
        self.x_y = random.randint(0,1) 
        self.health = 2
        self.vel = 5
        self.last = pygame.time.get_ticks()
        self.cooldown = 2000 
        self.PLAYER = PLAYER
        for wall in list_wall:
            if wall.rect.colliderect(self.rect) :
                self.pos.x = random.randint(0,800)
                self.pos.y = random.randint(0,800)
                self.rect.center = self.pos
                
                
    def update(self,x = 0,y = 0):
        if self.x_y == 0:
            self.angle = 0
            self.pos.x += self.vel 
            self.rect.center = self.pos
            if self.pos.x >= 800 or self.pos.x <= 0:
                self.vel *= -1
            for wall in list_wall:
                if self.rect.colliderect(wall):
                    self.vel *= -1
        if self.x_y == 1:
            self.angle = 90
            self.pos.y += self.vel
            self.rect.center = self.pos
            if self.pos.y >= 600 or self.pos.y <= 0:
                self.vel *= -1
            for wall in list_wall:
                if self.rect.colliderect(wall):
                    self.vel *= -1
        if self.health <= 0:
            self.kill()
            explosion()
            death_count = pygame.time.set_timer(pygame.USEREVENT+7, 500, True)
        if x-em1_range <= self.pos.x <= x+em1_range or y-em1_range <= self.pos.y <= y+em1_range :
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown:
                self.last = now
                try:
                    self.groups()[0].add(Projectile2(self.PLAYER, self.rect.center, self.direction.normalize()))
                    self.groups()[0].add(Projectile2(self.PLAYER,self.rect.center, self.direction.normalize().rotate(90)))
                    self.groups()[0].add(Projectile2(self.PLAYER,self.rect.center, self.direction.normalize().rotate(180)))
                    self.groups()[0].add(Projectile2(self.PLAYER,self.rect.center, self.direction.normalize().rotate(270)))
                except IndexError as e: 
                    print(e)
                    pass

# ------------------------- Chaser (attack by chasing players)) -------------------------

class Chaser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(enemy2).convert_alpha()
        self.org_image = self.image.copy()
        self.rect = self.image.get_rect(center=(random.randint(0,800), random.randint(0,600)))
        self.pos = pygame.Vector2(self.rect.center)
        self.health = 3
        self.vel = 2
        self.cooldown = 2000
        for wall in list_wall:
            if wall.rect.colliderect(self.rect) :
                self.pos.x = random.randint(0,0)
                self.pos.y = random.randint(0,0)
                self.rect.center = self.pos
    def update(self, player):
        direction = pygame.math.Vector2(player.rect.x - self.rect.x,player.rect.y - self.rect.y)
        direction.normalize()
        direction.scale_to_length(self.vel)
        self.rect.move_ip(direction)

        if self.rect.colliderect(player):
            player.health -= 2
            explosion()
            self.kill()
        
        if self.health <= 0:
            self.kill()
            explosion()
            death_count = pygame.time.set_timer(pygame.USEREVENT+7, 500, True)

# ------------------------- Coin (counts towards the score) -------------------------

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(coin).convert_alpha()
        self.rect = self.image.get_rect(center=(random.randint(0,800), random.randint(0,600)))
        self.pos = pygame.Vector2(self.rect.center)
        
        for wall in list_wall:
            if wall.rect.colliderect(self.rect) :
                self.pos.x = random.randint(0,800)
                self.pos.y = random.randint(0,600)
                self.rect.center = self.pos  
   
# ------------------------- Boost (grant special abilities) -------------------------

class Boost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(boost).convert_alpha()
        self.type = random.choice(['multishot', 'accelerate','ricochet'])
        self.rect = self.image.get_rect(center=(random.randint(0,800), random.randint(0,600)))
        self.pos = pygame.Vector2(self.rect.center)
        for wall in list_wall:
            if wall.rect.colliderect(self.rect) :
                self.pos.x = random.randint(0,800)
                self.pos.y = random.randint(0,600)
                self.rect.center = self.pos

def handle_boost(player_object, boost_object):
    if player_object.rect.colliderect(boost_object):
        boost_object.kill()
        if boost_object.type == "multishot" :
            activating_time = pygame.time.set_timer(pygame.USEREVENT+1,5000,True)
            player_object.multishot = True
            player_object.image = state[2]
            player_object.org_image = player_object.image.copy()
        elif boost_object.type == "accelerate" :
            activating_time = pygame.time.set_timer(pygame.USEREVENT+4,5000,True)
            player_object.image = state[1]
            player_object.org_image = player_object.image.copy()
            player_object.vel = 8
        else :
            activating_time = pygame.time.set_timer(pygame.USEREVENT+5,5000,True)
            player_object.ricochet = True
            player_object.image = state[3]
            player_object.org_image = player_object.image.copy()

# ------------------------- The player in control -------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, COIN_GROUP, BOOST_GROUP, ENEMY_1, ENEMY_2):
        super().__init__()
        self.image = state[0]
        self.org_image = self.image.copy()
        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.rect = self.image.get_rect(center=(200, 200))
        self.pos = pygame.Vector2(self.rect.center)
        self.multishot = False
        self.ricochet = False
        self.health = 10
        self.vel = 4
        self.coin = 0
        self.last = 0
        self.COIN_GROUP = COIN_GROUP
        self.BOOST_GROUP = BOOST_GROUP
        self.ENEMY_1 = ENEMY_1
        self.ENEMY_2 = ENEMY_2
    def update(self, events, dt):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if not self.multishot and not self.ricochet :
                        self.groups()[0].add(Projectile(self.rect.center, self.direction.normalize(), self.ENEMY_1, self.ENEMY_2))
                    elif self.ricochet :
                        self.multishot = False
                        self.groups()[0].add(Projectile(self.rect.center, self.direction.normalize(), self.ENEMY_1, self.ENEMY_2 ,ricochet=True))
                    elif self.multishot :
                        self.ricochet = False
                        self.groups()[0].add(Projectile(self.rect.center, self.direction.normalize(), self.ENEMY_1, self.ENEMY_2))
                        direction_1 = self.direction.normalize().rotate(30)
                        direction_2 = self.direction.normalize().rotate(330)
                        self.groups()[0].add(Projectile(self.rect.center, direction_1, self.ENEMY_1, self.ENEMY_2))
                        self.groups()[0].add(Projectile(self.rect.center, direction_2, self.ENEMY_1, self.ENEMY_2))
            if e.type == pygame.USEREVENT+1 :
                if self.multishot :
                    self.multishot = False
                    self.image = state[0]
                    self.org_image = self.image.copy()
            if e.type == pygame.USEREVENT+4:
                self.vel = 4
                self.image = state[0]
                self.org_image = self.image.copy()
            if e.type == pygame.USEREVENT+5:
                if self.ricochet:
                    self.ricochet = False
                    self.image = state[0]
                    self.org_image = self.image.copy()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a] :
            self.angle = 180
            self.pos.x -= self.vel 
            self.rect.center = self.pos
            self.rect.clamp_ip(screen_rect)
            for wall in list_wall:
                if self.rect.colliderect(wall):
                    self.pos.x += self.vel   
            for i in self.BOOST_GROUP:
                handle_boost(self,i)
            for i in self.COIN_GROUP:
                if self.rect.colliderect(i):
                    self.coin += 1
                    i.kill()
        if pressed[pygame.K_d]:
            self.angle = 0
            self.pos.x += self.vel
            self.rect.center = self.pos
            self.rect.clamp_ip(screen_rect)
            for wall in list_wall:
                if self.rect.colliderect(wall):
                    self.pos.x -= self.vel
            for i in self.BOOST_GROUP:
                if self.rect.colliderect(i):
                    handle_boost(self,i)
            for i in self.COIN_GROUP:
                if self.rect.colliderect(i):
                    self.coin += 1
                    i.kill()
        if pressed[pygame.K_w]:
            self.angle = 90
            self.pos.y -= self.vel
            self.rect.center = self.pos
            self.rect.clamp_ip(screen_rect)
            for wall in list_wall:
                if self.rect.colliderect(wall):
                    self.pos.y += self.vel
            for i in self.BOOST_GROUP:
                handle_boost(self, i)

            for i in self.COIN_GROUP:
                if self.rect.colliderect(i):
                    self.coin += 1
                    i.kill()
            
        if pressed[pygame.K_s]:
            self.angle = -90
            self.pos.y += self.vel
            self.rect.center = self.pos
            self.rect.clamp_ip(screen_rect)
            for wall in list_wall:
                if self.rect.colliderect(wall):
                    self.pos.y -= self.vel
            for i in self.BOOST_GROUP:
                handle_boost(self,i)
            for i in self.COIN_GROUP:
                if self.rect.colliderect(i):
                    self.coin += 1
                    i.kill()
    
        if pressed[pygame.K_e]:
            self.angle -= 3

        if pressed[pygame.K_q]:
            self.angle += 3                       

        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.health <= 0:
            self.kill()
            explosion()
            death = pygame.time.set_timer(pygame.USEREVENT+6, 1000, True)

        if self.coin % 5 == 0 and self.coin != self.last :
            self.health += 1
            self.last = self.coin

# ------------------------- Projectile (shoot enemies only) -------------------------

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, ENEMY_1, ENEMY_2, size=(8,8), ricochet = False):
        super().__init__()
        self.image = pygame.image.load(projectile).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)
        self.ricochet = ricochet
        self.bounce_num = 7
        self.enemy = list(ENEMY_1) + list(ENEMY_2)
        blast()
    def update(self, events, dt):
        if not self.ricochet :
            self.pos += self.direction * dt
            self.rect.center = self.pos
            if not pygame.display.get_surface().get_rect().contains(self.rect):
                self.kill()
            for wall in list_wall:
                if self.rect.colliderect(wall):
                    self.kill()
            for enemy in self.enemy:
                if self.rect.colliderect(enemy) and (isinstance(enemy, Chaser) or isinstance(enemy, Shooter) ):
                    enemy.health -= 1
                    self.kill()
        else :
            self.pos += self.direction * dt
            if not pygame.display.get_surface().get_rect().contains(self.rect):
                self.bounce_num -= 1
            if self.bounce_num == 0:
                return self.kill()

            if self.pos.x > screen_rect.right or self.pos.x < screen_rect.left:
                self.direction.x *= -1

            if self.pos.y > screen_rect.bottom or self.pos.y < screen_rect.top:
                self.direction.y *= -1
            
            for wall in list_wall:
                if self.rect.colliderect(wall):
                    self.bounce_num -= 1
                    

            next_pos = self.pos + self.direction * dt
        
            self.pos = next_pos
            self.rect.center = self.pos

            for enemy in self.enemy:
                if self.rect.colliderect(enemy) and isinstance(enemy, Shooter) or isinstance(enemy, Chaser):
                    enemy.health -= 1
                    self.kill()
        
# ------------------------- Projectile 2 (shoot player only) -------------------------

class Projectile2(pygame.sprite.Sprite):
    def __init__(self, PLAYER, pos, direction,size=(8,8)):
        super().__init__()
        self.image = pygame.image.load(projectile2).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)
        self.PLAYER = PLAYER

    def update(self, events, dt):
        self.pos += self.direction * 5
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
        for wall in list_wall:
            if self.rect.colliderect(wall):
                self.kill()
        if self.rect.colliderect(self.PLAYER):
            self.PLAYER.health -= 1
            self.kill()

def game():
    '''
    USEREVENT 
    0 :boost group
    1 :multishot
    2 coin group
    3 enemies
    '''
    
    enemies_type_1 = pygame.sprite.Group()
    enemies_type_2 = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()    
    boost_group = pygame.sprite.Group()    


    player = Player(coin_group, boost_group, enemies_type_1, enemies_type_2)
    sprites = pygame.sprite.Group()
    sprites.add(player)

    
    enemies_type_1.add(Shooter(player))
    enemies_type_2.add(Chaser())
    
    coin_group.add(Coin())    
    boost_group.add(Boost())

    RUNNING = True
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Galaxy Traveller")
    enemy_spawn = pygame.time.set_timer(pygame.USEREVENT+3, 8000)
    bkg = pygame.image.load(bkg_sprite).convert_alpha()
    bkg = pygame.transform.scale(bkg,(800,600))
    clock = pygame.time.Clock()
    dt = 0
    boost = pygame.time.set_timer(pygame.USEREVENT, 10000)
    coin_spawn = pygame.time.set_timer(pygame.USEREVENT + 2, 5000)
    cooldown_tracker = 0
    kills = 0
    while RUNNING:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT or e.type == pygame.USEREVENT + 6:
                write_score(player.coin + kills*2)
                return pygame.QUIT
            if e.type == pygame.USEREVENT :
                boost_group.add(Boost())
            if e.type == pygame.USEREVENT + 2 :
                coin_group.add(Coin())
            if e.type == pygame.USEREVENT + 3:
                enemies_type_1.add(Shooter(player))
                enemies_type_2.add(Chaser())
            if e.type == pygame.USEREVENT + 7:
                kills += 1

        sprites.update(events, dt)
        screen.blit(bkg,(0,0))
        sprites.draw(screen)
        boost_group.draw(screen)
        coin_group.draw(screen)

        enemies_type_1.draw(screen)
        enemies_type_1.update(player.pos.x,player.pos.y)
        enemies_type_2.draw(screen)
        enemies_type_2.update(player)

        wall_group.draw(screen)
        scoretext = myfont.render("Coin = "+str(player.coin)+" Life points = " +str(player.health) +" Kills = "+str(kills), True, (225,225,225))
        screen.blit(scoretext, (10, 5))
        pygame.display.update()
        dt = clock.tick(60)

