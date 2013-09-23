import pygame
import random

pygame.init()
w=600
h=600
gridx = 20
gridy = 20
speed = (w/gridx)
screen = pygame.display.set_mode((w,h))
running =0
#class Snake - encapsulates head and body inside one object while adding more functionability
class Block:

    def __init__(self,pos,dims):
        self.col = (random.randint(0,250),random.randint(0,250),random.randint(0,250))
        self.image = pygame.Surface((dims[0]-1,dims[1]-1))
        self.image.fill(self.col)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def draw(self,screen):
        screen.blit(self.image,self.rect)

        
class Head:
            
    def __init__(self,pos,vec,dims):
        self.col = (200,0,0)        
        self.image = pygame.Surface((dims[0]-1,dims[1]-1))
        self.image.fill(self.col)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0]+1,pos[1]+1)
        self.xvec = vec[0]
        self.yvec = vec[1]
        
    def update(self,dims):
        
        x=self.rect.topleft[0]
        y=self.rect.topleft[1]
        x+=self.xvec
        y+=self.yvec
        if x<0 or x>dims[0] or y<0 or y>dims[1]:
            return 0
        
        self.rect.topleft = [x,y]

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        
class S_body:

        
    #for all the body
    #eatcol colour of fruit
    def __init__(self,prev_body,eatcol):
        
        self.image = prev_body.image
        self.image.fill(eatcol)
        self.rect = self.image.get_rect()
        prevpos = prev_body.rect.topleft
        prevvec = (prev_body.xvec,prev_body.yvec)
        #self.rect.topleft = [prevpos[0]-20*prevvec[0],prevpos[1]-20*prevvec[1]]
        self.rect.topleft = [prevpos[0],prevpos[1]]
        self.xvec = 0
        self.yvec = 0

        
    def update(self,dims,prev_body):
    
        x=self.rect.topleft[0]
        y=self.rect.topleft[1]
        if(self.xvec == 0 and self.yvec == 0):
            pass
        else:
            x+=self.xvec
            y+=self.yvec
        self.rect.topleft = [x,y]
        self.xvec = prev_body.xvec
        self.yvec = prev_body.yvec

    def draw(self,screen):
        screen.blit(self.image,self.rect)

sx = 0
sy = 0

prevkey =0
keys = (pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT)
keynot = {pygame.K_UP:pygame.K_DOWN,pygame.K_DOWN:pygame.K_UP,pygame.K_LEFT:pygame.K_RIGHT,pygame.K_RIGHT:pygame.K_LEFT}

while (True):
    events=pygame.event.wait()
    
    if events.type == pygame.KEYDOWN:

        if events.key == pygame.K_UP:
            sy=-speed
        if events.key == pygame.K_DOWN:
            sy=speed
        if events.key == pygame.K_LEFT:
            sx=-speed
        if events.key == pygame.K_RIGHT:
             sx=speed
        if(events.key in keys):
            prevkey = events.key
            break

def block_pos(heads,bodys):
    xlist = range(0,w,speed)
    ylist = range(0,h,speed)
    while(True):
        x = xlist[random.randint(0,len(xlist)-1)]+1
        y = ylist[random.randint(0,len(ylist)-1)]+1
        if(heads.rect.collidepoint(x,y)):
            continue
        p = 0
        for i in bodys:
            if (i.rect.collidepoint(x,y)):
                p=1
                break
        if p==0:
            return (x,y)
                
head = Head((w/2,h/2),(sx,sy),(w/gridx,h/gridy))
body = []
count=0
block = Block(block_pos(head,body),(w/gridx,h/gridy))

while(running==0):
    
    screen.fill((0,200,0))

    for i in pygame.event.get():
        
        if i.type == pygame.QUIT:
            
            running =1
        if (i.type == pygame.KEYDOWN)and i.key != keynot[prevkey]:
            
            if i.key == pygame.K_UP:
                
                prevkey = i.key
                head.xvec=0
                head.yvec=-speed
                
            elif i.key == pygame.K_DOWN:
                
                prevkey = i.key
                head.xvec=0
                head.yvec=speed
                
            elif i.key == pygame.K_LEFT:
                
                 prevkey = i.key
                 head.xvec=-speed
                 head.yvec=0
                 
            elif i.key == pygame.K_RIGHT:
                
                 head.xvec=speed
                 head.yvec=0
                 prevkey = i.key
                 
            else:
                
                if len(body)==0:
                    
                    body.append(S_body(head))
                else:
                    
                    body.append(S_body(body[count]))
                    count+=1
    
              
    if(head.update((w,h))==0):
        running = 1
    l = len(body)-1
    while l>=0:
        if l==0:
            
            body[0].update((w,h),head)
            body[0].draw(screen)
            l-=1
            continue
        
        body[l].update((w,h),body[l-1])
        body[l].draw(screen)
        l-=1
    for i in body:
        if (head.rect.colliderect(i.rect)):
            running =1
    if (head.rect.colliderect(block.rect)):
        if len(body)==0:
                    
            body.append(S_body(head,block.col))
        else:
                    
            body.append(S_body(body[count],block.col))
            count+=1
        block = Block(block_pos(head,body),(w/gridx,h/gridy)) 
    block.draw(screen)
    head.draw(screen)
    pygame.display.flip()
    if running ==0:
        pygame.time.wait(150)
    else:
        pass
    


            
pygame.quit()
