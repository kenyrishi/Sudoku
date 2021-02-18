import pygame
import requests
import json
#from pygame.locals import *

orig_grid = [[0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0]]

grid =  [[0 for x in range(9)] for y in range(9)] 

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
            orig_grid[i["y"]][i["x"]] = i["value"]
            grid[i["y"]][i["x"]] = i["value"]
    
    
    createGrid(grid)
    putSquares(grid)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #sys.exit()
            if event.type == pygame.KEYDOWN:
                if (solve(grid)):
                    pass
            

        pygame.display.flip()
        clock.tick(60)
    pygame.display.quit()
    pygame.quit()




def createGrid(grid):
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

def putSquares(grid):
    for i in range (9):
        for j in range (9):
            placeSquare(grid,j,i)

def placeSquare(grid,x,y):

    rect = pygame.Rect(y*GRID_SIZE+3,x*GRID_SIZE+3,GRID_SIZE-6,GRID_SIZE-6)
    pygame.draw.rect(screen,WHITE,rect)

    myFont = pygame.font.SysFont("Times New Roman", 28)
    
    num = str(grid[x][y])
    if num == "0":
        num = " "
    colour = BLACK
    if (grid[x][y] != orig_grid[x][y]):
        colour = GREY
    squares = myFont.render(str(num),1,colour)
    screen.blit(squares,(GRID_SIZE*y+18,GRID_SIZE*x+12))
    

def gridPrint(grid):
    for i in range(9):
        for j in range(9):
            print (grid[i][j], end = " ")
        print("")
    print("\n")

def check(y,x,n,grid):
    #global grid
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

def is_empty(grid,l):
    for i in range(9):
        for j in range(9):
            if (grid[i][j] == 0):
                l[0] = i
                l[1] = j
                return True    
    return False


def solve(grid):
    l = [0,0]
    if (not is_empty(grid,l)):
        return True
    row = l[0]
    col = l[1]

    for num in range(1,10):
        if (check(row,col,num,grid)):
            grid[row][col] = num
            placeSquare(grid,row,col)
            pygame.time.wait(3)
            pygame.display.update()
            
            if (solve(grid)):
                return True
            grid[row][col] = 0
        
    return False



#gridPrint(grid)
#print('\n\n')

#solve()
#screen.fill(WHITE)
#createGrid()

#placeSquares()


if __name__ == "__main__":
    main()



