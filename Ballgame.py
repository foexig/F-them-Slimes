import random
import math
import pygame
from pytmx.util_pygame import load_pygame
import os
import csv
import load_asset
from pygame import gfxdraw

# UI elemente
# Level System
# wand mit mauszeiger
# wenn ball schnell genug ist spur hinterherziehen ?
# toxic enemy (particels töten gegner oder machen dmg)
# mit leertaste nen boost ( jeder ball hat ulti die sich aufläd)
# grüner ball synergy mit grünem slime usw
#Roter ball macht devil splatter zu waffe
# drops ?
# wenn der rote ball mit der spur nen dämon fickt sprüht er selber nh dicke blase // bombe ( dropt AOE BOMBE )

# Ulti ideen :
# Größer werden
#Spur hinterher ziehen
#Giga boost
#klonen ?

# Charckter eigenschaften ideen :
# mehr Bounce
# Synergie mit schleim farbe

#merh bounce
pygame.init()
width = load_asset.width
height = load_asset.height
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball game")
clock = pygame.time.Clock()
pygame.mixer.music.load('416-8-bit-chiptune-instrumental-for-games-339237.mp3')
pygame.mixer.music.set_volume(0.1)

grey = (53 , 53 , 53 )
white = (255 , 255 , 255 )
black= (0 ,0 ,0 )
blue = (115 , 245 , 251)
green = ( 153 , 229 , 80)
dark_blue = (37 , 37 , 84)
red = (228 , 0 , 21 )

# ball colors
green_b = (88 , 190 , 60)
red_b = (206 , 29 , 29)
orange_b = (244 , 134 , 13 )
blue_b = (28 , 193 , 255 )

bounce_faktor = -3.5

def map_length_to_speed(length, max_length):

    clamped_length = max(0, min(length, max_length))
    return (clamped_length / max_length) * 30

explosion_list = []

class SplatterParticle:

    def __init__(self, pos, direction , speed , splatter_col ):

        self.x, self.y = pos
        self.drag = 0.97
        self.speed =  speed * random.uniform(0.7 , 0.9 )
        self.splatter_col_primary = splatter_col[0]
        self.splatter_col_secondary = splatter_col[1]
        # Basisrichtung normalisieren
        base_dir = direction.normalize() if direction.length() != 0 else pygame.math.Vector2(1, 0)
        # Leichter Zufallsstreuung ±30°
        angle_offset = random.uniform(-math.pi/6, math.pi/6)
        angle = math.atan2(base_dir.y, base_dir.x) + angle_offset

        self.vel = pygame.math.Vector2(math.cos(angle) * self.speed,
                                       math.sin(angle) * self.speed)
        self.life = random.randint(30, 120)

        self.color = self.splatter_col_primary
        if random.randrange(1 , 5) == 1 :
            self.color = self.splatter_col_secondary


    def update(self):

        self.x += self.vel.x
        self.y += self.vel.y

        if pygame.math.Vector2.length(self.vel) != 0 :
                self.vel *= self.drag
        if self.x <= 0 :
           self.x = 0
           self.vel.x *= -1
        elif self.x >= width:
            self.x = width
            self.vel.x *= -1
        if self.y <= 0:
            self.y = 0
            self.vel.y *= -1
        elif self.y >= height:
            self.y = height
            self.vel.y *= -1

        self.life -= 1

    def draw(self, surface, offset):
        if self.life > 0:
            pygame.draw.circle(surface,
                               self.color,
                               (int(self.x + offset[0]), int(self.y + offset[1])),
                               3)

class ExplosionParticle:
    def __init__(self , img , pos ):
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.x = pos[0]
        self.y = pos[1]

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def update(self):
        self.draw()


PLAYER_MAP = {
    "green_ball": (load_asset.GREEN_BALL, green_b),
    "red_ball": (load_asset.RED_BALL, red_b ),
    "orange_ball": (load_asset.ORANGE_BALL , orange_b),
    "blue_ball": (load_asset.BLUE_BALL ,blue_b),
}
def lerp( a , b , t ):
    return  a + (b - a) * t
# Klassen sind nicht nur objekte die im spiel angezigt werdern sondern können vile mehr wie kleine helfer das spiel strulturieren , Woah erst dachte ich warum hat die ULTSTate klasse kein __init__... geht aber das brauch es garnicht (war mir bsiher garnicht so klar gewesen )

class Player:
    def __init__(self, player_color , pos):
        self.player_img_orig , self.color = PLAYER_MAP[player_color]
        self.player_img = pygame.transform.scale_by(self.player_img_orig, 1.5)
        self.original_width , self.original_height = self.player_img_orig.get_size()
        self.rot_image = self.player_img
        self.rot_image_rect = self.player_img.get_rect(center=(8, 8))
        self.mask = pygame.mask.from_surface(self.player_img)
        self.x = pos[0]
        self.y = pos[1]
        self.vel = pygame.math.Vector2(0, 0)
        self.drag = 0.98
        self.bounce = False
        self.streak = 0

    def draw(self):
        screen.blit(self.rot_image, self.rot_image.get_rect(center=(self.x, self.y)))

    def check_out_of_bounds(self):
        if -1000 < self.x >= 1900:
            self.x = 0

        if -1000 < self.y >= 1900:
            self.y = 0

    def cap_velocity(self):
        if pygame.math.Vector2.length(self.vel) > 200:
            self.vel *= 0.25

    def apply_drag(self):
        if pygame.math.Vector2.length(self.vel) != 0 :
                self.vel *= self.drag

    def draw_line(self, first_mouse_pos):
        current_pos = pygame.mouse.get_pos()
        drag_vector = pygame.math.Vector2(current_pos) - pygame.math.Vector2(first_mouse_pos)
        stretch_height = max(int(self.original_height * (1 - (pygame.math.Vector2.length(drag_vector) * 0.0007))), 30)
        stretch_width = int(self.original_width * (1 + (pygame.math.Vector2.length(drag_vector) * 0.0003)))
        if 30 <= stretch_height >= 0:
            self.player_img = pygame.transform.smoothscale(self.player_img_orig, (stretch_width, stretch_height))
        drag_len = min(pygame.math.Vector2.length(drag_vector), 255)
        if drag_len < 128:
            # Von grün zu gelb
            r = int(2 * drag_len)
            g = 255
        else:
            # Von gelb zu rot
            r = 255
            g = int(255 - 2 * (drag_len - 128))
        b = 0
        base_color = (r, g, b)
        preview_end = pygame.math.Vector2(self.x, self.y) - drag_vector
        num_segments = 50

        for i in range(num_segments):
            t1 = i / num_segments
            t2 = (i + 1) / num_segments

            start = lerp((self.x, self.y), preview_end, t1)
            end = lerp((self.x, self.y), preview_end, t2)

            alpha = int(255 * (1 - t1))  # Am Anfang deckend, am Ende transparent
            color_with_alpha = (*base_color, alpha)
            pygame.draw.line(screen, color_with_alpha, start, end, width=5)

    def handle_wall_bounce(self):
        half_width = self.rot_image.get_width() // 2
        half_height = self.rot_image.get_height() // 2

        if self.x - half_width < 0:
            self.x = half_width
            if self.bounce:
                self.vel.x *= bounce_faktor
                self.vel.y += random.randint(-40, 40)
            else:
                self.vel.x *= -1
            pygame.mixer.Sound.play(load_asset.BOUNCE_SOUND)
        if self.x + half_width > width:
            self.x = width - half_width

            if self.bounce:
                self.vel.x *= bounce_faktor
                self.vel.y += random.randint(-40 , 40)
            else:
                self.vel.x *= -1
            pygame.mixer.Sound.play(load_asset.BOUNCE_SOUND)
        if self.y - half_height < 0:
            self.y = half_height
            if self.bounce:
                self.vel.y *= bounce_faktor
                self.vel.x += random.randint(-40, 40)
            else:
                self.vel.y *= -1
            pygame.mixer.Sound.play(load_asset.BOUNCE_SOUND)
        if self.y + half_height > height:
            self.y = height - half_height
            if self.bounce:
                self.vel.y *= bounce_faktor
                self.vel.x += random.randint(-40, 40)
            else:
                self.vel.y *= -1
            pygame.mixer.Sound.play(load_asset.BOUNCE_SOUND)
    def rotation_calc(self):
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.x, self.y - my  # dy ist invers wegen Bildschirmkoordinaten
        angle = math.degrees(math.atan2(dy, dx))
        self.rot_image = pygame.transform.rotate(self.player_img, angle)

    def update(self , mouse_down , first_mouse_pos):
        self.cap_velocity()
        self.apply_drag()
        self.check_out_of_bounds()
        self.handle_wall_bounce()
        self.rotation_calc()
        if mouse_down:

            self.draw_line(first_mouse_pos)
        else:
            self.player_img = self.player_img_orig

        self.x += self.vel.x
        self.y += self.vel.y

        self.draw()

    def apply_boost(self):
        self.vel *= 5

    def calc_speed(self, pos_old , pos_new):
        vector_mouse_def = pygame.math.Vector2(pos_new[0] - pos_old[0] ,pos_new[1] - pos_old[1] )
        len_vec = pygame.math.Vector2.length(vector_mouse_def)
        mapped_len = map_length_to_speed(len_vec , 20)

        if len_vec != 0:
            direction = vector_mouse_def.normalize()
            self.vel = -direction * (mapped_len  // 1.5)  # Rückstoß!

    def get_enlarged_rect(self):
        # aktuelles (gerade gerotetes!) Bildrechteck:
        rect = self.rot_image.get_rect(center=(self.x, self.y))
        # um die Ballgröße erweitern → Verdopplung
        return rect.inflate(rect.width , rect.height )


COLOR_MAP = {
    "green_slime": (load_asset.GREEN_SLIME, (green , black ) , "green_slime"),
    "evil_slime": (load_asset.EVIL_SLIME, (red , black ) , "evil_slime"),
    "cool_slime": (load_asset.COOL_SLIME, (green , dark_blue ) , "cool_slime"),
    "blue_slime": (load_asset.BLUE_SLIME, (blue , black ) , "blue_slime" )
}

class Enemy:
    def __init__(self, pos , slime_color ):
        self.slime_img , self.color_palette  , self.type = COLOR_MAP[slime_color]

        self.slime_img_orig = self.slime_img
        self.original_width, self.original_height = self.slime_img_orig.get_size()

        self.rect = self.slime_img.get_rect(center=(8, 8))
        self.mask = pygame.mask.from_surface(self.slime_img)
        self.x = pos[0]
        self.y = pos[1]
        self.runner = False
        self.hor_runner = False
        self.vert_runner = False
        self.speed = 0.6


        if random.randint(1 , 2 ) == 1:
            self.runner = True

        if self.runner:
            if random.randint(1 , 2 ) == 1 :
                self.hor_runner = True
            else:
                self.vert_runner = True

    def animate_slime(self , time ):
        if self.hor_runner:
            stretch_width = int(self.original_width * (1 + 0.5 * math.sin(time)))
            stretch_height = int(self.original_height * (1 - 0.5 * math.sin(time)))
        if self.vert_runner:
            stretch_width = int(self.original_width * (1 + 0.08 * math.sin(time)))
            stretch_height = int(self.original_height * (1 - 0.15 * math.sin(time)))
        else:
            stretch_width = int(self.original_width * (1 + 0.03 * math.sin(time)))
            stretch_height = int(self.original_height * (1 - 0.08 * math.sin(time)))


        self.slime_img = pygame.transform.smoothscale(self.slime_img_orig , (stretch_width , stretch_height))

        return stretch_width , stretch_height
    def draw(self ,stretch_width , stretch_height):
        x_pos = self.x - (self.rect.width // 2) - ((stretch_width - self.original_width) // 2 )
        y_pos =  self.y - (self.rect.height // 2)- ((stretch_height - self.original_height) // 2 )

        screen.blit(self.slime_img, (x_pos ,y_pos))

    def collision(self , obj1):
       return collide( self , obj1)

    def update(self , time ):
        stretch_width , stretch_height = self.animate_slime(time)

        if self.runner:
            if self.hor_runner:
                if self.x  < 0:
                    self.speed *= -1
                if self.x > width:
                    self.speed *= -1

                self.x += self.speed

            if self.vert_runner:

                if self.y  < 0:
                    self.speed *= -1
                if self.y > height:
                    self.speed *= -1

                self.y += self.speed

        self.draw(stretch_width , stretch_height)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def spawn_enemy(enemy_list):
    for i in range(random.randrange(5 , 25)):

        enemy = Enemy((random.randrange(20  ,  width - 20 ) , random.randrange(20 , height - 20 )) , random.choice(list(COLOR_MAP.keys())))
        enemy_list.append(enemy)

    return enemy_list

def spawn_wave1(enemy_list):
    for i in range(3):
        enemy = Enemy(( i * 100 + 250 ,  i * 100 + 100 ) , "blue_slime" )
        enemy_list.append(enemy)

    return enemy_list

def handle_kill(player , splatter_list , enemy_list , enemy_in):
    direction = player.vel

    speed = min(pygame.math.Vector2.length(player.vel) , 10) # speed cap for particle at 10

    for _ in range(20):
        splatter_list.append(
            SplatterParticle((enemy_in.x, enemy_in.y), direction, speed, enemy_in.color_palette))

    shake_timer = 15
    pygame.mixer.Sound.play(random.choice(load_asset.SQUACH_LIST))

    try:
        enemy_list.remove(enemy_in)
    except:
        pass
    return enemy_list

def give_time_offset(current_time, end_time):
    offset = (current_time - end_time + 1) * 30
    return offset

def main(player_color):
    player = Player(player_color , ( width // 2, height// 2  ))
    mouse_down = False
    ult_downtime_over = True
    ult_timer = 299
    first_mouse_pos = (width // 2 , height // 2)
    enemy_list = []
    enemy_list = spawn_wave1(enemy_list)
    hits = 0
    splatter_list = []
    shake_timer_splatter = 0
    shake_offset = pygame.math.Vector2(0, 0)
    game_over_state = False

    font = pygame.font.Font("assets/fonst/CreativeChildren-Regular.otf", 20)
    time = 0

    highest_streak = 0
    countdown = 10
    countdown_font = pygame.font.Font("assets/fonst/quaver.ttf", 35)
    pygame.mixer.music.play(-1)

    pygame.mouse.set_visible(False)
    cursor_rect = load_asset.HAND1.get_rect()

    while True:
        #grey
        screen.fill(grey)

        countdown_lable = countdown_font.render(f'Time: {int(countdown)}', 1, white)
        screen.blit(countdown_lable, (width - (countdown_lable.get_width() + 5), 10))

        if shake_timer_splatter > 0:
            shake_timer_splatter -= 1
            shake_offset.x = random.randint(-5, 5)
            shake_offset.y = random.randint(-5, 5)
        else:
            shake_offset = pygame.math.Vector2(0, 0)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_TAB:
                    menu()


            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if player.get_enlarged_rect().collidepoint(event.pos):
                    first_mouse_pos = event.pos
                    mouse_down = True

            if event.type == pygame.MOUSEBUTTONUP and mouse_down:
                player.calc_speed(first_mouse_pos, pygame.mouse.get_pos())
                mouse_down = False
                hits += 1

        # draw


        player.update(mouse_down, first_mouse_pos)
        if pygame.math.Vector2.length(player.vel) < 2:
            player.streak = 0

        #enemy update
        for enemy_in in enemy_list:
            enemy_in.update(time)
            if enemy_in.collision(player):

                if pygame.math.Vector2.length(player.vel) >= 1:
                    player.streak += 1

                if highest_streak < player.streak:
                    highest_streak = player.streak

                if enemy_in.type == "evil_slime":

                    game_over_state = True
                    enemy_list = handle_kill(player , splatter_list , enemy_list , enemy_in)

                elif enemy_in.type == "cool_slime" :

                    player.apply_boost()
                    enemy_list = handle_kill(player, splatter_list, enemy_list, enemy_in)
                else:
                    enemy_list = handle_kill(player, splatter_list, enemy_list, enemy_in)


        for p in splatter_list[:]:
            p.update()
            p.draw(screen, shake_offset)
            if p.life <= 0:
                splatter_list.remove(p)


        if len(enemy_list) == 0 :
            countdown += 10
            enemy_list = spawn_enemy(enemy_list)



        drag_len = 250
        if drag_len < 128:
            # Von grün zu gelb
            r = int(2 * drag_len)
            g = 255
        else:
            # Von gelb zu rot
            r = 255
            g = int(255 - 2 * (drag_len - 128))

        b = 0
        color = (r, g, b)
        pygame.draw.line(screen, color, (width // 3 , 800 ), ( (width // 3 ) * 2 , 800), width=5)

        ult_pos = (0 , 0)


        cursor_rect.center = pygame.mouse.get_pos()
        if mouse_down :
            cursor_img = load_asset.HAND_DRAG1
        else:
            cursor_img = load_asset.HAND1

        screen.blit(cursor_img , cursor_rect)
        pygame.display.update()
        clock.tick(120)
        time += 0.07
        countdown -= 1 / 120
       # if countdown <= 0:
            #break
    menu()

def menu():
    screen.fill((25 , 26 , 36))
    pygame.mouse.set_visible(True)
    start_hover = False
    options_hover = False
    exit_hover = False
    left_arrow_hover = False
    right_arrow_hover = False

    player_color = "red_ball"
    player_color_list = ["red_ball", "green_ball", "orange_ball", "blue_ball"]
    index = 0

    correction = (200 , 0 )
    rahmen_pos = (width // 2 - 250 - correction[0] , height // 2 - 250)

    start_image = load_asset.START_V
    start_rect = start_image.get_bounding_rect()
    start_pos = (345 - correction[0] , 235)
    start_rect.topleft = start_pos

    options_image = load_asset.OPTIONS_V
    options_rect = options_image.get_bounding_rect()
    options_pos = (345  - correction[0] , 315)
    options_rect.topleft = options_pos

    exit_image = load_asset.EXIT_V
    exit_rect = exit_image.get_bounding_rect()
    exit_pos = (345  - correction[0], 395)
    exit_rect.topleft = exit_pos

    arrow_right_image = load_asset.ARROW_RIGHT

    arrow_right_image = load_asset.ARROW_RIGHT
    arrow_right_rect = arrow_right_image.get_bounding_rect()
    arrow_right_pos = ( (width // 10) * 9  , (height // 10 ) * 4  )
    arrow_right_rect.topleft = arrow_right_pos

    arrow_left_image = load_asset.ARROW_LEFT
    arrow_left_rect = arrow_right_image.get_bounding_rect()
    arrow_left_pos = ((width // 2) , (height // 10) * 4)
    arrow_left_rect.topleft = arrow_left_pos

    # _image = load_asset.
    #_rect = _image.get_bounding_rect()
    #_pos = ( , )
    #_rect.topleft = _pos
    title_font = pygame.font.Font("assets/fonst/quaver.ttf" , 70)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and start_hover:
                main(player_color_list[index])

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and exit_hover:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and left_arrow_hover or event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                index = (index - 1) % len(player_color_list)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and right_arrow_hover or event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                index = (index + 1) % len(player_color_list)

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        player_image, ball_collor = PLAYER_MAP[player_color_list[index]]
        player_image = pygame.transform.scale_by(player_image, 4)
        player_rect = player_image.get_bounding_rect()
        player_pos = ((width // 40) * 26, (height // 10) * 3)
        player_rect.topleft = player_pos

        title_lable = title_font.render("SLINGY BALLIN", 1,ball_collor )
        screen.blit(title_lable , (width // 2  - (title_lable.get_width() // 2 ), 50 ) )
        screen.blit(load_asset.SOE_RAHMEN, rahmen_pos)


        # Buttons SOE
        if start_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(load_asset.START_PRESSED, rahmen_pos)
            start_hover = True
        else:
            start_hover = False
            screen.blit(load_asset.START_V, rahmen_pos)

        if options_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(load_asset.OPTIONS_PRESSED, rahmen_pos)
            options_hover = True
        else:
            options_hover = False
            screen.blit(load_asset.OPTIONS_V, rahmen_pos)

        if exit_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(load_asset.EXIT_PRESSED, rahmen_pos)
            exit_hover = True
        else:
            exit_hover = False
            screen.blit(load_asset.EXIT_V, rahmen_pos)


        if arrow_right_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(load_asset.ARROW_RIGHT_PRESSED, arrow_right_pos)
            right_arrow_hover = True
        else:
            right_arrow_hover = False
            screen.blit(load_asset.ARROW_RIGHT, arrow_right_pos)

        if arrow_left_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(load_asset.ARROW_LEFT_PRESSED, arrow_left_pos)
            left_arrow_hover = True
        else:
            left_arrow_hover = False
            screen.blit(load_asset.ARROW_LEFT, arrow_left_pos)


        screen.blit(player_image , player_rect )

        pygame.display.flip()
        clock.tick(60)


menu()

