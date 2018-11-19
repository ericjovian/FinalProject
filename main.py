import pygame
import random
from arrow import Bullet
from enemy import Block
from boss import Boss
pygame.init()

# Colours
black = (0, 0, 0)
white = (225, 225, 225)
green = (0, 220, 0)
bright_green = (0, 225, 0)
red = (220, 0, 0)
bright_red = (225, 0, 0)
tgi = 700
lbr = 1200

# Variable
x = 0
y = 0
vel = 0
score = 0
win = pygame.display.set_mode((lbr, tgi))
player = pygame.image.load("marksman.png")
player = pygame.transform.scale(player, (80, 130))
players = pygame.image.load("marksmanflip.png")
players = pygame.transform.scale(players, (80, 130))
flip = players
bg = pygame.image.load("bgd.png")
bg = pygame.transform.scale(bg, (lbr, tgi))
pygame.display.set_caption("Zombie Invasion")
clock = pygame.time.Clock()
pygame.mixer.music.load("songsong.wav")

# --- Sprite lists

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
block_list = pygame.sprite.Group()

# List of Boss
boss_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

def quitgame():
    pygame.quit()
    quit()
                    
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ac,ic,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    smallText = pygame.font.Font("freesansbold.ttf", 20)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(win, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(win, ic, (x,y,w,h))

    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    win.blit(textSurf, textRect)

def game_intro():
    mainbg = pygame.image.load("mainbg.jpg")
    mainbg = pygame.transform.scale(mainbg, (lbr, tgi))

    pygame.mixer.music.play(1)
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.blit(mainbg, [0, 0])
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Zombie Invasion", largeText)
        TextRect.center = ((lbr / 2), (tgi / 2))
        win.blit(TextSurf, TextRect)

        button("Play", 450, 450, 300, 50, green, bright_green, game_loop)
        button("Quit", 450, 550, 300, 50, red, bright_red, quitgame)

        pygame.display.update()

def big():
    for i in range(1):
        # This represents a block
        boss = Boss()

        # Set a random location for the block
        boss.rect.x = 1000
        boss.rect.y = 350

        # Add the block to the list of objects
        boss_list.add(boss)
        all_sprites_list.add(boss)

def create():
    for i in range(10):
        # This represents a block
        block = Block()

        # Set a random location for the block
        block.rect.x = random.randrange(lbr)
        block.rect.y = random.randrange(tgi - 50)

        # Add the block to the list of objects
        block_list.add(block)
        all_sprites_list.add(block)

def game_loop():
    pygame.mixer_music.stop()
    pygame.mixer.music.load("song.wav")
    pygame.mixer.music.play(1)
    x = 0
    y = 0
    score = 0
    vel = 9
    counter = 0
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]
    run = True
    while run:
        if len(block_list) == 0 and counter < 5:
            create()
            counter +=1

            if counter == 5:
                big()

        win.blit(bg, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.mixer_music.stop()
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
                # Get the mouse position
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]
                # Create the bullet based on where we are, and where we want to go.
                bullet = Bullet(x + 55, y + 55, mouse_x, mouse_y)
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and x > vel:
            x -= 5
        if keys[pygame.K_d] and x < 1200-vel-100:
            x += 5
        if keys[pygame.K_w] and y > vel:
            y -= 5
        if keys[pygame.K_s] and y < 700-vel-170:
            y += 5
        if keys[pygame.K_r]:
            game_intro()

        # --- Game logic

        # Call the update() method on all the sprites
        all_sprites_list.update()

        # Calculate mechanics for each bullet
        for bullet in bullet_list:

            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

            # See if it hit the boss
            boss_hit_list = pygame.sprite.spritecollide(bullet, boss_list, True)

            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                print(score)

            for boss in boss_hit_list:
                boss_list.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 10
                print(score)
            if score == 60:
                die = pygame.image.load("gameover.jpg")
                die = pygame.transform.scale(die, (1200, 700))
                win.blit(die, [0, 0])

            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                boss_list.remove(bullet)
                all_sprites_list.remove(bullet)

        if mouse_x < x:
            player = flip
        else:
            player = pygame.image.load("marksman.png")
            player = pygame.transform.scale(player, (80, 130))
        win.blit(player, (x, y))
        for i in block_list:
            i.follow(x, y)
            i.stop(x, y)
        for j in boss_list:
            j.follow(x, y)
            j.stop(x, y)
        all_sprites_list.draw(win)
        clock.tick(60)
        pygame.display.flip()


game_intro()
