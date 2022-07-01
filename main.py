import random

import pygame, sys
from button import Button
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pic=[pygame.image.load("images/red_win.png"),
     pygame.image.load("images/main_menu.png"),
     pygame.image.load("images/blue_win.png"),
     pygame.image.load("images/main_menu_blue.png"),
     ]
WIDTH = 800
HEIGHT = 650
SIZE = 50
FPS = 60
DIRECTIONS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tanki 1990")

bg = pygame.mixer.Sound('music/Фон.mp3')
bg.set_volume(0.1)

s = pygame.mixer.Sound('music/выстрел.mp3')
s.set_volume(0.1)

bonus = pygame.mixer.Sound('music/bonus.mp3')
bonus.set_volume(0.1)

def win(color='red', hex='#c61500', picture=[pic[0], pic[1]]):

    PLAYER2_BUTTON = Button(image=picture[0], pos=(420, 250),
                            text_input=f"{color.upper()} ПОБЕДИЛ", font=get_font(52), base_color=hex)
    PLAYER1_BUTTON = Button(image=picture[1], pos=(420, 450),
                            text_input="НАЧАТЬ ЗАНОВО", font=get_font(34), base_color=hex, hovering_color="white")
    QUIT_BUTTON = Button(image=picture[1], pos=(420, 570),
                         text_input="ГЛАВНОЕ МЕНЮ", font=get_font(37), base_color=hex, hovering_color="white")
    while True:
        SCREEN.fill('black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for button in [PLAYER2_BUTTON, PLAYER1_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bg.stop()
                if PLAYER2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player2()
                if PLAYER1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player2()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/font.ttf", size)


def player2():


    while True:
        admin = False
        field = []
        for x in range(0, 850, 50):
            for y in range(0, 700, 50):
                if x < 800 and y == 0:
                    pass
                else:
                    field.append((x, y))


        # Создаем игру и окно
        pygame.display.set_caption("Tanki 1990")
        clock = pygame.time.Clock()

        tanks = [
            pygame.image.load('images/tank1.png'),
            pygame.image.load('images/tank2.png')
        ]
        bangs = [
            pygame.image.load('images/Sprite-Boom-1.png'),
            pygame.image.load('images/Sprite-Boom-2.png'),
            pygame.image.load('images/Sprite-Boom-3.png'),
        ]
        block_textures = [
            'images/Sprite-Wall-2.png',
            'images/Sprite-Wall-2-1.png',
            'images/Sprite-Wall-2-2.png',
            'images/Sprite-Wall-One-Block.png'
        ]
        image = block_textures[0]
        fontInfo = pygame.font.Font(None, 40)

        class Tank:
            def __init__(self, color, px, py, direct, key_list):
                objects.append(self)
                self.type = 'tank'
                self.color = color
                self.rect = pygame.Rect(px, py, SIZE, SIZE)
                self.direct = direct
                self.move_speed = 2
                self.hp = 5
                self.bonus = 0
                self.shot_timer = 0
                self.shot_lag = 60
                self.timer = 180
                self.bullet_damage = 1
                self.bullet_speed = 5

                self.key_left = key_list[0]
                self.key_right = key_list[1]
                self.key_up = key_list[2]
                self.key_down = key_list[3]
                self.key_shot = key_list[4]
                field.remove((px, py))
                self.tanks = 0
                self.image = pygame.transform.rotate(tanks[self.tanks], -self.direct * 90)
                self.rect = self.image.get_rect(center=self.rect.center)

            def update(self):
                if self.color == 'blue':
                    self.image = pygame.transform.rotate(tanks[0], -self.direct * 90)
                    self.image = pygame.transform.scale(self.image,
                                                        (self.image.get_width() - 5, self.image.get_height() - 5))
                    self.rect = self.image.get_rect(center=self.rect.center)
                elif self.color == 'red':
                    self.image = pygame.transform.rotate(tanks[1], -self.direct * 90)
                    self.image = pygame.transform.scale(self.image,
                                                        (self.image.get_width() - 5, self.image.get_height() - 5))
                    self.rect = self.image.get_rect(center=self.rect.center)

                oldX, oldY = self.rect.topleft
                if self.rect.top == 50 and self.rect.left == 0:
                    if keys[self.key_right]:
                        self.rect.x += self.move_speed
                        self.direct = 1
                    elif keys[self.key_down]:
                        self.rect.y += self.move_speed
                        self.direct = 2
                elif self.rect.top == 50:
                    if keys[self.key_left]:
                        self.rect.x -= self.move_speed
                        self.direct = 3
                    elif keys[self.key_right]:
                        self.rect.x += self.move_speed
                        self.direct = 1
                    elif keys[self.key_down]:
                        self.rect.y += self.move_speed
                        self.direct = 2
                elif self.rect.left == 0:
                    if keys[self.key_right]:
                        self.rect.x += self.move_speed
                        self.direct = 1
                    elif keys[self.key_down]:
                        self.rect.y += self.move_speed
                        self.direct = 2
                    elif keys[self.key_up]:
                        self.rect.y -= self.move_speed
                        self.direct = 0
                elif self.rect.right == 800:
                    if keys[self.key_left]:
                        self.rect.x -= self.move_speed
                        self.direct = 3
                    elif keys[self.key_down]:
                        self.rect.y += self.move_speed
                        self.direct = 2
                    elif keys[self.key_up]:
                        self.rect.y -= self.move_speed
                        self.direct = 0
                elif self.rect.bottom == 650:
                    if keys[self.key_right]:
                        self.rect.x += self.move_speed
                        self.direct = 1
                    elif keys[self.key_left]:
                        self.rect.x -= self.move_speed
                        self.direct = 3
                    elif keys[self.key_up]:
                        self.rect.y -= self.move_speed
                        self.direct = 0
                else:
                    if keys[self.key_right]:
                        self.rect.x += self.move_speed
                        self.direct = 1
                    elif keys[self.key_left]:
                        self.rect.x -= self.move_speed
                        self.direct = 3
                    elif keys[self.key_up]:
                        self.rect.y -= self.move_speed
                        self.direct = 0
                    elif keys[self.key_down]:
                        self.rect.y += self.move_speed
                        self.direct = 2

                # условие столкновения танков
                for obj in objects:
                    if obj != self and self.rect.colliderect(obj.rect) and obj.type != 'bonus':
                        self.rect.topleft = oldX, oldY

                if keys[self.key_shot] and self.shot_timer == 0:
                    dx = DIRECTIONS[self.direct][0] * self.bullet_speed
                    dy = DIRECTIONS[self.direct][1] * self.bullet_speed
                    Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bullet_damage)
                    self.shot_timer = self.shot_lag

                if self.shot_timer > 0:
                    self.shot_timer -= 1
                if self.bonus == 1:
                    if self.timer > 0:
                        self.timer -= 1
                        self.move_speed = 3
                    else:
                        self.timer = 180
                        self.bonus = 0
                        self.move_speed = 2

            def draw(self):
                SCREEN.blit(self.image, self.rect)

            def damage(self, value):
                self.hp -= value
                if self.hp <= 0:
                    objects.remove(self)
                    if self.color == 'blue':
                        win('red', '#c61500')
                    if self.color == 'red':
                        win('blue', '#0077c7', [pic[2],pic[3]])
                    print(self.color, 'dead')

            def cords(self):
                return [self.rect.centerx, self.rect.centery]

        class Bullet:
            def __init__(self, father, px, py, dx, dy, damage):
                bullets.append(self)
                self.father = father
                self.px = px
                self.py = py
                self.dx = dx
                self.dy = dy
                self.damage = damage

            def update(self):
                self.px += self.dx
                self.py += self.dy

                if self.px < 0 or self.px > WIDTH or self.py < 50 or self.py > HEIGHT:
                    bullets.remove(self)
                else:
                    for obj in objects:
                        if obj != self.father and obj.rect.collidepoint(self.px, self.py) and obj.type != 'bonus':
                            obj.damage(self.damage)
                            bullets.remove(self)
                            Bang(self.px, self.py)
                            break

            def draw(self):
                pygame.draw.circle(SCREEN, 'white', (self.px, self.py), 4)

        class Block:
            def __init__(self, px, py, size, hp, image, direct):
                objects.append(self)
                if admin:
                    field.append((px,py))
                self.type = 'block'
                self.px = px
                self.py = py
                self.hp = hp
                self.img = image
                self.rect = pygame.Rect(px, py, size, size)
                self.image = pygame.image.load(image)
                self.direct = direct
                self.image = pygame.transform.rotate(self.image, -self.direct * 90)
                field.remove((px, py))

            def update(self):
                pass

            def draw(self):

                SCREEN.blit(self.image, self.rect)

            def damage(self, value):
                self.hp -= value
                if self.hp <= 0:
                    objects.remove(self)

            def __str__(self):
                return f"Block({self.px}, {self.py}, SIZE, {self.hp}, '{self.img}', {self.direct})"

        class Info:
            def __init__(self):
                pass

            def update(self):
                pass

            def draw(self):
                i = 0
                for obj in objects:
                    if obj.type == 'tank':
                        pygame.draw.rect(SCREEN, obj.color, (5 + i * 100, 5, 30, 30))
                        text = fontInfo.render(str(obj.hp), 1, obj.color)
                        rect = text.get_rect(center=(5 + i * 100 + 40, 10 + 11))
                        SCREEN.blit(text, rect)
                        i += 1
                if admin:
                    admin_text = fontInfo.render('admin', 1, 'red')
                    rect_admin = text.get_rect(center=(5 + 2.1 * 100 + 40, 10 + 11))
                    SCREEN.blit(admin_text, rect_admin)
                    texture_area = pygame.Rect(5 + 2 * 100, 5, 30, 30)
                    texture = pygame.image.load(image)
                    texture = pygame.transform.scale(texture,
                                                     (texture.get_width() - 15, texture.get_height() - 15))
                    SCREEN.blit(texture, texture_area)

        class Bonus:
            def __init__(self, px, py, type):
                objects.append(self)
                self.type = 'bonus'
                self.rect = pygame.Rect(px, py, SIZE, SIZE)
                self.image = [pygame.image.load('images/bonushp.png'), pygame.image.load('images/bonusspped.png')]
                self.timer = 900
                self.bonus_type = type
                self.player1 = [px, py]
                self.player2 = [px, py]

            def update(self):
                if self.timer > 0:
                    if self.rect.centerx - 25 <= self.player1[0] <= self.rect.centerx + 25 and self.rect.centery - 25 <= \
                            self.player1[1] <= self.rect.centery + 25:
                        objects.remove(self)

                        for obj in objects:
                            if obj.type == 'tank' and obj.color == 'blue':
                                bonus.play()
                                if self.bonus_type == 0:
                                    if obj.hp >= 5:
                                        obj.hp += 1
                                    else:
                                        obj.hp = 5
                                elif self.bonus_type == 1:
                                    obj.bonus = 1
                    elif self.rect.centerx - 25 <= self.player2[0] <= \
                            self.rect.centerx + 25 and self.rect.centery - 25 <= self.player2[1] <= self.rect.centery + 25:
                        objects.remove(self)
                        for obj in objects:
                            bonus.play()
                            if obj.type == 'tank' and obj.color == 'red':
                                if self.bonus_type == 0:
                                    if obj.hp >= 5:
                                        obj.hp += 1
                                    else:
                                        obj.hp = 5
                                elif self.bonus_type == 1:
                                    obj.bonus = 1
                    self.timer -= 1
                else:
                    objects.remove(self)

            def draw(self):
                SCREEN.blit(self.image[self.bonus_type], self.rect)

        class Bang:
            def __init__(self, px, py):
                objects.append(self)
                self.type = 'bang'
                self.rect = pygame.Rect(px, py, 20, 20)
                self.px, self.py = px, py
                self.frame = 0


            def update(self):
                s.play()
                self.frame += 0.2
                if self.frame >= 3:
                    objects.remove(self)

            def draw(self):
                image = bangs[int(self.frame)]
                rect = image.get_rect(center=(self.px, self.py))
                SCREEN.blit(image, rect)



        bullets = []
        objects = []
        p1 = Tank('blue', 0, 50, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
        p2 = Tank('red', 750, 600, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP0))
        info = Info()

        Block(0, 100, SIZE, 1, 'images/Sprite-Wall-One-Block.png', 0)
        Block(50, 50, SIZE, 3, 'images/Sprite-Wall-2-1.png', 1)
        Block(100, 50, SIZE, 3, 'images/Sprite-Wall-2.png', 1)
        Block(150, 50, SIZE, 3, 'images/Sprite-Wall-2.png', 1)
        Block(200, 50, SIZE, 3, 'images/Sprite-Wall-2-2.png', 3)
        Block(200, 100, SIZE, 3, 'images/Sprite-Wall-2.png', 0)
        Block(200, 150, SIZE, 3, 'images/Sprite-Wall-2.png', 0)
        Block(200, 200, SIZE, 3, 'images/Sprite-Wall-2-1.png', 0)
        Block(350, 50, SIZE, 3, 'images/Sprite-Wall-2-2.png', 2)
        Block(350, 100, SIZE, 3, 'images/Sprite-Wall-2.png', 0)
        Block(350, 150, SIZE, 3, 'images/Sprite-Wall-2.png', 0)
        Block(350, 200, SIZE, 3, 'images/Sprite-Wall-2-1.png', 0)
        Block(400, 50, SIZE, 3, 'images/Sprite-Wall-2.png', 1)
        Block(450, 50, SIZE, 3, 'images/Sprite-Wall-2.png', 1)
        Block(500, 50, SIZE, 3, 'images/Sprite-Wall-2-2.png', 3)
        Block(500, 100, SIZE, 3, 'images/Sprite-Wall-2.png', 0)
        Block(500, 150, SIZE, 3,'images/Sprite-Wall-2.png', 0)
        Block(500, 200, SIZE, 3, 'images/Sprite-Wall-2-1.png', 0)
        Block(700, 50, SIZE, 3, 'images/Sprite-Wall-2-1.png', 1)
        Block(750, 50, SIZE, 3, 'images/Sprite-Wall-2-2.png', 3)
        Block(750, 100, SIZE, 3, 'images/Sprite-Wall-2.png', 0)
        Block(750, 150, SIZE, 3, 'images/Sprite-Wall-2.png', 0)
        Block(750, 200, SIZE, 3, 'images/Sprite-Wall-2-1.png', 0)
        Block(650, 300, SIZE, 2, 'images/Sprite-Wall-2-1.png', 2)
        Block(650, 350, SIZE, 2, 'images/Sprite-Wall-2-1.png', 0)
        Block(450, 300, SIZE, 1,'images/Sprite-Wall-One-Block.png', 0)
        Block(300, 350, SIZE, 1, 'images/Sprite-Wall-One-Block.png', 0)
        Block(100, 350, SIZE, 2, 'images/Sprite-Wall-2-1.png', 0)
        Block(100, 300, SIZE, 2, 'images/Sprite-Wall-2-1.png', 2)
        Block(750, 550, SIZE, 1, 'images/Sprite-Wall-One-Block.png', 0)
        Block(700, 600, SIZE, 2, 'images/Sprite-Wall-2-1.png', 3)
        Block(650, 600, SIZE, 2, 'images/Sprite-Wall-2.png', 1)
        Block(600, 600, SIZE, 2, 'images/Sprite-Wall-2.png', 1)
        Block(550, 600, SIZE, 2, 'images/Sprite-Wall-2-2.png', 1)
        Block(550, 550, SIZE, 2, 'images/Sprite-Wall-2.png', 0)
        Block(550, 500, SIZE, 2, 'images/Sprite-Wall-2.png', 0)
        Block(550, 450, SIZE, 2, 'images/Sprite-Wall-2-1.png', 2)
        Block(400, 600, SIZE, 2, 'images/Sprite-Wall-2-2.png', 0)
        Block(400, 550, SIZE, 2, 'images/Sprite-Wall-2.png', 0)
        Block(400, 500, SIZE, 2, 'images/Sprite-Wall-2.png', 0)
        Block(400, 450, SIZE, 2, 'images/Sprite-Wall-2-1.png', 2)
        Block(350, 600, SIZE, 2, 'images/Sprite-Wall-2.png', 1)
        Block(300, 600, SIZE, 2, 'images/Sprite-Wall-2.png', 1)
        Block(250, 600, SIZE, 2, 'images/Sprite-Wall-2-2.png', 1)
        Block(250, 550, SIZE, 2, 'images/Sprite-Wall-2.png', 0)
        Block(250, 500, SIZE, 2, 'images/Sprite-Wall-2.png', 0)
        Block(250, 450, SIZE, 2, 'images/Sprite-Wall-2-1.png', 2)
        Block(50, 600, SIZE, 2, 'images/Sprite-Wall-2-1.png', 3)
        Block(0, 600, SIZE, 2, 'images/Sprite-Wall-2-2.png', 1)
        Block(0, 550, SIZE, 2, 'images/Sprite-Wall-2.png', 0)
        Block(0, 500, SIZE, 2, 'images/Sprite-Wall-2.png', 0)
        Block(0, 450, SIZE, 2, 'images/Sprite-Wall-2-1.png', 2)
        # блоки за страницей снизу
        Block(0, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(50, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(100, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(150, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(200, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(250, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(300, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(350, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(400, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(450, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(500, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(550, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(600, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(650, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(700, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(750, 650, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        # блоки за страницей справа
        Block(800, 600, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 550, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 500, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 450, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 400, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 350, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 300, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 250, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 200, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 150, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 100, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 50, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        Block(800, 0, SIZE, 1000, 'images/Sprite-Wall-2.png', 0)
        timer = 1080
        play = True
        rand = random.randint(0, len(field) - 1)
        b1 = Bonus(field[rand][0], field[rand][1], random.randint(0, 1))

        while play:
            if timer != 0:
                timer -= 1
            else:
                rand = random.randint(0, len(field) - 1)
                b1 = Bonus(field[rand][0], field[rand][1], random.randint(0, 1))
                timer = 1080
            b1.player1 = p1.cords()
            b1.player2 = p2.cords()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.QUIT



            # глобальная переменная для обращения изнутри
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                for obj in objects:
                    if obj.type == 'block':
                        print(obj)
                main_menu()

            if keys[pygame.K_m] and keys[pygame.K_i] and keys[pygame.K_n]:
                admin = not admin
                i = 4
                j = 4
                z = 4
                t = 1
            if admin:
                if keys[pygame.K_1]:
                    image = block_textures[0]
                if keys[pygame.K_2]:
                    image = block_textures[1]
                if keys[pygame.K_3]:
                    image = block_textures[2]
                if keys[pygame.K_4]:
                    image = block_textures[3]

                if keys[pygame.K_z]:
                    for obj in objects:
                        if obj.type == 'block' and obj.px == pygame.mouse.get_pos()[0]-pygame.mouse.get_pos()[0]%50 \
                                and obj.py == pygame.mouse.get_pos()[1]-pygame.mouse.get_pos()[1]%50:
                            if z > 0:
                                z -= 1
                            else:
                                print(obj)
                                obj.img = image
                                obj.image = pygame.image.load(image)
                                z = 4
                if keys[pygame.K_x]:
                    for obj in objects:
                        if obj.type == 'block' and obj.px == pygame.mouse.get_pos()[0]-pygame.mouse.get_pos()[0]%50 \
                                and obj.py == pygame.mouse.get_pos()[1]-pygame.mouse.get_pos()[1]%50:
                            if z > 0:
                                z -= 1
                            else:
                                t+=1
                                print(obj)
                                obj.image = pygame.transform.rotate(obj.image,  -t * 90)
                                z = 4
                if pygame.mouse.get_pressed()[0]:
                        if i > 0:
                            i -= 1
                        else:

                            Block(pygame.mouse.get_pos()[0] - pygame.mouse.get_pos()[0] % 50,pygame.mouse.get_pos()[1] - pygame.mouse.get_pos()[1] % 50,SIZE, 1,'images/Sprite-Wall-2.png', 0)
                            i = 4
                        print(pygame.mouse.get_pos()[0] - pygame.mouse.get_pos()[0] % 50,pygame.mouse.get_pos()[1] - pygame.mouse.get_pos()[1] % 50, i)

                if keys[pygame.K_DELETE]:
                        print(pygame.mouse.get_pos())
                        for obj in objects:
                            if obj.type == 'block' and obj.px == pygame.mouse.get_pos()[0]-pygame.mouse.get_pos()[0]%50 \
                                and obj.py == pygame.mouse.get_pos()[1]-pygame.mouse.get_pos()[1]%50:
                                if j > 0:
                                    j -= 1
                                else:
                                    objects.remove(obj)
                                    j = 4


            for bullet in bullets:
                bullet.update()

            for obj in objects:
                obj.update()
            info.update()

            SCREEN.fill('black')

            for obj in objects:
                obj.draw()

            for bullet in bullets:
                bullet.draw()

            info.draw()
            pygame.display.update()
            clock.tick(FPS)


        pygame.display.update()
        for obj in objects:
            if obj.type == 'block':
                print(obj)

def player1(color):
    pygame.init()

    # Создаем игру и окно
    pygame.display.set_caption("Tanki 1990")
    clock = pygame.time.Clock()
    fontInfo = pygame.font.Font(None, 40)
    bangs = [
        pygame.image.load('images/Sprite-Boom-1.png'),
        pygame.image.load('images/Sprite-Boom-2.png'),
        pygame.image.load('images/Sprite-Boom-3.png'),
    ]
    tanks = [
        pygame.image.load('images/tank1.png'),
        pygame.image.load('images/tank2.png')
    ]

    class Tank:
        def __init__(self, color, px, py, direct, key_list):
            objects.append(self)
            self.type = 'tank'
            self.color = color
            self.rect = pygame.Rect(px, py, SIZE, SIZE)
            self.direct = direct
            self.move_speed = 2
            self.hp = 5

            self.shot_timer = 0
            self.shot_lag = 60

            self.bullet_damage = 1
            self.bullet_speed = 5

            self.key_left = key_list[0]
            self.key_right = key_list[1]
            self.key_up = key_list[2]
            self.key_down = key_list[3]
            self.key_shot = key_list[4]

            self.tanks = 0
            self.image = pygame.transform.rotate(tanks[self.tanks], -self.direct * 90)
            self.rect = self.image.get_rect(center=self.rect.center)

        def update(self):
            if self.color == 'blue':
                self.image = pygame.transform.rotate(tanks[0], -self.direct * 90)
                self.image = pygame.transform.scale(self.image,
                                                    (self.image.get_width() - 5, self.image.get_height() - 5))
                self.rect = self.image.get_rect(center=self.rect.center)
            elif self.color == 'red':
                self.image = pygame.transform.rotate(tanks[1], -self.direct * 90)
                self.image = pygame.transform.scale(self.image,
                                                    (self.image.get_width() - 5, self.image.get_height() - 5))
                self.rect = self.image.get_rect(center=self.rect.center)

            oldX, oldY = self.rect.topleft
            if self.rect.top == 50 and self.rect.left == 0:
                if keys[self.key_right]:
                    self.rect.x += self.move_speed
                    self.direct = 1
                elif keys[self.key_down]:
                    self.rect.y += self.move_speed
                    self.direct = 2
            elif self.rect.top == 50:
                if keys[self.key_left]:
                    self.rect.x -= self.move_speed
                    self.direct = 3
                elif keys[self.key_right]:
                    self.rect.x += self.move_speed
                    self.direct = 1
                elif keys[self.key_down]:
                    self.rect.y += self.move_speed
                    self.direct = 2
            elif self.rect.left == 0:
                if keys[self.key_right]:
                    self.rect.x += self.move_speed
                    self.direct = 1
                elif keys[self.key_down]:
                    self.rect.y += self.move_speed
                    self.direct = 2
                elif keys[self.key_up]:
                    self.rect.y -= self.move_speed
                    self.direct = 0
            elif self.rect.right == 800:
                if keys[self.key_left]:
                    self.rect.x -= self.move_speed
                    self.direct = 3
                elif keys[self.key_down]:
                    self.rect.y += self.move_speed
                    self.direct = 2
                elif keys[self.key_up]:
                    self.rect.y -= self.move_speed
                    self.direct = 0
            elif self.rect.bottom == 650:
                if keys[self.key_right]:
                    self.rect.x += self.move_speed
                    self.direct = 1
                elif keys[self.key_left]:
                    self.rect.x -= self.move_speed
                    self.direct = 3
                elif keys[self.key_up]:
                    self.rect.y -= self.move_speed
                    self.direct = 0
            else:
                if keys[self.key_right]:
                    self.rect.x += self.move_speed
                    self.direct = 1
                elif keys[self.key_left]:
                    self.rect.x -= self.move_speed
                    self.direct = 3
                elif keys[self.key_up]:
                    self.rect.y -= self.move_speed
                    self.direct = 0
                elif keys[self.key_down]:
                    self.rect.y += self.move_speed
                    self.direct = 2

            # условие столкновения танков
            for obj in objects:
                if obj != self and self.rect.colliderect(obj.rect):
                    self.rect.topleft = oldX, oldY

            if keys[self.key_shot] and self.shot_timer == 0:
                dx = DIRECTIONS[self.direct][0] * self.bullet_speed
                dy = DIRECTIONS[self.direct][1] * self.bullet_speed
                Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bullet_damage, 'white')
                self.shot_timer = self.shot_lag

            if self.shot_timer > 0:
                self.shot_timer -= 1

        def draw(self):
            SCREEN.blit(self.image, self.rect)

        def damage(self, value):
            self.hp -= value
            if self.hp <= 0:
                objects.remove(self)
                print(self.color, 'dead')

        def cords(self):
            return [self.rect.left, self.rect.right, self.rect.bottom, self.rect.top]

    class Turret:
        def __init__(self, color, px, py, direct, enemy):
            objects.append(self)
            self.type = 'Turret'
            self.color = color
            self.rect = pygame.Rect(px, py, SIZE, SIZE)
            self.direct = direct
            self.hp = 3
            self.enemy = enemy
            self.shot_timer = 0
            self.shot_lag = 60

            self.bullet_damage = 1
            self.bullet_speed = 6

            self.tanks = 0
            self.image = pygame.transform.rotate(pygame.image.load('images/Turret.png'), -self.direct * 90)
            self.rect = self.image.get_rect(center=self.rect.center)

        def damage(self, value):
            self.hp -= value
            if self.hp <= 0:
                objects.remove(self)
                print(self.color, 'dead')

        def draw(self):
            SCREEN.blit(self.image, self.rect)

        def shoot(self):
            dx = DIRECTIONS[self.direct][0] * self.bullet_speed
            dy = DIRECTIONS[self.direct][1] * self.bullet_speed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bullet_damage, 'white')
            self.shot_timer = self.shot_lag

        def update(self):
            if self.color == 'red':
                self.image = pygame.transform.rotate(pygame.image.load('images/Turret.png'), -self.direct * 90)
                self.rect = self.image.get_rect(center=self.rect.center)

            if self.rect.top <= self.enemy[2] and self.rect.bottom >= self.enemy[3] and self.rect.left >= self.enemy[1]:
                self.direct = 3
                if self.shot_timer == 0:
                    self.shoot()
            elif self.rect.top <= self.enemy[2] and self.rect.bottom >= self.enemy[3] and self.rect.right <= self.enemy[
                0]:
                self.direct = 1
                if self.shot_timer == 0:
                    self.shoot()
            elif self.rect.right >= self.enemy[0] and self.rect.left <= self.enemy[1] and self.rect.top >= self.enemy[2]:
                self.direct = 0
                if self.shot_timer == 0:
                    self.shoot()
            elif self.rect.right >= self.enemy[0] and self.rect.left <= self.enemy[1] and self.rect.bottom <= \
                    self.enemy[3]:
                self.direct = 2
                if self.shot_timer == 0:
                    self.shoot()

            if self.shot_timer > 0:
                self.shot_timer -= 1

    class Bullet:
        def __init__(self, father, px, py, dx, dy, damage, color):
            bullets.append(self)
            self.father = father
            self.px = px
            self.py = py
            self.dx = dx
            self.dy = dy
            self.damage = damage
            self.color = color

        def update(self):
            self.px += self.dx
            self.py += self.dy

            if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
                bullets.remove(self)
            else:
                for obj in objects:
                    if obj != self.father and obj.rect.collidepoint(self.px,
                                                                    self.py) and not obj.type == 'block_turret' \
                            and not obj.type == 'bang':
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.px, self.py)

                    elif obj != self.father and obj.rect.collidepoint(self.px, self.py) and obj.type == 'block_turret':
                        if self.father.type == 'tank':
                            obj.damage(self.damage)
                            bullets.remove(self)
                            Bang(self.px, self.py)

                        else:
                            break

        def draw(self):
            pygame.draw.circle(SCREEN, self.color, (self.px, self.py), 4)

    class Defender:
        def __init__(self, px, py, size, hp, image, direct):
            objects.append(self)
            self.type = 'block_turret'
            self.rect = pygame.Rect(px, py, size, size)
            self.hp = hp
            self.image = image
            self.direct = direct
            self.image = pygame.transform.rotate(self.image, -self.direct * 90)

        def update(self):
            pass

        def draw(self):
            SCREEN.blit(self.image, self.rect)

        def damage(self, value):
            self.hp -= value
            if self.hp <= 0:
                objects.remove(self)

    class Block:
        def __init__(self, px, py, size, hp, image, direct):
            objects.append(self)
            self.type = 'block'
            self.rect = pygame.Rect(px, py, size, size)
            self.hp = hp
            self.image = image
            self.direct = direct
            self.image = pygame.transform.rotate(self.image, -self.direct * 90)

        def update(self):
            pass

        def draw(self):
            SCREEN.blit(self.image, self.rect)

        def damage(self, value):
            self.hp -= value
            if self.hp <= 0:
                objects.remove(self)

    class Info:
        def __init__(self):
            pass

        def update(self):
            pass

        def draw(self):

            i = 0
            for obj in objects:
                if obj.type == 'tank':
                    pygame.draw.rect(SCREEN, obj.color, (5 + i * 100, 5, 30, 30))
                    text = fontInfo.render(str(obj.hp), 1, obj.color)
                    rect = text.get_rect(center=(5 + i * 100 + 40, 10 + 11))
                    SCREEN.blit(text, rect)
                    i += 1

    class Bang:
        def __init__(self, px, py):
            objects.append(self)
            self.type = 'bang'
            self.rect = pygame.Rect(px, py, 20, 20)
            self.px, self.py = px, py
            self.frame = 0

        def update(self):
            s.play()
            self.frame += 0.2
            if self.frame >= 3:
                objects.remove(self)

        def draw(self):
            image = bangs[int(self.frame)]
            rect = image.get_rect(center=(self.px, self.py))
            SCREEN.blit(image, rect)



    bullets = []
    objects = []
    t = []
    p1 = Tank(color, 0, 50, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
    t.append(Turret('red', 400, 300, 0, p1.cords()))
    t.append(Turret('red', 450, 250, 0, p1.cords()))
    t.append(Turret('red', 300, 200, 0, p1.cords()))
    t.append(Turret('red', 350, 350, 0, p1.cords()))
    t.append(Turret('red', 500, 400, 0, p1.cords()))
    info = Info()


    for x in range(100, 700, 50):
        Block(x, 100, SIZE, 2, pygame.image.load('images/Sprite-Wall-2.png'), 1)
        Block(x, 550, SIZE, 2, pygame.image.load('images/Sprite-Wall-2.png'), 1)

    for y in range(50, 650, 50):
        Block(50, y, SIZE, 2, pygame.image.load('images/Sprite-Wall-2.png'), 0)
        Block(700, y, SIZE, 2, pygame.image.load('images/Sprite-Wall-2.png'), 0)

    Defender(350, 300, SIZE, 3, pygame.image.load('images/Sprite-Wall-One-Block.png'), 0)
    Defender(450, 300, SIZE, 3, pygame.image.load('images/Sprite-Wall-One-Block.png'), 0)
    Defender(400, 250, SIZE, 3, pygame.image.load('images/Sprite-Wall-One-Block.png'), 0)
    Defender(400, 350, SIZE, 3, pygame.image.load('images/Sprite-Wall-One-Block.png'), 0)
    # блоки за страницей снизу
    Block(0, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(50, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(100, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(150, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(200, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(250, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(300, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(350, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(400, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(450, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(500, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(550, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(600, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(650, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(700, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(750, 650, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    # блоки за страницей справа
    Block(800, 600, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 550, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 500, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 450, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 400, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 350, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 300, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 250, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 200, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 150, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 100, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 50, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)
    Block(800, 0, SIZE, 1000, pygame.image.load('images/Sprite-Wall-2.png'), 0)


    play = True
    while play:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                play = False


        # глобальная переменная для обращения изнутри
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            main_menu()

        for bullet in bullets:
            bullet.update()

        for obj in objects:
            for i in range(len(t)):
                t[i].enemy = p1.cords()

            obj.update()



        SCREEN.fill('black')

        for obj in objects:
            obj.draw()

        for bullet in bullets:
            bullet.draw()

        info.draw()
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

def choice():
    RED = Button(image=pygame.image.load("images/red.png"), pos=(250, 300),
                 text_input="", font=get_font(37), base_color="white", hovering_color="#0c7fba")
    BLUE = Button(image=pygame.image.load("images/blue.png"), pos=(550, 300),
                  text_input="", font=get_font(37), base_color="white", hovering_color="#0c7fba")
    QUIT_BUTTON = Button(image=pygame.image.load("images/exit.png"), pos=(400, 550),
                         text_input="НАЗАД", font=get_font(37), base_color="white", hovering_color="#0c7fba")
    while True:

        SCREEN.fill('black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("ВЫБЕРИТЕ ТАНК", True, "white")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 70))



        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [RED, BLUE, QUIT_BUTTON]:
            if button == QUIT_BUTTON:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)
            else:
                button.change_position(MENU_MOUSE_POS, SCREEN)
                button.update(SCREEN)




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RED.checkForInput(MENU_MOUSE_POS):
                    player1('red')
                if BLUE.checkForInput(MENU_MOUSE_POS):
                    player1('blue')
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.fill('black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        bg.play()
        MENU_TEXT = get_font(50).render("ТАНКИ  1990", True, "white")
        MENU_RECT = MENU_TEXT.get_rect(center=(420, 70))

        PLAYER2_BUTTON = Button(image=pygame.image.load("images/2p.png"), pos=(420, 200),
                             text_input="2 ИГРОКА", font=get_font(37), base_color="white", hovering_color="#0c7fba")
        PLAYER1_BUTTON = Button(image=pygame.image.load("images/1p.png"), pos=(420, 350),
                                text_input="1 ИГРОК", font=get_font(37), base_color="white", hovering_color="#0c7fba")
        QUIT_BUTTON = Button(image=pygame.image.load("images/exit.png"), pos=(420, 500),
                             text_input="ВЫХОД", font=get_font(37), base_color="white", hovering_color="#0c7fba")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAYER2_BUTTON, PLAYER1_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bg.stop()
                if PLAYER2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player2()
                if PLAYER1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    choice()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
