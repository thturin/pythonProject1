import pgzrun
from random import randint
import time
"""
Project No. Happy Garden
Game starts. Cow appears in garden. every few seconds another flower appears or an existing flower begins to wilt. 
Use the arrow keys ot move the cow to the wilted flowers and press the space bar to water them. If any flower remains 
wilted for more than 15 seconds, one of the flowers mutates into a fangflower and tries to zap the cor 


HACKS AND TWEAKS 

add a menace 
"""

#constants
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
#global vars
time_elapsed = 0
flower_list = []
fangflower_list = []
start_time = time.time()
wilted_list = []
fangflower_vx_list = []
fangflower_vy_list = []
#flags
game_over = False
garden_happy = True
finalized = False
#actors
cow = Actor('cow')
cow.pos = 100,HEIGHT-100

def draw():
    global time_elapsed, finalized
    if not game_over:
        screen.clear()
        screen.blit('garden',(0,0))
        cow.draw()
        for flower in flower_list:
            flower.draw()
        for fangflower in fangflower_list:
            fangflower.draw()
        #check to see how long the game has been running for
        time_elapsed = int(time.time()- start_time)
        screen.draw.text('Garden Happy for: {} seconds'.format(time_elapsed),color='black',topleft=(10,10))
    else:
        if not finalized:
            cow.draw()
            #screen.draw.text('Garden Happy for: {} seconds'.format(time_elapsed), topleft=(10,10), color='black')
            if (not garden_happy):
                screen.draw.text('GARDEN IS UNHAPPY-GAME OVER',topleft=(10,50),color='black')
                finalized = True
            else:
                screen.draw.text('FANGFLOWER ATTACK-GAME OVER!', color='black', topleft=(10,50))
                finalized = True
    return

def new_flower():
    flower_new = Actor('flower')
    flower_new.pos = randint(100, WIDTH - 100), randint(150, HEIGHT - 100)
    flower_list.append(flower_new)
    wilted_list.append('happy')
    return

def add_flowers():
    if not game_over:
        new_flower()
        clock.schedule(add_flowers,4)
    return

def check_wilt_time():
    global garden_happy, game_over
    if wilted_list:
        for flower in wilted_list:
            if not flower == 'happy':
                if time.time()-int(flower) > 10:
                    garden_happy = False
                    game_over = True
                    break
    return

def wilt_flower():
    #wilt a random flower every 3 seconds
    global wilted_list, flower_list
    if not game_over:
        if flower_list:
            random_num = randint(0,len(flower_list)-1)
            if flower_list[random_num].image == 'flower':
                flower_list[random_num].image = 'flower-wilt'
                wilted_list[random_num] = time.time()
        clock.schedule(wilt_flower,3) #call this function every 3 seconds
    return

def check_flower_collisions():
    global wilted_list
    for index, flower in enumerate(flower_list):
        if flower.colliderect(cow) and flower.image == 'flower-wilt':
            flower.image = 'flower'
            wilted_list[index] = 'happy'
            break
    return

def reset_cow():
    if not game_over:
        cow.image = 'cow'
    return


def check_fangflower_collision():
    global game_over
    for fangflower in fangflower_list:
        if fangflower.colliderect(cow):
            cow.image = 'zap'
            game_over = True
            break
    return

def velocity():
    random_dir = randint(0,1)
    random_velocity = randint(2,3)
    if random_dir == 0: #if direction is left <<<< x is negative so make velocity negative
        return -random_velocity
    else: #if direction is right >>>>>>> x is positive to velocity is positive
        return random_velocity

def mutate():
    if not game_over and flower_list:
        random_num = randint(0,len(flower_list)-1)
        fangflower_xpos = flower_list[random_num].x
        fangflower_ypos = flower_list[random_num].y
        del flower_list[random_num]
        fangflower = Actor('fangflower')
        fangflower.pos = fangflower_xpos,fangflower_ypos
        fangflower_vx = velocity()
        fangflower_vy = velocity()
        fangflower = fangflower_list.append(fangflower)
        fangflower_vx_list.append(fangflower_vx)
        fangflower_vy_list.append(fangflower_vy)
        clock.schedule(mutate,10)
    return

def update_fangflowers():
    if not game_over:
        for index, fangflower in enumerate(fangflower_list):
            fangflower_vx = fangflower_vx_list[index] #get the current fangflower x velocity
            fangflower_vy = fangflower_vy_list[index]
            fangflower.x += fangflower_vx #set the new x and y position of the current fangflower by adding velocity to it
            fangflower.y += fangflower_vy
            #constraints
            if fangflower.x > WIDTH or fangflower.x < 0:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.y <150 or fangflower.y>HEIGHT:
                fangflower_vy_list[index] = -fangflower_vy
    return


def update():
    global time_elapsed
    #keyboard controls
    fangflower_collision = check_fangflower_collision()
    print(fangflower_collision)
    check_wilt_time()
    if not game_over:
        if keyboard.space:
            cow.image='cow-water'
            clock.schedule(reset_cow,0.5)
            check_flower_collisions()
        if keyboard.left and cow.x>100:
            cow.x -= 5
        if keyboard.right and cow.x<WIDTH-100:
            cow.x +=5
        if keyboard.up and cow.y>150:
            cow.y -= 5
        if keyboard.down and cow.y<HEIGHT:
            cow.y +=5
        if time_elapsed > 10 and not fangflower_list:
            mutate()
        update_fangflowers()




add_flowers()
wilt_flower()

pgzrun.go()