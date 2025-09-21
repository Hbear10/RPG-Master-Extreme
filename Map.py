import pygame

class tile():#tiles that displayed in the world are objects - contain info about their looks and the different interactions they create
    def __init__(self, img: str,type: str, extra_info=()):#add information
        self.img = img 
        self.type = type#path,wall,enemy,random,sign,etc.
        self.extra_info = extra_info # any additional info

#take list of map and load it and create the object
def map_load(maptext:str, tiles,window_scale=1):

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
                tiles[block_info[1]]=pygame.transform.scale(pygame.image.load("Assets/"+block_info[1  ]+".png").convert(),(64*window_scale,64*window_scale))
    file.close()
    return map, tiles