import pygame
import random

print("hello world")


class being():
    def __init__(self,name: str,max_health: int,strength: int,defence: int):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.strength = strength
        self.defence = defence
        self.alive = True
        self.defended = 1 # 1 is not defended, 2 is defended, for when use defend button

    def hurt(self, enemy_strength): #attack this being
        global dmg

        damage_dealt = int(enemy_strength//(((self.defence*self.defended)+2)/2) + random.randint(0,1))+1
        dmg = damage_dealt

        self.health -= damage_dealt
        if self.health <= 0:
            self.health = 0
            self.alive = False



    def attack(self):
        return self.strength


class text_pop_up():
    def __init__(self,text:str,duration:int,coords: tuple, type="dmg-indicator"):
        self.text = text
        self.duration = duration
        self.coords = coords
        self.type = type


class tile():
    def __init__(self, img: str,type: str, extra_info=()):
        self.img = img #will start as colour then switch to img
        self.type = type
        self.extra_info = extra_info


class world_being():
    def __init__(self, x:int,y:int):
        self.x = x
        self.y = y
        self.moving = False
        self.target_x = x
        self.target_y = y

class enemy_being(being):
    def __init__(self, name, max_health, strength, defence):
        super().__init__(name, max_health, strength, defence)
        self.health = max_health
        self.alive = True
        self.defended = 1 # 1 is not defended, 2 is defended, for when use defend button
        self.choice = "attack"



# grass_tile = tile("Grass.png","path")
# path_tile = tile("Grass.png","path")
# brick_tile = tile("Brick.png", "wall")

#e.g. p-Grass
#p(ath),w(all),l(eave),h(arm),e(ncounter/enemy)

map = []

def map_load(maptext:str):
    global tiles

    map = []
    file = open("Maps/"+maptext+".txt", "r")
    map_bad = file.read().split('\n')
    for i in map_bad:
        i = i.split(",")
        map.append([])
        for x in i:
            block_info = x.split("-")
            if block_info[0] == "p":
                block = tile(block_info[1],"path")
            elif x[0] == "w":
                if len(block_info)>=3:
                    block = tile(block_info[1],"wall",list(block_info[2].split("~")))
                    block.extra_info[-2] = block.extra_info[-2].split(".")
                else:
                    block = tile(block_info[1],"wall")
            elif x[0] == "l":
                block = tile(block_info[1],"leave",tuple(block_info[2].split("~")))
            elif x[0] == "h":
                block = tile(block_info[1],"harm")
            elif x[0] == "e":
                block = tile(block_info[1],"enemy")
            elif x[0] == "r":
                block = tile(block_info[1],"random")
            map[-1].append(block)
            if block_info[1] not in tiles:
                tiles[block_info[1]]=pygame.transform.scale(pygame.image.load("Assets/"+block_info[1  ]+".png").convert(),(64*widnow_scale,64*widnow_scale))
    file.close()
    return map


def load_enemy():
    types = ["Slime","Mushroom"]
    return enemy_being(random.choice(types),random.randint(9,11),random.randint(3,5),random.randint(3,4))




world_player = world_being(64,64)
player_speed = 4
player_direction = 90


text_list = []


player = being("Player",24,4,4)

enemy = load_enemy()
#enemy.health -= 5

game_state = "transition"

#battle variables
battle_selector = 1
player_turn = True
dmg = 0

widnow_scale = 1

pygame.init()
#set up screen
screen = pygame.display.set_mode((640*widnow_scale, 640*widnow_scale))
screen.fill((255,255,255))

pygame.font.init() 

def font(n:int):
    return pygame.font.SysFont('Comic Sans MS', n*widnow_scale)


big_font = font(50)
little_font = font(25)

clock = pygame.time.Clock()
timer = 64

text_box_info = {"title":"","desc":[""],"img":"Random.png"}



#tiles = {"Grass":pygame.image.load("Assets/Grass.png").convert(),"Brick":pygame.image.load("Assets/Brick.png").convert(),"Enemy":pygame.image.load("Assets/Enemy.png").convert(),}
tiles = {}
map = map_load("start")


post_transition_stage = "world"
next_map = "start"

def battle_scene():
    screen.fill((0,0,0))

    #enemy name
    enemy_name = big_font.render(enemy.name, False, (255, 255, 255))
    screen.blit(enemy_name, (100,0))

    #enemy health bar
    enemy_health_bar_back = pygame.Rect(80*widnow_scale,80*widnow_scale,480*widnow_scale,32*widnow_scale)
    pygame.draw.rect(screen,(64,64,64),enemy_health_bar_back)
    enemy_health_bar_front = pygame.Rect(80*widnow_scale,80*widnow_scale,480*(enemy.health/enemy.max_health)*widnow_scale,32*widnow_scale)
    pygame.draw.rect(screen,(255,0,0),enemy_health_bar_front)

    

    #enemy health info
    enemy_health = little_font.render(str(enemy.health)+" / "+str(enemy.max_health), False, (255, 255, 255))
    screen.blit(enemy_health, (280,80))

    seperator = pygame.Rect(0,400,640,4)
    pygame.draw.rect(screen,(120,120,120),seperator)

    #player Health
    player_health_bar_back = pygame.Rect(80,420,480,32)
    pygame.draw.rect(screen,(64,64,64),player_health_bar_back)
    player_health_bar_front = pygame.Rect(80,420,480*(player.health/player.max_health),32)
    pygame.draw.rect(screen,(255,0,0),player_health_bar_front)

    #player health info
    player_health = little_font.render(str(player.health)+" / "+str(player.max_health), False, (255, 255, 255))
    screen.blit(player_health, (280,420))

    #options
    attack_select = big_font.render("attack",False, (255,255,255))
    screen.blit(attack_select, (100,460))
    defend_select = big_font.render("defend",False, (255,255,255))
    screen.blit(defend_select, (360,460))
    stats_select = big_font.render("stats",False, (255,255,255))
    screen.blit(stats_select, (100,540))

    #run
    run_select = big_font.render("run",False, (255,255,255))
    screen.blit(run_select, (360,540))

    #selector indicators
    if player_turn:
        arrow_colour = (255,255,0)
    else:
        arrow_colour = (125,125,0)

        #print(timer)

    x_incriment = (battle_selector+1)%2*260
    y_incriment = (battle_selector-1)//2*80
    pygame.draw.polygon(screen, arrow_colour, ((60+x_incriment,480+y_incriment),(60+x_incriment,520+y_incriment),(80+x_incriment,500+y_incriment)))
    pygame.draw.polygon(screen, arrow_colour, ((300+x_incriment,480+y_incriment),(300+x_incriment,520+y_incriment),(280+x_incriment,500+y_incriment)))

    if player_turn == True or timer <= 30 or enemy.choice == "defend":
        #enemy sprite
        enemy_sprite = pygame.image.load("Assets/"+enemy.name+".png").convert()
        enemy_rect = enemy_sprite.get_rect()
        enemy_rect.center = (320,320)
        screen.blit(enemy_sprite,enemy_rect)
    else:
        #enemy sprite
        enemy_sprite = pygame.image.load("Assets/"+enemy.name+".png").convert()
        enemy_rect = enemy_sprite.get_rect()
        enemy_rect.center = (320,320+timer-30)
        screen.blit(enemy_sprite,enemy_rect)






def enemy_turn():
    choice = random.randint(1,4)
    if choice <= 3:
        #enemy attacks
        
        enemy.choice = "attack"
        print(timer)
        enemy.defended = 1
    elif choice == 4:
        enemy.choice = "defend"
        enemy.defended = 2
        text_list.append(text_pop_up("Defending",120,(220*widnow_scale,195*widnow_scale),"defending"))


def game_over():
    screen.fill((0,0,0))

    #game over text
    text = little_font.render("Game Over WOMP WOMP stinky", False, (255, 255, 255))
    screen.blit(text, (120*widnow_scale,240*widnow_scale))


def game_won():
    screen.fill((0,0,0))

    #game over text
    text_you_beat = font(42).render("You beat ", False, (255, 255, 255))
    screen.blit(text_you_beat, (240,120))
    text_enemy_name = font(42).render(enemy.name, False, (255, 255, 255))
    screen.blit(text_enemy_name, (320-(len(enemy.name)//2*25),180))
    text_WELL_DONE = font(42).render(" WELL DONE", False, (255, 255, 255))
    screen.blit(text_WELL_DONE, (180,240))

    if timer > 60:
        text = little_font.render("Press any key to go to world", False, (255, 255, 255))
        screen.blit(text, (160,360))


def transition(): # black screen slowly passes over
    progress = (64 - timer)*10
    curtain = pygame.Rect(0,0,progress,640)
    pygame.draw.rect(screen,(0,0,0),curtain)


def start_transition(next_stage):
    global post_transition_stage, text_list,timer,game_state

    post_transition_stage = next_stage
    text_list = []
    timer = 64

    game_state = "transition"


def text_box(next_stage:str,title:str,desc:list,img="Random.png"):
    global post_transition_stage,text_box_info,game_state

    post_transition_stage = next_stage
    game_state = "text_box"
    text_box_info = {"title":title,"desc":desc,"img":img}


def draw_text_box():
    big_box_outline = pygame.Rect(0,400*widnow_scale,640*widnow_scale,240*widnow_scale)
    pygame.draw.rect(screen,(255,255,255),big_box_outline)
    big_box = pygame.Rect(5*widnow_scale,405*widnow_scale,630*widnow_scale,230*widnow_scale)
    pygame.draw.rect(screen,(0,0,0),big_box)
    middle_line = pygame.Rect(150*widnow_scale,400*widnow_scale,5*widnow_scale,240*widnow_scale)
    pygame.draw.rect(screen,(255,255,255),middle_line)
    title_line = pygame.Rect(0*widnow_scale,440*widnow_scale,150*widnow_scale,5*widnow_scale)
    pygame.draw.rect(screen,(255,255,255),title_line)

    title = little_font.render(text_box_info["title"], False, (255, 255, 255))
    screen.blit(title, (10*widnow_scale,410*widnow_scale))

    img = pygame.image.load("Assets/"+text_box_info["img"]).convert()
    img_rect = img.get_rect()
    img_rect.center = (70,540)
    screen.blit(img,img_rect)

    for i in range(len(text_box_info["desc"])):
        desc = little_font.render(text_box_info["desc"][i], False, (255, 255, 255))
        screen.blit(desc, ((200)*widnow_scale,(410+i*30)*widnow_scale))


def draw_world():
    screen.fill((0,0,0))
    for y in range(0,10):#0-9
        for x in range(0,10):#0-9
            # square = pygame.Rect(64*x,64*y,64,64)
            # pygame.draw.rect(screen,(map[y][x].img),square)

            #square_img = pygame.image.load("Assets/"+map[y][x].img).convert()
            square_rect = tiles[map[y][x].img].get_rect()
            square_rect.center = (64*x*widnow_scale+32*widnow_scale,64*y*widnow_scale+32*widnow_scale)
            screen.blit(tiles[map[y][x].img],square_rect)

    # player = pygame.Rect(world_player.x,world_player.y,64,64)
    # pygame.draw.rect(screen,("YELLOW"),player)

    player_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Assets/Player_temp.png").convert(),(64,64)),player_direction)
    player_rect = player_img.get_rect()
    player_rect.center = ((world_player.x+32)*widnow_scale,(world_player.y+32)*widnow_scale)
    screen.blit(player_img,player_rect)


running = True
while running:
    # for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False

    if game_state == "battle":
        if player_turn:
            pressed_keys = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                #moving selector indicator
                if event.type == pygame.KEYDOWN:
                    #print(111)
                    if event.key == pygame.K_UP:
                        battle_selector = [0,3,4,1,2][battle_selector]
                    if event.key == pygame.K_DOWN:
                        battle_selector = [0,3,4,1,2][battle_selector]
                    if event.key == pygame.K_LEFT:
                        battle_selector = [0,2,1,4,3][battle_selector]
                    if event.key == pygame.K_RIGHT:
                        battle_selector = [0,2,1,4,3][battle_selector]
        
                    if event.key == pygame.K_SPACE: # add enter key as well
                        # player_turn = False
                        # timer = 120

                        if battle_selector == 1:
                            player.defended = 1
                            enemy.hurt(player.strength)
                            x=text_pop_up(str(dmg),60,(240,240))
                            text_list.append(x)
                            #print(text_list)
                            #battle_scene()
                            player_turn = False
                            timer = 120
                        elif battle_selector == 2:
                            player.defended = 2
                            player_turn = False
                            timer = 120
                        elif battle_selector == 3:
                            text_box("battle","Stats",["hi","bye"],"Slime.png")
                        elif battle_selector == 4:
                            start_transition("world")
                    


        else: # enemy turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False    

            if timer > 0:
                timer -= 1
                #print(timer)
            else:
                player_turn = True
                if enemy.choice == "attack":
                    player.hurt(enemy.strength)
                    text_list.append(text_pop_up(str(dmg),60,(560*widnow_scale,440*widnow_scale),"dmg-indicator"))


            if timer == 30:
                if enemy.health > 0:
                    enemy_turn()
                    if player.health == 0:
                        start_transition("game_over")
                        

                else:
                    start_transition("game_won")
                    
                    

        battle_scene()
    
    elif game_state == "game_over":
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        game_over()

    elif game_state == "game_won":  
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    start_transition("world")
        
        game_won()
        timer += 1

        
    elif game_state == "transition":    
        #print(1)  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        transition()

        if timer == 0:
            game_state = post_transition_stage
            if post_transition_stage == "game_won":
                timer = 0
            elif post_transition_stage == "world":
                map = map_load(next_map)
                if map[world_player.y//64][world_player.x//64].type == "enemy":
                    world_player.x -= 64
                    world_player.target_x -= 64
            elif post_transition_stage == "battle":
                battle_selector = 1
        else:
            timer -= 1
   
   
    elif game_state == "text_box":    
        #print(1)  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                game_state = post_transition_stage
                timer = 0
        
        draw_text_box()

        
  
    elif game_state == "world":     # 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # add enter key as well
                            pass
                            #add interact

        if world_player.moving == False:
            #if pygame.key.get_pressed[pygame.KEYUP]:
            if  pygame.key.get_pressed()[pygame.K_UP]:
                player_direction = 180
                if map[world_player.y//64-1][world_player.x//64].type != "wall" and world_player.y != 0:
                    world_player.target_y = world_player.y-64
                    world_player.moving = True
                    
                else:
                    print("Can't go")
            if  pygame.key.get_pressed()[pygame.K_DOWN]:
                player_direction = 0
                if map[world_player.y//64+1][world_player.x//64].type != "wall" and world_player.y != 576:
                    world_player.target_y = world_player.y+64
                    world_player.moving = True
                else:
                    print("Can't go")
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                player_direction = 270
                if map[world_player.y//64][world_player.x//64-1].type != "wall" and world_player.x != 0:
                    world_player.target_x = world_player.x-64
                    world_player.moving = True
                else:
                    print("Can't go")
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                player_direction = 90
                if map[world_player.y//64][world_player.x//64+1].type != "wall" and world_player.x != 576:
                    world_player.target_x = world_player.x+64
                    world_player.moving = True
                else:
                    print("Can't go")
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                if timer > 30:
                    if player_direction == 90:
                        if map[world_player.y//64][world_player.x//64+1].extra_info != () and world_player.x != 576:
                            info = map[world_player.y//64][world_player.x//64+1].extra_info
                            text_box(info[0],info[1],info[2],info[3])
                    elif player_direction == 180:
                        if map[world_player.y//64-1][world_player.x//64].extra_info != () and world_player.x != 576:
                            info = map[world_player.y//64-1][world_player.x//64].extra_info
                            text_box(info[0],info[1],info[2],info[3])
                    elif player_direction == 270:
                        if map[world_player.y//64][world_player.x//64-1].extra_info != () and world_player.x != 576:
                            info = map[world_player.y//64][world_player.x//64-1].extra_info
                            text_box(info[0],info[1],info[2],info[3])
                    elif player_direction == 0:
                        if map[world_player.y//64+1][world_player.x//64].extra_info != () and world_player.x != 576:
                            info = map[world_player.y//64+1][world_player.x//64].extra_info
                            text_box(info[0],info[1],info[2],info[3])
                    
                    
        if world_player.x == world_player.target_x and world_player.y == world_player.target_y:
            if world_player.moving == True:
                if map[world_player.y//64][world_player.x//64].type == "random":
                    #print(1111111)
                    if random.randint(1,5)==5:
                        enemy = load_enemy()
                        start_transition("battle")
                elif map[world_player.y//64][world_player.x//64].type == "leave":
                    info = map[world_player.y//64][world_player.x//64].extra_info
                    world_player.x, world_player.target_x = int(info[1])*64,int(info[1])*64
                    world_player.y, world_player.target_y = int(info[2])*64,int(info[2])*64
                    next_map = info[0]
                    start_transition("world")
                elif map[world_player.y//64][world_player.x//64].type == "enemy":
                    enemy = load_enemy()
                    start_transition("battle")
                world_player.moving = False

            
            
            else:
                draw_world()
                
        else:
            if world_player.x > world_player.target_x:#move left
                world_player.x -= player_speed
            elif world_player.x < world_player.target_x:#move right
                world_player.x += player_speed
            elif world_player.y > world_player.target_y:#move up
                world_player.y -= player_speed
            elif world_player.y < world_player.target_y:#move down
                world_player.y += player_speed


            draw_world()
        
        if timer != 60:
            timer += 1


    #well hello there



    #if len(text_list) > 0:
    for i in text_list:
        #print(text_list)
        #print(type(i))
        #print(i.coords)

        if i.type == "dmg-indicator":
            words = pygame.font.SysFont('Comic Sans MS', i.duration).render(i.text, False, (255, 255, 255))
        elif i.type == "defending":
            words = pygame.font.SysFont('Comic Sans MS', 50).render(i.text, False, (255, 255, 255))
        else:
            words = pygame.font.SysFont('Comic Sans MS', 60).render("Error", False, (255, 255, 255))

        screen.blit(words, i.coords)
        i.duration -= 1

    for i in text_list:
        if i.duration <= 0:
            text_list.pop(text_list.index(i))

    pygame.display.flip()
    clock.tick(60)
    #print(clock.get_fps())


pygame.quit()