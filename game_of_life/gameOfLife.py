import numpy
import random
import time
import os
import sys

#TODO barevne oznacit stari bunky - druhy kod
#TODO nemocny vydrzi jen nejakou dobu?

#TODO vysledek vzdy na konec 

Rules = {
    'default': ([2,3],[3]),
    'maze': ([1,2,3,4],[3]),
    'walls': ([2,3,4,5],[4,5,6,7,8]),
    'move': ([2,4,5],[3,6,8]),
    '34life': ([3,4],[3,4]),
    'coral': ([4,5,6,7,8],[3])
}

cols, rows = os.get_terminal_size()

height = rows  # rows
width = cols  # cols

size = width * height

cells = numpy.zeros((rows, cols), dtype=int)
illCells = numpy.zeros((rows, cols), dtype=int)
newCells = numpy.zeros((rows, cols), dtype=int)

# --------------------------------------------------------------
def aliveNeighbours(index):
    neighboursIndexes = set()
    alives = 0

    neighboursIndexes.add((index[0] - 1, index[1] - 1))  # up left
    neighboursIndexes.add((index[0], index[1] - 1))  # left
    neighboursIndexes.add((index[0] + 1, index[1] - 1))  # bottom left
    neighboursIndexes.add((index[0] + 1, index[1]))  # bottom
    neighboursIndexes.add((index[0] + 1, index[1] + 1))  # bottom right
    neighboursIndexes.add((index[0], index[1] + 1))  # right
    neighboursIndexes.add((index[0] - 1, index[1] + 1))  # up right
    neighboursIndexes.add((index[0] - 1, index[1]))  # up
 
    # is index correct?
    #for i in neighboursIndexes:
    alives = [cells[x[0],x[1]] for x in neighboursIndexes if 0 <= x[0] < rows and 0 <= x[1] < cols]
         #   alives += cells[i[0], i[1]]
 
    return (len(alives)-(alives.count(0)),2 in alives)

# --------------------------------------------------------------
def willBeDead(value, index, key):
    alives, willBeIll = aliveNeighbours(index)

    if value == 1:  # cell is alive or ill   
        if alives in Rules[key][0]:
            if willBeIll:
                return 2
            return 1
    elif value == 0:  # cell is dead
        if alives in Rules[key][1]:
            return 1       
    # keep ills
    #elif value == 2:
        #if alives in Rules[key][0]:
        #    illCells[index] -= 1
        #    if illCells[index] > 0:
        #        return 2
        #return 2
    #elif value == 2:
     #   if alives in Rules[key][0]:
      #      return 2
    return 0

# --------------------------------------------------------------
def showCells(cells):
    print("\033[0;0H")
    #row = 1
    #col = 1
    for i in range(0, rows):
        for j in range(cols):
            print(f"\033[{i};{j}H", end='', flush=True)
            if cells[i, j] == 0:
                print("\033[40m \033[0m", end='', flush=True)
            elif cells[i, j] == 1:
                print("\033[42m \033[0m", end='', flush=True)
            else:
                print("\033[41m \033[0m", end='', flush=True)
# --------------------------------------------------------------
def help():
    tmp = '\nname-of-file mode (ill) (save)\n\n' \
          'Modes:\n' \
          'default - original Game of Life (23/3)\n' \
          'maze - (1234/3)\n' \
          'walls - (2345/45678)\n' \
          'move - (245/368)\n' \
          '34life - (34/34)\n' \
          'coral - (45678/3)\n\n' \
          '"ill" - infectious cells (red colour)\n' \
          '"save" - save every generation into file\n'

    print(tmp)

# --------------------------------------------------------------
def saveGeneration(nthGeneration, cells):
    with open(f"./{nthGeneration}-gen.txt", mode='w', encoding="utf-8") as f:
        f.write(str(nthGeneration) + " " + str(width) + " " + str(height) + "\n")

        tmp = ""

        for x in cells:
            for y in x:
                tmp += str(y) + " "
        
        f.write(tmp + "\n")

# --------------------------------------------------------------
def openGeneration(fileName):
    with open(fileName, mode='r', encoding="utf-8") as f:
        numGen, width, height = f.readline().split()
        #print(numGen)  
        #print(width)
        #print(height)  
        cells = numpy.zeros((int(height), int(width)), dtype=int)      
        for line in f:
            #cells[i] = line;
            for num in line.split():      
                #print(num)

                if int(num) == 0:
                    print("\033[40m \033[0m", end='', flush=True)
                elif int(num) == 1:
                    print("\033[42m \033[0m", end='', flush=True)
                else:
                    print("\033[41m \033[0m", end='', flush=True)
                #return
    

# --------------------------------------------------------------
# --------------------------------------------------------------

if len(sys.argv) >= 2:
    if sys.argv[1] == 'help':
        help()
        exit()
    elif sys.argv[1] == 'open':   
        openGeneration(sys.argv[2]) 
        exit()
    elif sys.argv[1] in Rules:   
        key = sys.argv[1]
        #exit()

else:
    key = 'default'

#TODO small generation, medium, high? - // 4, //2, //1

#random points
for i in range(random.randint(1, size//4)):
    x = random.randint(0, rows - 1)
    y = random.randint(0, cols - 1)
    cells[x, y] = 1

if 'ill' in sys.argv:
    for i in range(random.randint(1, 20)):
        x = random.randint(0, rows - 1)
        y = random.randint(0, cols - 1)
        cells[x, y] = 2
        illCells[x,y] = 20

generation = 0

print("\033[2J\033[?25l")

try:
    while True:
        generation += 1
        for m in range(rows):
            for n in range(cols):
                x = cells[m, n]
                newCells[m, n] = willBeDead(x, (m, n), key)

        cells = newCells.copy()

        showCells(cells)
        if 'save' in sys.argv:
            saveGeneration(generation, cells)
        time.sleep(0.5)

except KeyboardInterrupt:
    print(f"\nEnd of Game of Life. Cells lived for {generation} generations.\033[?25h")
