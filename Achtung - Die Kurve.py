import pygame
import random
from Variables import *


pygame.init()

size = WIDTH, HEIGHT = 1000, 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((200, 200, 200))

power_modes = ["normal", "speed", "slow", "big", "90_turn"]

powerup_images = [pygame.image.load("Images/speed.jpg"), pygame.image.load("Images/slow.jpg"), pygame.image.load("Images/size.jpg"), pygame.image.load("Images/90_turn.jpg")]

class Powerup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mode = power_modes[random.randint(1, 4)]
        self.image = powerup_images[power_modes.index(self.mode) - 1]
        self.image = pygame.transform.scale(self.image, powerup_size)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.color = (0, 0, 0)
        for player in players:
            for rect in player.rects:
                if self.rect.colliderect(rect):
                    print("collided")
                    self.x = random.randint(25, WIDTH - 25)
                    self.y = random.randint(25, HEIGHT - 25)
                    self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.draw()
        self.collision()

    def collision(self):
        for player in players:
            for rect in player.rects:
                if self.rect.colliderect(rect):
                    pygame.draw.rect(screen, (200, 200, 200), 
                                    (self.x - self.image.get_width()/2, 
                                     self.y- self.image.get_height()/2, 
                                     self.image.get_width() + 1, self.image.get_height() + 1))
                    
                    powerups.remove(self)
                    pygame.draw.rect(screen, (player.color), rect)
                    pygame.display.flip()


class Player:
    def __init__(self, color, left, right, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.width = player_size[0]
        self.height = player_size[1]
        self.direction = (pygame.Vector2(WIDTH/2, HEIGHT/2) - pygame.Vector2(x, y)).normalize()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)
        self.rects = []
        self.invisible_time = 15
        self.mode = power_modes[0]
        self.power_time = powerup_duration
        self.left = left
        self.right = right

    def update(self):
        if self.mode == power_modes[0]:
            self.power_0()

        if self.mode == power_modes[1]:
            self.power_1()

        if self.mode == power_modes[2]:
            self.power_2()

        if self.mode == power_modes[3]:
            self.power_3()

        if self.mode == power_modes[4]:
            self.power_4()

        self.movement()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.invisible_time <= 0:
            self.draw()
            self.rects.append(self.rect)
        self.invisible_time -= 1

        if self.invisible_time <= -180:
            self.invisible_time = player_hole_duration

        if len(self.rects) > self.width * 2:
            self.collision()

        self.powerup_collision()
        self.outOfBounds()

    def power_0(self): #normal
        self.power_time = powerup_duration
        self.speed = player_speed
        self.rotation = player_rotation_speed
        self.width = player_size[0]
        self.height = player_size[1]
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.direction.rotate_ip(-self.rotation)
        if keys[self.right]:
            self.direction.rotate_ip(self.rotation)

    def power_1(self): #speed
        self.speed = player_speed * 2
        self.rotation = player_rotation_speed
        self.width = player_size[0]
        self.height = player_size[1]
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.direction.rotate_ip(-self.rotation)
        if keys[self.right]:
            self.direction.rotate_ip(self.rotation)
        self.power_time -= 1
        if self.power_time <= 0:
            self.mode = power_modes[0]
            self.power_time = powerup_duration

    def power_2(self): #slow
        self.speed = player_speed / 2
        self.rotation = player_rotation_speed
        self.width = player_size[0]
        self.height = player_size[1]
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.direction.rotate_ip(-self.rotation)
        if keys[self.right]:
            self.direction.rotate_ip(self.rotation)
        self.power_time -= 1
        if self.power_time <= 0:
            self.mode = power_modes[0]
            self.power_time = powerup_duration

    def power_3(self): #big
        self.speed = player_speed
        self.rotation = player_rotation_speed
        self.width = player_size[0] * 3
        self.height = player_size[1] * 3
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.direction.rotate_ip(-self.rotation)
        if keys[self.right]:
            self.direction.rotate_ip(self.rotation)
        self.power_time -= 1
        if self.power_time <= 0:
            self.mode = power_modes[0]
            self.power_time = powerup_duration

    def power_4(self): #90_turn
        self.speed = player_speed
        self.width = player_size[0]
        self.height = player_size[1]

        self.power_time -= 1
        if self.power_time <= 0:
            self.mode = power_modes[0]
            self.power_time = powerup_duration


    def movement(self):
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def outOfBounds(self):
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            pygame.quit()
            exit()

    def collision(self):
        for rect in self.rects[0: len(self.rects) - self.width * 2]:
            if self.rect.colliderect(rect):
                print("you killed yourself :(")
                pygame.quit()
                exit()
        for player in players:
            if player != self:
                for rect in player.rects:
                    if self.rect.colliderect(rect):
                        pygame.quit()
                        exit()

    def powerup_collision(self):
        for powerup in powerups:
            if self.rect.colliderect(powerup.rect):
                self.mode = powerup.mode


players = [
            Player((255, 0, 0), pygame.K_a, pygame.K_d, WIDTH/10, HEIGHT/10),
            #Player((0, 255, 0), pygame.K_LEFT, pygame.K_RIGHT, WIDTH - WIDTH/10, HEIGHT/10),
            #Player((0, 0, 255), pygame.K_o, pygame.K_p, WIDTH/10, HEIGHT - HEIGHT/10),
            #Player((255, 255, 0), pygame.K_v, pygame.K_b, WIDTH - WIDTH/10, HEIGHT - HEIGHT/10)
          ]

powerups = [Powerup(500, 500)]

power_up_spawn_time = powerup_spawn_rate


class Button:
    def __init__(self, x, y, width, height, text, text_size) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)
        self.text = text
        self.text_size = text_size

    def update(self):  
        self.draw()
        self.collision()

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        font = pygame.font.Font('freesansbold.ttf', self.text_size)
        text = font.render(self.text, True, (255, 255, 255))
        textRect = text.get_rect()
        #screen.blit(text, (self.x + self.width/2 - textRect.width/2, self.y + self.height/2 - textRect.height/2))
        screen.blit(text, (self.x - textRect.width/2, self.y - textRect.height/2))
        
    def collision(self, playerCount = Player_default_count):
        if pygame.mouse.get_pos()[0] > self.x - self.width/2 and pygame.mouse.get_pos()[0] < self.x + self.width and pygame.mouse.get_pos()[1] > self.y - self.height/2 and pygame.mouse.get_pos()[1] < self.y + self.height:
            if pygame.mouse.get_pressed()[0]:
                if self.text == "START":
                    game(power_up_spawn_time)
                if self.text == "+":
                    playerCount += 1
                    if playerCount > 4:
                        playerCount = 4
                    print(playerCount)
                if self.text == "-":
                    playerCount -= 1
                    if playerCount < 2:
                        playerCount = 2
                    print(playerCount)


def game(timer):
    screen.fill((200, 200, 200))
    while True:
        clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                for player in players:
                    if player.mode == power_modes[4]:
                        player.rotation = 90
                        if event.key == player.left:
                            player.direction.rotate_ip(-player.rotation)
                        if event.key == player.right:
                            player.direction.rotate_ip(player.rotation)
    
        clock.tick(60)

        timer -= 1
        if timer <= 0:
            powerups.append(Powerup(random.randint(25, WIDTH - 25), random.randint(25, HEIGHT - 25)))
            timer = power_up_spawn_time
        
        for player in players:       
            player.update()

        for powerup in powerups:
            powerup.update()

        pygame.display.flip()

def menu():
    buttons = [
                Button(WIDTH/2, 200, 500, 200, "START", 100), 
                Button(WIDTH/2, 500, 240, 50, "Player count", 32),
                Button(WIDTH/2 - 150, 500, 50, 50, "-", 32),
                Button(WIDTH/2 + 150, 500, 50, 50, "+", 32)
              ]
    
    while True:
        screen.fill((220, 220, 220))
        for button in buttons:
            button.update()
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

menu()



