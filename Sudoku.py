import pygame
import requests
import json
#from pygame.locals import *

grid = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]

NUM_SQUARES = 9
DIFFICULTY = 2; #1,2,3

pygame.init()
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(128, 128, 128)
RED = pygame.Color(255, 0, 0)
WINDOW_SIZE = 450
GRID_SIZE = WINDOW_SIZE//NUM_SQUARES


def main():
    global screen,clock
    pygame.init()
    pygame.font.init()
    global num_font
    num_font = pygame.font.SysFont("Helvetica",round(GRID_SIZE*0.75))
    #myfont = pygame.font.SysFont('Comic Sans MS', round(grid_size*0.75))
    
    screen = pygame.display.set_mode((WINDOW_SIZE,WINDOW_SIZE))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()
    screen.fill(WHITE)


    r = requests.get(f"http://www.cs.utep.edu/cheon/ws/sudoku/new/?size={NUM_SQUARES}&level={DIFFICULTY}")
    response = r.json()
    if (response["response"]):
        squares = response["squares"]
        for i in squares:
            grid[i["y"]][i["x"]] = i["value"]
    
    
    createGrid()
    placeSquares()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #sys.exit()
            if event.type == pygame.KEYDOWN:
                solve()
                gridPrint()
                createGrid()
                placeSquares()
            

        pygame.display.flip()
        clock.tick(60)
    pygame.display.quit()
    pygame.quit()




def createGrid():
    for x in range(9):
        for y in range(9):
            rect = pygame.Rect(x*GRID_SIZE,y*GRID_SIZE,
                               GRID_SIZE,GRID_SIZE)
            pygame.draw.rect(screen,WHITE,rect)
            pygame.draw.rect(screen,BLACK,rect,1)

    for x in range(0,9,3):
        for y in range(0,9,3):
            rect = pygame.Rect(x*GRID_SIZE,y*GRID_SIZE,
                               3*GRID_SIZE,3*GRID_SIZE)
            pygame.draw.rect(screen,BLACK,rect,5)                      


def placeSquares():
    global grid

    myFont = pygame.font.SysFont("Times New Roman", 24)
    
    for i in range(9):
        for j in range(9):
            num = str(grid[i][j])
            if num == "0":
                num = " "
            squares = myFont.render(str(num),1,BLACK)
            screen.blit(squares,(GRID_SIZE*j+20,GRID_SIZE*i+15))
    

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

#solve()
#screen.fill(WHITE)
#createGrid()

#placeSquares()


if __name__ == "__main__":
    main()



