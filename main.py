import pygame
import random
import Spritesheet

print("hello world")


class being(): #for battles e.g. player or enemy and contains their stats
    def __init__(self,name: str,max_health: int,strength: int,defence: int,lvl=int,exp=None):#set up object
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.strength = strength
        self.defence = defence
        self.alive = True
        self.defended = 1 # 1 is not defended, 2 is defended, for when use defend button
        self.choice = "attack"
        self.lvl = lvl
        self.exp = exp

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


class text_pop_up(): # for the text pop ups e.g. appear as attack indicators
    def __init__(self,text:str,duration:int,coords: tuple, type="dmg-indicator"): # add information
        self.text = text
        self.duration = duration
        self.coords = coords
        self.type = type


class tile():#tiles that displayed in the world are objects - contain info about their looks and the different interactions they create
    def __init__(self, img: str,type: str, extra_info=()):#add information
        self.img = img 
        self.type = type#path,wall,enemy,random,sign,etc.
        self.extra_info = extra_info # any additional info


class world_being(): # player in world
    def __init__(self, x:int,y:int):
        self.x = x
        self.y = y
        self.moving = False
        self.target_x = x
        self.target_y = y
        

#finitude
#/ˈfɪnɪtjuːd,ˈfʌɪnɪtjuːd/
#noun formal
#the state of having limits or bounds.  

class item():
    def __init__(self,name,type,finitude,extra_info=[]):
        self.name = name
        self.type = type
        self.finitude = finitude
        self.extra_info = extra_info

# grass_tile = tile("Grass.png","path")
# path_tile = tile("Grass.png","path")
# brick_tile = tile("Brick.png", "wall")

#e.g. p-Grass
#p(ath),w(all),l(eave),h(arm),e(ncounter/enemy)

map = []

#take list of map and load it and create the object
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
            elif x[0] == "e":
                block = tile(block_info[1],"enemy")
            elif x[0] == "r":
                block = tile(block_info[1],"random")
            elif x[0] == "h":
                block = tile(block_info[1],"heal")
            map[-1].append(block)
            if block_info[1] not in tiles:
                tiles[block_info[1]]=pygame.transform.scale(pygame.image.load("Assets/"+block_info[1  ]+".png").convert(),(64*widnow_scale,64*widnow_scale))
    file.close()
    return map




def item_load(file):
    items = {}
    file = open(file)
    file_w_bad_formatting = file.read().split("\n")
    for line in file_w_bad_formatting:
        item_data = line.split(",")
        if len(item_data)==4:
            extra = item_data[3].split("~")
        else:
            extra = []
        items[item_data[0]] = item(item_data[0],item_data[1],item_data[2],extra_info=extra)
    file.close()
    return items


itemtypes = item_load("itemtypes.txt")
print(itemtypes)


def load_enemy(set):#random enemy
    if set == "start":
        types = ["Slime","Mushroom"]
        lvl = random.randint(2,4)
        return being(random.choice(types),random.randint(lvl*3,lvl*4),random.randint(lvl+1,lvl+4),random.randint(lvl+1,lvl+4),lvl)


world_player = world_being(64,64) # create player in world
player_speed = 4 #how fast moves
player_direction = 90#direction facing


text_list = [] #list of pop ups


player = being("Player",20,5,5,5,80) #health,strength,defence,lvl,exp

enemy = load_enemy("start")
#create battle objects
#enemy.health -= 5

game_state = "transition" # phase of game so the program knows what to draw and what logic to do and what inputs to take

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

def font(n:int): #returns a font of n size
    return pygame.font.SysFont('Comic Sans MS', n*widnow_scale)


big_font = font(50)
little_font = font(25)

clock = pygame.time.Clock()
timer = 64

text_box_info = {"title":"","desc":[""],"img":"Random.png"}
#creates animation for the player's attack slash
slash_sheet = Spritesheet.SpriteSheet("Assets\Slash.png")
slash = [slash_sheet.image_at((0,0,16,16),colorkey=(0,0,0)),slash_sheet.image_at((16,0,16,16),colorkey=(0,0,0)),slash_sheet.image_at((32,0,16,16),colorkey=(0,0,0)),slash_sheet.image_at((48,0,16,16),colorkey=(0,0,0)),\
        slash_sheet.image_at((64,0,16,16),colorkey=(0,0,0)),slash_sheet.image_at((80,0,16,16),colorkey=(0,0,0)),slash_sheet.image_at((96,0,16,16),colorkey=(0,0,0)),slash_sheet.image_at((112,0,16,16),colorkey=(0,0,0))]

projectile_sheet = Spritesheet.SpriteSheet("Assets\Projectile.png")
projectile = [projectile_sheet.image_at((0,0,16,16),colorkey=(0,0,0)),projectile_sheet.image_at((16,0,16,16),colorkey=(0,0,0)),projectile_sheet.image_at((32,0,16,16),colorkey=(0,0,0)),projectile_sheet.image_at((48,0,16,16),colorkey=(0,0,0)),\
        projectile_sheet.image_at((64,0,16,16),colorkey=(0,0,0)),projectile_sheet.image_at((80,0,16,16),colorkey=(0,0,0)),projectile_sheet.image_at((96,0,16,16),colorkey=(0,0,0)),projectile_sheet.image_at((112,0,16,16),colorkey=(0,0,0))]



battle_selection_mode = "normal"#normal or item
inventory = {"Stick":5,"Rock":4,"Magic Sword":"-","Potion":3,"Broken Shield":99,"Back":"<"}#,"plase":4,"halp":4,"me":4,"sword":1}
inventory_address = 0
inventory_increment=0 #how much I move the item list down
money = 100



#tiles = {"Grass":pygame.image.load("Assets/Grass.png").convert(),"Brick":pygame.image.load("Assets/Brick.png").convert(),"Enemy":pygame.image.load("Assets/Enemy.png").convert(),}
tiles = {}#dictionary of loaded images
map = map_load("start")

#for after transition
post_transition_stage = "world"
#for moving between maps
next_map = "start"

def battle_scene():#draw battle
    screen.fill((0,0,0))

    #enemy name
    enemy_name_and_level = big_font.render("Lvl "+str(enemy.lvl)+"   "+enemy.name, False, (255, 255, 255))
    screen.blit(enemy_name_and_level, (100,0))

    #enemy health bar
    enemy_health_bar_back = pygame.Rect(80*widnow_scale,80*widnow_scale,480*widnow_scale,32*widnow_scale)
    pygame.draw.rect(screen,(64,64,64),enemy_health_bar_back)
    enemy_health_bar_front = pygame.Rect(80*widnow_scale,80*widnow_scale,480*(enemy.health/enemy.max_health)*widnow_scale,32*widnow_scale)
    pygame.draw.rect(screen,(255,0,0),enemy_health_bar_front)

    

    #enemy health info
    enemy_health = little_font.render(str(enemy.health)+" / "+str(enemy.max_health), False, (255, 255, 255))
    screen.blit(enemy_health, (280,80))

    #seperator
    seperator = pygame.Rect(0,400,640,4)
    pygame.draw.rect(screen,(120,120,120),seperator)


    #if on normal selection screen/menu
    if battle_selection_mode == "normal":
        #player level
        player_level = little_font.render("Lvl "+str(player.lvl), False, (255, 255, 255))
        screen.blit(player_level, (5,420))

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
        item_select = big_font.render("item",False, (255,255,255))
        screen.blit(item_select, (360,460))
        stats_select = big_font.render("stats",False, (255,255,255))
        screen.blit(stats_select, (100,540))
        run_select = big_font.render("run",False, (255,255,255))
        screen.blit(run_select, (360,540))

        #selector indicators
        if player_turn:
            arrow_colour = (255,255,0)
        else:
            arrow_colour = (125,125,0)

            #print(timer)

        #selector - yellow arrows
        x_incriment = (battle_selector+1)%2*260
        y_incriment = (battle_selector-1)//2*80
        pygame.draw.polygon(screen, arrow_colour, ((60+x_incriment,480+y_incriment),(60+x_incriment,520+y_incriment),(80+x_incriment,500+y_incriment)))
        pygame.draw.polygon(screen, arrow_colour, ((300+x_incriment,480+y_incriment),(300+x_incriment,520+y_incriment),(280+x_incriment,500+y_incriment)))
    elif battle_selection_mode == "item":#item selector
        item_title = font(40).render("Items", False, (255, 255, 255))
        screen.blit(item_title, (20,400))

        #backboard for items
        item_list_back = pygame.Rect(200,414,380,215)
        pygame.draw.rect(screen,(64,64,64),item_list_back)

        if player_turn:
            arrow_colour = (255,255,0)
        else:
            arrow_colour = (125,125,0)

            #print(timer)

        #selector - yellow arrow
        y_incriment = (inventory_address-inventory_increment)*40
        pygame.draw.polygon(screen, arrow_colour, ((170,420+y_incriment),(170,460+y_incriment),(190,440+y_incriment)))

        #items
        names = list(inventory.keys())[0+inventory_increment:5+inventory_increment]
        #print(inventory_increment)
        for i in names:
            item_text = font(38).render(i, False, (255, 255, 255))
            #print(list(inventory.keys()))
            screen.blit(item_text, (200,410+(names.index(i)*40)))
            item_amount = font(40).render(str(inventory[i]), False, (255, 255, 255))
            screen.blit(item_amount, (520,410+(names.index(i)*40)))





    #draw enemy and their attack animation
    if player_turn == True or timer >= 30 or enemy.choice == "defend":#not moving
        #enemy sprite
        enemy_sprite = pygame.image.load("Assets/"+enemy.name+".png").convert()
        enemy_rect = enemy_sprite.get_rect()
        enemy_rect.center = (320,240)
        screen.blit(enemy_sprite,enemy_rect)
    else:#jumping up
        if timer > 15:
            #enemy sprite
            enemy_sprite = pygame.image.load("Assets/"+enemy.name+".png").convert()
            enemy_rect = enemy_sprite.get_rect()
         #   print(timer)
            enemy_rect.center = (320,240-(15-(timer-15))*2)
            screen.blit(enemy_sprite,enemy_rect)
        else:#falling down
            #enemy sprite
            enemy_sprite = pygame.image.load("Assets/"+enemy.name+".png").convert()
            enemy_rect = enemy_sprite.get_rect()
            enemy_rect.center = (320,240-timer*2)
            screen.blit(enemy_sprite,enemy_rect)
        
    if timer >= 36 and player.choice == "attack":#player attack slash
        screen.blit(pygame.transform.scale(slash[(60-timer)//4],(128,128)),(260,260))
    if timer >= 36 and player.choice == "projectile":#player attack slash
        screen.blit(pygame.transform.scale(projectile[(60-timer)//4],(128,128)),(260,260))



def enemy_turn(): #enemy action logic
    choice = random.randint(1,4)
    if choice <= 3:
        #enemy attacks
        
        enemy.choice = "attack"
       # print(timer)
        enemy.defended = 1
    elif choice == 4:
        enemy.choice = "defend"
        enemy.defended = 2
        text_list.append(text_pop_up("Defending",60,(200*widnow_scale,110*widnow_scale),"defending"))



def game_over(): # you died - need to make you get out of it
    screen.fill((0,0,0))

    #game over text
    text = little_font.render("Game Over WOMP WOMP stinky", False, (255, 255, 255))
    screen.blit(text, (120*widnow_scale,240*widnow_scale))



def game_won():#won battle
    screen.fill((0,0,0))

    #game won text
    text_you_beat = font(42).render("You beat ", False, (255, 255, 255))
    screen.blit(text_you_beat, (240,120))
    text_enemy_name = font(42).render(enemy.name, False, (255, 255, 255))
    screen.blit(text_enemy_name, (320-(len(enemy.name)//2*25),180))
    text_WELL_DONE = font(42).render(" WELL DONE", False, (255, 255, 255))
    screen.blit(text_WELL_DONE, (180,240))

    if timer > 30:
        exp_up_text = little_font.render("You gained "+str(enemy.lvl*5)+" exp", False, (255, 255, 255))
        screen.blit(exp_up_text, (220,340))
        if player.exp-enemy.lvl*5 <= 2.5*((player.lvl)**2) + 2.5*(player.lvl):#if levelled up
            #print(player.exp-enemy.lvl*5)
            level_up_text = little_font.render("You Leveled up, you are now Level "+str(player.lvl), False, (255, 255, 255))
            screen.blit(level_up_text, (120,380))
    if timer > 60:#appear after a second
        text = little_font.render("Press any key to go to world", False, (255, 255, 255))
        screen.blit(text, (160,480))


def level_up():
    player.lvl += 1
    player.max_health = player.lvl*4
    player.health += 4
    player.strength = player.lvl
    player.defence = player.lvl


def transition(): # black screen slowly passes over
    progress = (64 - timer)*10
    curtain = pygame.Rect(0,0,progress,640)
    pygame.draw.rect(screen,(0,0,0),curtain)



def start_transition(next_stage): #start transition
    global post_transition_stage, text_list,timer,game_state

    post_transition_stage = next_stage
    text_list = []
    timer = 64

    game_state = "transition"



def text_box(next_stage:str,title:str,desc:list,img="Random.png"):#start text box phase
    global post_transition_stage,text_box_info,game_state

    post_transition_stage = next_stage
    game_state = "text_box"
    text_box_info = {"title":title,"desc":desc,"img":img}



def draw_text_box(): #draw text box
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



def draw_world():#draw map
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

    #player
    player_png = ["Player_Down.png","Player_Right.png","Player_Up.png","Player_Left.png"][player_direction//90]
    player_img = pygame.transform.scale(pygame.image.load("Assets/"+player_png).convert(),(64,64))#getimage and convert to 64x64 and 
    player_img.set_colorkey((255,0,0))#remove all red as i used that as that as beckground when making the pixel art
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


                #player inputs
                if event.type == pygame.KEYDOWN:
                    #print(111)
                    if battle_selection_mode == "normal":
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

                            #player choice logic
                            if battle_selector == 1:#attack
                                player.defended = 1
                                enemy.hurt(player.strength)
                                x=text_pop_up(str(dmg),60,(240,240))
                                text_list.append(x)
                                #print(text_list)
                                #battle_scene()
                                player_turn = False
                                timer = 60
                                player.choice = "attack"
                            elif battle_selector == 2:#item, was defend
                                #player.defended = 2
                                #player_turn = False
                                #timer = 60
                                #player.choice = "defend"
                                battle_selection_mode = "item"
                            elif battle_selector == 3:#stats
                                text_box("battle","Stats",["hi","bye"],"Slime.png")
                            elif battle_selector == 4:#run
                                start_transition("world")
                                player.choice = "run"
                                battle_selection_mode = "normal"
                    elif battle_selection_mode == "item":
                        if event.key == pygame.K_UP:
                            if inventory_address == 0:
                                inventory_address = len(inventory)-1
                                if len(inventory) > 5:
                                    inventory_increment = len(inventory)-5
                                else:
                                    inventory_increment = 0
                            else:
                                inventory_address -= 1

                                if len(inventory) > 5:
                                    if inventory_address>=2 and len(inventory)-3>inventory_address:
                                        inventory_increment-=1 
                                
                        if event.key == pygame.K_DOWN:
                            if inventory_address == len(inventory)-1:
                                inventory_address = 0
                                inventory_increment = 0
                            else:
                                inventory_address += 1

                                if len(inventory) > 5:
                                    if inventory_address>2 and len(inventory)-3>=inventory_address:
                                        inventory_increment+=1 

                        if event.key == pygame.K_SPACE:
                            item_selected = itemtypes[list(inventory.keys())[inventory_address]]
                            #print(item_selected)
                            #print(item_selected.type)
                            if item_selected.type == "back":
                                battle_selection_mode = "normal"
                            elif item_selected.type == "throwable":
                                player.defended = 1#not defending

                                enemy.hurt(int(item_selected.extra_info[0])) # do damage
                                x=text_pop_up(str(dmg),60,(240,240))#text pop up
                                text_list.append(x)

                                player_turn = False
                                battle_selection_mode = "normal"

                                timer = 60
                                player.choice = "projectile"

                            elif item_selected.type == "health":
                                player.defended = 1
                                player_turn = False
                                battle_selection_mode = "normal"
                                timer = 60
                                player.choice = "heal"

                                heal_amount = int(item_selected.extra_info[0])
                                if heal_amount+player.health>player.max_health:
                                    player.health=player.max_health
                                else:
                                    player.health+=heal_amount

                            elif item_selected.type == "defence":
                                player_turn = False
                                battle_selection_mode = "normal"
                                timer = 60
                                player.choice = "defend"

                                player.defended = int(item_selected.extra_info[0])

                            if item_selected.finitude == "finite":
                                inventory[list(inventory.keys())[inventory_address]]-=1
                                if inventory[list(inventory.keys())[inventory_address]] == 0:
                                    inventory.pop(list(inventory.keys())[inventory_address])

                        #if len(inventory) > 5:


                        


        else: # enemy turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False    

            if timer > 0:
                timer -= 1
                #print(timer)
            else:
                player_turn = True
                battle_selection_mode = "normal"
                if enemy.choice == "attack":
                    player.hurt(enemy.strength)
                    text_list.append(text_pop_up(str(dmg),60,(560*widnow_scale,440*widnow_scale),"dmg-indicator"))
                    if player.health == 0:
                        start_transition("game_over")


            if timer == 30:
                if enemy.health > 0:
                    enemy_turn()
                        

                else:#enemy health 0
                    start_transition("game_won")
                    player_turn = True
                    battle_selection_mode = "normal"
                    player.exp += enemy.lvl*5
                    while player.exp > 2.5*((player.lvl+1)**2) + 2.5*(player.lvl+1):
                        level_up()
                    
                    

        battle_scene()
    
    elif game_state == "game_over":#game over
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        game_over()

    elif game_state == "game_won":  #won game
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:#go back to world
                    start_transition("world")
        
        game_won()#draw game won
        timer += 1#timer

        
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
                if map[world_player.y//64][world_player.x//64].type == "enemy":#make sure not end up back on enemy tile
                    world_player.x -= 64
                    world_player.target_x -= 64
            elif post_transition_stage == "battle":
                battle_selector = 1
        else:
            timer -= 1
   
   
    elif game_state == "text_box":    #text box - stats,signs draw it
        #print(1)  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                game_state = post_transition_stage
                timer = 0
        
        draw_text_box()

        
  
    elif game_state == "world":     # draw map and moving logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # add enter key as well
                            pass
                            #add interact

        if world_player.moving == False: #moving logic
            #if pygame.key.get_pressed[pygame.KEYUP]:
            if  pygame.key.get_pressed()[pygame.K_UP]:
                player_direction = 180
                if map[world_player.y//64-1][world_player.x//64].type != "wall" and world_player.y != 0:
                    world_player.target_y = world_player.y-64
                    world_player.moving = True
                    
                #else:
                    #print("Can't go")
                    
            if  pygame.key.get_pressed()[pygame.K_DOWN]:
                player_direction = 0
                if map[world_player.y//64+1][world_player.x//64].type != "wall" and world_player.y != 576:#if not wall
                    world_player.target_y = world_player.y+64
                    world_player.moving = True
                #else:
                    
                    #print("Can't go")
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                player_direction = 270
                if map[world_player.y//64][world_player.x//64-1].type != "wall" and world_player.x != 0:#if not wall
                    world_player.target_x = world_player.x-64
                    world_player.moving = True
                #else:
                    #print("Can't go")
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                player_direction = 90
                if map[world_player.y//64][world_player.x//64+1].type != "wall" and world_player.x != 576:#if not wall
                    world_player.target_x = world_player.x+64
                    world_player.moving = True
               # else:
                    #print("Can't go")
            elif pygame.key.get_pressed()[pygame.K_SPACE]:#interactive tiles
                if timer > 30:
                    if player_direction == 90:#right
                        if map[world_player.y//64][world_player.x//64+1].extra_info != () and world_player.x != 576:
                            info = map[world_player.y//64][world_player.x//64+1].extra_info
                            text_box(info[0],info[1],info[2],info[3])
                    elif player_direction == 180:#down
                        if map[world_player.y//64-1][world_player.x//64].extra_info != () and world_player.x != 576:
                            info = map[world_player.y//64-1][world_player.x//64].extra_info
                            text_box(info[0],info[1],info[2],info[3])
                    elif player_direction == 270:#left
                        if map[world_player.y//64][world_player.x//64-1].extra_info != () and world_player.x != 576:
                            info = map[world_player.y//64][world_player.x//64-1].extra_info
                            text_box(info[0],info[1],info[2],info[3])
                    elif player_direction == 0:#up
                        if map[world_player.y//64+1][world_player.x//64].extra_info != () and world_player.x != 576:
                            info = map[world_player.y//64+1][world_player.x//64].extra_info
                            text_box(info[0],info[1],info[2],info[3])
                    
                    
        if world_player.x == world_player.target_x and world_player.y == world_player.target_y: #logic for when standing on new tile
            if world_player.moving == True:
                #print(map[world_player.y//64][world_player.x//64].type)
                if map[world_player.y//64][world_player.x//64].type == "random":
                    #print(1111111)
                    if random.randint(1,5)==5:
                        enemy = load_enemy("start")
                        start_transition("battle")
                elif map[world_player.y//64][world_player.x//64].type == "leave":
                    info = map[world_player.y//64][world_player.x//64].extra_info
                    world_player.x, world_player.target_x = int(info[1])*64,int(info[1])*64
                    world_player.y, world_player.target_y = int(info[2])*64,int(info[2])*64
                    next_map = info[0]
                    start_transition("world")
                elif map[world_player.y//64][world_player.x//64].type == "enemy":
                    enemy = load_enemy("start")
                    start_transition("battle")
                elif map[world_player.y//64][world_player.x//64].type == "heal":
                    #print(1)
                    player.health = player.max_health
                    
                    x=text_pop_up("Healing",60,(world_player.x,world_player.y+64))#text pop up
                    text_list.append(x)
                world_player.moving = False

            
            
            else:
                draw_world()
                
        else:#move player
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
    for i in text_list: #draw text indicators above everything else
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

    for i in text_list: #remove outdated text on screen
        if i.duration <= 0:
            text_list.pop(text_list.index(i))

    pygame.display.flip()
    clock.tick(60)
    #print(clock.get_fps())


pygame.quit()