import pygame
import random
import Queue
import math
pygame.init()
XMULTI = 20 
YMULTI = 20
MAX_DIST = 1000000000

def create_rand_colours(num):
    colours = [(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for i in range(num)]
    return colours

class Agrid:
    def __init__(self,dims,celldims):
        self.rows = dims[1] // celldims[1]
        self.columns = dims[0] // celldims[0]
        self.maze_start = (0,0)
        self.maze_end = (self.columns-1,self.rows-1)
        self.blocking = [ [False for i in range( self.columns )] for j in range( self.rows )]

        self.cellarray = [ [object for i in range( self.columns )] for j in range( self.rows )]
        fours = ((-1,0),(0,-1),(1,0),(0,1))

        for i in range(self.rows):
            for j in range(self.columns):
                ns = []
                for z in fours:
                    c_offset = z[0]
                    r_offset = z[1]

                    if( c_offset+j < 0 or c_offset+j > self.columns-1 ):
                        continue
                    if( r_offset+i < 0 or r_offset+i > self.rows-1 ):
                        continue 
                    ns.append((c_offset+j,r_offset+i))
                self.cellarray[i][j] = Acell((j,i),ns)

    def calculate_route(self,start,end):
        dist = [ [object for i in range(self.columns)] for j in range( self.rows )]
        prev = [ [object for i in range(self.columns)] for j in range( self.rows )]
        p_queue = Queue.PriorityQueue()
        dist[start[1]][start[0]] = 0
        prev[start[1]][start[0]] = -1
        for i in self.cellarray:
            for j in i:
                v_c = j.coor[0]
                v_r = j.coor[1]
                if not(v_c == start[0] and v_r == start[1]):
                    dist[v_r][v_c] =MAX_DIST
                    prev[v_r][v_c] = -1
                p_queue.put((v_c,v_r),dist[v_c][v_r] )
        while not p_queue.empty():
            u = p_queue.get()
            u_c,u_r = u
            u_cell = self.cellarray[u_r][u_c]

            for z in u_cell.neighs:
                z_c,z_r = z
                z_cell = self.cellarray[z_r][z_c]
                cell_blocked = self.blocking[z_r][z_c]
                if cell_blocked == True:
                    continue
                alt = dist[u_r][u_c] + 1
                if alt<dist[z_r][z_c]:
                    dist[z_r][z_c] = alt
                    prev[z_r][z_c] = u
                    p_queue.put(z,alt)

        return prev

    def get_route(self,start,end):
        p_c,p_r = end
        g = self.calculate_route(start,end)
        route = []
        route.append(end)
        length = 0
        while True:
            pre = g[p_r][p_c]
            if pre == -1:
                return (False,0)
            route.append(pre)
            if pre ==start or pre==-1:
                break
            p_c,p_r = pre
            length+=1
        route.reverse()
        return (route[:4],length)

    def update_blocking(self,n_blocking):
        self.blocking = n_blocking

class Acell:

    def __init__(self,pos,neighboors):
        self.coor = pos
        self.contain = 3
        self.neighs = neighboors

class Turret:

    def __init__(self,pos):
        self.fire_rate = 1
        self.damage = 1
        self.range = 10
        #index of rect in rect array
        self.pos = pos

    def in_range(self,pos):
        ydif = pos[1]*YMULTI-self.pos[1]*YMULTI
        xdif = pos[0]*XMULTI-self.pos[0]*XMULTI
        dist = (ydif**2+xdif**2)**0.5
        if dist<=self.range*XMULTI:
            return True
def angle_to(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    xdif = x1-x2
    ydif = y1-y2
    dist = (ydif**2+xdif**2)**0.5

    if xdif==0:
        if y2>y1:
            return 270
        else:
            return 90
    if ydif==0:
        if x2>x1:
            return 0
        else:
            return 180
    ans = math.degrees(math.acos(ydif/dist))
    if xdif
    return math.degrees(math.acos(ydif/dist))

class Turret_Handler:
    def __init__(self):
        self.turrets = []

    def get_all(self):
        positions = [self.turrets[j].pos for j in range(len(self.turrets))]
        return positions

    def add_turret(self,pos):
        self.turrets.append(Turret(pos))

    #returns rects of projectiles that have not moved
    def fire_turrets(self,enemies_pos):
        projectiles = []
        for i in range(len(self.turrets)):
            t_x,t_y = self.turrets[i].pos
            t_range = self.turrets[i].range
            for j in range(len(enemies_pos)-1,-1,-1):
                e_x,e_y = enemies_pos[j]
                #if ((t_x-e_x)**2+(t_y-e_y)**2)**0.5<t_range:
                if self.turrets[i].in_range((e_x,e_y)):
                    direction = angle_to((t_x,t_y),(e_x,e_y))
                    projectiles.append(Projectile( (t_x*XMULTI,t_y*YMULTI),direction,t_range))
                    break
        return projectiles
#
#
#//////////////////////////////thisssss
class Projectile:
    def __init__(self,pos,direction,d_range):
        self.surface = pygame.surface.Surface((50,50))
        self.surface.fill((0,250,200))
        self.rect = pygame.rect.Rect(pos[0],pos[1],50,50)
        self.dir = direction
        self.dist = 0
        self.range = d_range
        speed = 2
        dx = 0
        dy = 0
        if self.dir>0:
            if self.dir>90:
                dy = speed*math.sin(180-self.dir)
                dx = speed*math.cos(180-self.dir)
            else:
                dy = speed*math.sin(self.dir)
                dx = speed*math.cos(self.dir)
        else:
            if self.dir<-90:
                dy = speed*math.sin(180+self.dir)
                dx = speed*math.cos(180+self.dir)
            else:
                dy = speed*math.sin(self.dir)
                dx = speed*math.cos(self.dir)
        self.dx = dx
        self.dy = dy

    def draw(self,screen):
        screen.blit(self.surface,self.rect)

    def update(self):
        if self.dist>self.range:
            return False
        n_rect = list(self.rect.topleft)
        x,y = self.rect.topleft
        n_rect[0] +=self.dx
        n_rect[1] +=self.dy
        self.rect.topleft = n_rect
        self.dist+=(self.dx**2+self.dy**2)**0.5
        return True

class Projecile_Handler:
    def __init__(self):

        self.projectiles = []

    def add_projectiles(self,projectiles):
        self.projectiles += projectiles

    def update_all(self):
        for i in range(len(self.projectiles)):
            self.projectiles[i].update()

    #do something in OverGrid to translate pos to rects
    def check_collisions(self,enemies_rect):
        damage_list = [0 for i in range(len(enemies_rect))]
        p_rects = [i.rect for i in self.projectiles]
        disclude = []
        for i in range(len(enemies_rect)):
            index = enemies_rect[i].collidelist(p_rects)
            #damage_list[i]+=self.projectiles[index].damage
            if(index!=-1):
                damage_list[i]+=1
            disclude.append(index)

        self.projectiles = [self.projectiles[i] for i in range(len(self.projectiles)) if i not in disclude]
        return damage_list

    def draw_all(self,screen):
        for i in self.projectiles:
            i.draw(screen)


class Enemy:

    #pos being the position along the path
    def __init__(self):
        self.health = 1
        self.speed = 1
        self.path = []
        self.pos = (0,0)
        self.path_left = 0

    #return 0 if end reached

    def update_path(self,a_grid):

        m_end = a_grid.maze_end
        path,left = a_grid.get_route(self.pos,m_end)
        #print path
        if self.health<=0:
            return 0
        if self.pos==m_end:
            return 0
        if path==False:
            pass
        elif len(self.path)<=1 and self.pos!=(0,0):
            return 0
        else:
            self.path = path[1:]
            self.pos = self.path[0]
        self.path_left=left
    def take_damage(self,damage):
        self.health-=damage

class Enemy_Handler:
    def __init__(self):

        self.enemies = []
    
    def get_all(self):
        positions = [self.enemies[j].pos for j in range(len(self.enemies))]
        return positions

    def add_enemy(self,enemy):
        self.enemies.append(enemy)

    def update_paths(self,grid):
        temps = self.enemies
        store = []

        for i in range(len(self.enemies)):
            x =self.enemies[i].update_path(grid)
            if x!=0:
                store.append(self.enemies[i])
        self.enemies=store
    def update_damage(self,damage):

        for i in range(len(damage)):
            self.enemies[i].take_damage(damage[i])


class OverGrid:
    def __init__(self,dims,celldims):

        self.surface = pygame.surface.Surface((dims[0],dims[1]))
        self.surface.fill((100,0,0))
        self.rect = pygame.rect.Rect(0,0,dims[0],dims[1])
        self.rows = dims[1] // celldims[1]
        self.columns = dims[0] // celldims[0]

        #eventual class handlers
        self.enemies = []
        self.ne = Enemy_Handler()
        self.turrets = Turret_Handler()
        self.projectiles = Projecile_Handler()
        self.walls = [ [False for i in range( self.columns )] for j in range( self.rows )]
        self.blocking = [ [False for i in range( self.columns )] for j in range( self.rows )]

        self.algorithm_grid = Agrid(dims,celldims)

        
        rowm = dims[1] // self.rows
        columnm = dims[0] // self.columns
        #multipliers
        
        #turret image, cell background, monsters
        self.cellimages = ((100,0,0),(0,100,0),(100,100,0),(0,0,0),(0,200,200))
        
        self.basic = pygame.surface.Surface((celldims[0],celldims[1]))

        #cellarray[row][column]

        #gridmap
        #0 = empty
        #1 = turret
        #2 = wall
        #3 = enemy
        #4 = path
        #enemies and walls priority over all with wall #1 priority
        self.gridmap = [ [0 for i in range( self.columns )] for j in range( self.rows )]
        self.rectarray = [ [pygame.rect.Rect(x*columnm,y*rowm,celldims[0],celldims[1]) for x in range(self.columns)] for y in range(self.rows) ]

        fours = ((-1,0),(0,-1),(1,0),(0,1))

    def draw(self,screen):
        y = 0
        for i in self.rectarray:
            x = 0
            for j in i:
                #print j
                self.basic.fill((100,0,0))

                index = self.gridmap[y][x]
                self.basic.fill(self.cellimages[index])
                self.surface.blit(self.basic,j)
                x+=1
            y+=1
        screen.blit(self.surface,self.rect)
        self.projectiles.draw_all(screen)

    def update_gridmap(self):
        e_poss = self.ne.get_all()

        for i in range(self.rows):
            for j in range(self.columns):
                if (j,i) in e_poss:
                    self.gridmap[i][j] = 3
                else:
                    if self.gridmap[i][j] == 3:
                        self.gridmap[i][j] = 0


    def build(self,pos):
        y = 0
        for i in self.rectarray:
            x = 0
            for j in i:
                if j.collidepoint(pos):
                    current = self.gridmap[y][x]
                    wall = self.walls[y][x]

                    if wall:
                        self.walls[y][x]=False
                        self.gridmap[y][x]=0
                        self.blocking[y][x]=False
                        return
                    elif not wall and current==0:
                        self.walls[y][x]=True
                        self.gridmap[y][x]=2
                        self.blocking[y][x]=True
                        return
                    else:
                        pass

                x+=1
            y+=1

    def build_t(self,pos):
        y = 0
        for i in self.rectarray:
            x = 0
            for j in i:
                if j.collidepoint(pos):
                    current = self.gridmap[y][x]
                    wall = self.walls[y][x]

                    if wall:
                        return
                    elif not wall and current==0:
                        self.gridmap[y][x]=1
                        self.blocking[y][x]=True
                        self.turrets.add_turret((x,y))
                        return
                    else:
                        pass

                x+=1
            y+=1
    def tick(self):
        self.algorithm_grid.update_blocking(self.blocking)
        self.update_gridmap()
        self.ne.update_paths(self.algorithm_grid)

        enemy_positions = self.ne.get_all()
        enemy_rects = [self.rectarray[i[1]][i[0]] for i in enemy_positions]

        projectiles = self.turrets.fire_turrets(enemy_positions)
        self.projectiles.add_projectiles(projectiles)
        d_list = self.projectiles.check_collisions(enemy_rects)
        self.ne.update_damage(d_list)

    def spawn(self):
        new_enemy = Enemy()
        new_enemy.update_path(self.algorithm_grid)
        self.ne.add_enemy(new_enemy)




def main():
    sdims = (600,600)
    cdims = (30,30)
    screens = pygame.display.set_mode(sdims)
    grid = OverGrid(sdims,cdims)
    running = 1
    while running ==1:
        grid.tick()
        screens.fill((0,0,0))
        pygame.time.wait(100)
        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                grid.spawn()
            if i.type == pygame.MOUSEBUTTONDOWN:
                grid.build_t(i.pos)

            if i.type == pygame.QUIT:
                pygame.quit()
                return 0
        grid.draw(screens)
        
        pygame.display.flip()

main()
