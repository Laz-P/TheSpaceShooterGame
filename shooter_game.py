#Create your own shooter
from random import randint
from pygame import *
from time import time as timer
font.init()
font1 = font.Font(None,80)
win = font1.render("YOU WIN!",True,(255,255,255))
lose = font1.render("YOU LOSE!",True,(180,0,0))

font2 = font.Font(None,36)
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
img_enemy = "ufo.png"
img_back = "galaxy.jpg"
img_hero = "icon.png"
img_bullet = "bullet.png"
img_beamstrike = "Beamstrike.png"
img_ast = "asteroid.png"
score = 0
lost = 0
max_lost = 10
charge = 1
life = 3
beams = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x += self.speed

    def fire(self):
        global charge

        bullet1 = Bullet(img_bullet,self.rect.centerx-30,self.rect.y+30,15,20,-15)
        bullet2 = Bullet(img_bullet,self.rect.centerx+20,self.rect.y+30,15,20,-15)

        bullets.add(bullet1)
        bullets.add(bullet2)
        charge += 1
        

        if charge >= 10:
            beam = Beam(
                img_beamstrike,
                self.rect.centerx-40,
                self.rect.top-540,
                120, 600,
                0
            )

            beams.add(beam)   # <-- important
            charge = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        self.rect.x += randint(-(self.speed+10),(self.speed+10))
        global lost
        if self.rect.y >  win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost = lost +1
bullets = sprite.Group()
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
class Beam(GameSprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.timer = 10   # frames

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load(img_back),(win_width,win_height))
ship = Player(img_hero,5,win_height-100,80,100,10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(2):
    asteroid = Enemy(img_ast,randint(30,win_width-30),-40,80,50,randint(1,7))
    asteroids.add(asteroid)
finish = False
run = True
rel_time = False
goal = 20
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            if num_fire < 5 and not rel_time:
                num_fire += 1
                fire_sound.play()
                ship.fire()
            if num_fire >= 5 and not rel_time:
                last_time = timer()
                rel_time = True

    if not finish:
        window.blit(background,(0,0))   
        ship.update()
        ship.reset()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        beams.draw(window)
        beams.update()
        if rel_time:
            now_time = timer()
            if now_time - last_time <3:
                reload_text = font2.render("Wait, reload...",True,(150,0,0))
                window.blit(reload_text,(260,460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        beamcollides = sprite.groupcollide(monsters,beams,True,False)
        for b in beamcollides:
            score += 1
            monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        asteroidbeamcollision = sprite.groupcollide(asteroids,beams,True,False)
        for a in asteroidbeamcollision:
            asteroid = Enemy(img_ast,randint(30,win_width - 30),-40,80,50,randint(1,7))
        if sprite.spritecollide(ship,monsters, False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life -= 1
        if life ==0 or lost >= max_lost:
            finish = True
            won_check = False
            window.blit(lose,(200,200))
        if score >= goal:
            finish = True
            won_check = True
            window.blit(win,(200,200))
        text = font2.render("Score: " + str(score),1,(255,255,255))
        window.blit(text,(10,20))
        text_lose = font2.render("Missed: " + str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))
        text_goal = font2.render("Goal: "+ str(goal),1,(255,255,255))
        window.blit(text_goal,(10,80))
        text_charged = font2.render("Charge: "+ str(charge),1,(0,100,255))
        window.blit(text_charged,(200,20))
        life_color = (0,150,0) if life == 3 else (150,150,0) if life ==2 else (150,0,0)
        text_life = font1.render(str(life),True,life_color)
        window.blit(text_life,(650,10))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        charge = 0
        num_fire = 0
        life = 3
        if won_check == True:
            goal += 1
        for a in asteroids:
            a.kill()
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        for i in range(2):
            asteroid = Enemy(img_ast,randint(30,win_width - 30),-40,80,50,randint(1,7))
            asteroids.add(asteroid)


    time.delay(50)     
