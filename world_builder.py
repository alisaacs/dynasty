import random
import math
import pygame
import pygame.gfxdraw

#random.seed(42424242)

class tile:
    def __init__(self,x,y,tile_id):
        self.x = x
        self.y = y
        self.tile_id = tile_id
    def set_height(self,height):
        self.height = height

class world_map:
    def __init__(self, map_size_x, map_size_y):
        self.map_size = (map_size_x,map_size_y)
        self.map_array = [tile(x,y,(x*map_size_y + y)) for x in range(map_size_x) for y in range(map_size_y)]     
        self.create_heightmap()

    def create_heightmap(self):
        layer_1 = noise("perlin",256,self.map_size)
        layer_2 = noise("perlin",128,self.map_size)
        layer_3 = noise("perlin",64,self.map_size)
        layer_4 = noise("perlin",32,self.map_size)
        layer_5 = noise("perlin",16,self.map_size)
        layer_6 = noise("perlin",8,self.map_size)
        for cell in self.map_array:
                x = cell.x
                y = cell.y
                val = layer_1.perlin(x,y) + 0.5*layer_2.perlin(x,y) + 0.25*layer_3.perlin(x,y) + 0.125*layer_4.perlin(x,y) + 0.0625*layer_5.perlin(x,y) + 0.03125*layer_6.perlin(x,y)
                val = val/(1+0.5+0.25+0.125+0.0625+0.03125)
                cell.set_height((val+1)*5000)
	


    def find_x_y(self,tile_id):
        x = math.floor(tile_id/self.map_size[0])
        y = tile_id - x*map_size[0]
        return [x,y]

    def calc_tile_id(self,x,y):
        return x*self.map_size[1] + y

    #Functions to move around
    
    def move_north(self,tile_id):
        coords = self.find_x_y(tile_id)
        if coords[1] == map_size[1] - 1:
            return tile_id
        else:
            return self.calc_tile_id(coords[0],coords[1]+1)

    def move_south(self,tile_id):
        coords = self.find_x_y(tile_id)
        if coords[1] == 0:
            return tile_id
        else:
            return self.calc_tile_id(coords[0],coords[1]-1)

    def move_west(self,tile_id):
        coords = self.find_x_y(tile_id)
        if coords[0] == 0:
            return tile_id
        else:
            return self.calc_tile_id(coords[0]-1,coords[1])

    def move_east(self,tile_id):
        coords = self.find_x_y(tile_id)
        if coords[0] == map_size[0] - 1:
            return tile_id
        else:
            return self.calc_tile_id(coords[0]+1,coords[1])

    def random_tile(self):
        x = random.randint(0,self.map_size[0])
        y = random.randint(0,self.map_size[1])
        return self.calc_tile_id(x,y)
        


    #Functions to create a world


#Noise - move to module?


class noise:
    def __init__(self,noise,scale,map_size):
        if noise == "perlin":
            self.perlin_noise(scale,map_size)
        else:
            print("Noise type not recognised")

    def lerp(self,a0, a1, w):
        return (1.0 - w)*a0 + w*a1

    def distanceVector(self,p1,p2):
        delx = p2[0] - p1[0]
        dely = p2[1] - p1[1]
        magnitude = math.sqrt(delx*delx + dely*dely)
        if magnitude != 0:
            delx = delx/magnitude
            dely = dely/magnitude
        return (delx,dely) 

    def dotProduct(self,v1,v2):
        return v1[0]*v2[0] + v1[1]*v2[1]

    def randomVector(self):
        x = 2*random.random() - 1
        y = math.sqrt(1-math.pow(x,2))
        return (x,y)
        
    def perlin_noise(self,scale, map_size):
        #Check frequency divides into map_size
        self.scale = scale
        perlin_grid_x = math.ceil(map_size[0]/scale)
        perlin_grid_y = math.ceil(map_size[1]/scale)

        
        self.perlin_grid = [[self.randomVector()
                            for y in range(perlin_grid_y+1)]
                            for x in range(perlin_grid_x+1)]
        
    def perlin(self,x,y):
        x = x
        y = y
        x0 = math.floor(x/self.scale)
        x1 = math.ceil(x/self.scale)
        y0 = math.floor(y/self.scale)
        y1 = math.ceil(y/self.scale)

        u = (x-x0*self.scale)/self.scale
        v = (y-y0*self.scale)/self.scale
        
        a0 = self.dotProduct(self.perlin_grid[x0][y0], self.distanceVector((x/self.scale,y/self.scale),(x0,y0)))
        a1 = self.dotProduct(self.perlin_grid[x0][y1], self.distanceVector((x/self.scale,y/self.scale),(x0,y1)))
        a2 = self.dotProduct(self.perlin_grid[x1][y0], self.distanceVector((x/self.scale,y/self.scale),(x1,y0)))
        a3 = self.dotProduct(self.perlin_grid[x1][y1], self.distanceVector((x/self.scale,y/self.scale),(x1,y1)))

        #print(u,v,a0,a1,a2,a3)
        average = self.lerp(self.lerp(a0,a2,u),self.lerp(a1,a3,u),v)
        return average

world = world_map(512,256)

screen = pygame.display.set_mode(world.map_size)
for x in range(world.map_size[0]):
    for y in range(world.map_size[1]):
        val = world.map_array[world.calc_tile_id(x,y)].height
        if val < 1500:
            colour = (3,3,159)
        elif val < 2500:
            colour = (7,36,154)
        elif val < 3500:
            colour = (10,66,149)
        elif val < 4500:
            colour = (14,92,144)
        elif val < 5500:
            colour = (16,114,139)
        elif val < 6500:
            colour = (25,119,63)
        elif val < 7500:
            colour = (27,114,44)
        elif val < 8500:
            colour = (29,109,29)
        else:
            colour = (31,104,14)
       # print(x,y,world.calc_tile_id(x,y),val,colour,sep=" ")

        pygame.gfxdraw.pixel(screen,x,y,colour)

done = False
clock = pygame.time.Clock()
pygame.display.flip()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    clock.tick(60)

pygame.quit()

    
    
