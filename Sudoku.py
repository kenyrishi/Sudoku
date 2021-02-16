import pygame
from pygame.locals import *

grid = [[0,0,0,0,0,0,0,0,0],
        [0,3,0,0,0,0,1,6,0],
        [0,6,7,0,3,5,0,0,4],
        [6,0,8,1,2,0,9,0,0],
        [0,9,0,0,8,0,0,3,0],
        [0,0,2,0,7,9,8,0,6],
        [8,0,0,6,9,0,3,5,0],
        [0,2,6,0,0,0,0,9,0],
        [0,0,0,0,0,0,0,0,0]]


BLACK = pygame.Color(0, 0, 0)         # Black
WHITE = pygame.Color(255, 255, 255)   # White
GREY = pygame.Color(128, 128, 128)   # Grey
RED = pygame.Color(255, 0, 0)       # Red



pygame.init()
FPS = 30
FramePerSec = pygame.time.Clock()



screen = pygame.display.set_mode((450,450))
screen.fill(WHITE)
pygame.display.set_caption("sukoku program")






def createGrid():
    width = 30
    height = 30
    space = 60
    for row in range(9):
        for column in range(9):
            pygame.draw.rect(screen, GREY,
                             [width * column + space,
                                height * row + space,
                              width,
                              height],1)

    for i in range(2):
        pygame.draw.line(screen,GREY,
                         (3*width*(i+1)+space,space),
                         (3*width*(i+1)+space,space+9*height), 5)

    
    for i in range(2):
        pygame.draw.line(screen,GREY,
                         (space,3*width*(i+1)+space),
                         (space+9*height,3*width*(i+1)+space), 5)                         


def placeSquares():
    global grid

    myFont = pygame.font.SysFont("Times New Roman", 24)
    
    for i in range(9):
        for j in range(9):
            num = str(grid[i][j])
            if num == "0":
                num = " "
            squares = myFont.render(str(num),1,BLACK)
            screen.blit(squares,(70+30*j,60+30*i))
    

def gridPrint():
    global grid
    for i in range(9):
        print(" ".join(str(x) for x in grid[i]))

def check(y,x,n):
    global grid
    for i in range(9):
        if grid[y][i] == n:
            return False

    for i in range(9):
        if grid[i][x] == n:
            return False

    sx = (x//3)*3
    sy = (y//3)*3

    for i in range(3):
        for j in range(3):
            if grid[sy+i][sx+j] == n:
                return False

    return True



def solve():
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range (1,10):
                    if check(y,x,n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0

                return
    gridPrint()
    #input("hello")



#gridPrint(grid)
#print('\n\n')

solve()
screen.fill(WHITE)
createGrid()

placeSquares()


running = True

a = True

while running:
    #pygame.draw.circle(screen, RED, (200,50), 30)
    #pygame.draw.rect(screen, BLACK, (100, 200, 100, 50), 2)
    #solve()
    #screen.fill(WHITE)
    #createGrid()
    #solve()
    #placeSquares()
    
    




    
    pygame.display.update()
    FramePerSec.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            running = False



