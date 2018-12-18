import numpy as np
import sys
from PIL import Image
from copy import deepcopy
import os

# TODO ukladani obrazku, ne zobrazovani


def inverse(data):
    data = 255 - data
    return data

# ------------------------------------------------------------------

def grey(data):
    # print(data[1])

    g = (0.299, 0.587, 0.114) * data
    g2 = np.sum(g, axis=2)
    data = (g2 + 0.5).astype(dtype=np.uint8) 	# pretypujeme

    return data

# ------------------------------------------------------------------

def lighter(data):
    tmp = 1.5 * data.astype(dtype=np.uint16)
    
    data = np.clip(tmp,0,255)
    data = data.astype(dtype=np.uint8)
    
    #for line in data:
    #    for pixel in line:
    #       for i in range(len(pixel)):
    #            pixel[i] = pixel[i] + (255 - pixel[i]) * (1 / 4)
    return data

# ------------------------------------------------------------------

def darker(data):
    tmp = 0.5 * data
    data = tmp.astype(dtype=np.uint8)
    return data

# ------------------------------------------------------------------

def horizontalFlip(data, width):

    newData = np.zeros_like(data)

    for (i, line) in enumerate(data):         
        newData[i] = line[::-1]

    return newData

# ------------------------------------------------------------------

def verticalFlip(data, height):

    newData = np.zeros_like(data)

    for (i, line) in enumerate(data):         
        newData[-i] = line

    return newData

# ------------------------------------------------------------------

def applyConvMask(data, y, x, w, h, convolutionMask, constant):

    if len(data.shape) == 2:
        channels = 1
        tmp = data.shape + (1,)
        data = data.reshape(tmp)
    else:
        channels = data.shape[2] 
   
    n = ()
    l = np.zeros_like(convolutionMask)

    if 0 <= x < w and 0 <= y < h:
        #print(str(x) + " " + str(y))
        for i in range(channels):
            l = data[y:y+3 , x:x+3,i]
            k = (l*convolutionMask).sum() * constant
            if k > 255:
                k = 255
            n += (k,)
        
    else:
        return 0

    if channels == 1:
        return n[0]    
    return n

# ------------------------------------------------------------------

def blur(data, width, height, ch):
    convolutionMask = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    constant = 1 / 9
    #convolutionMask = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    #constant = 1 / 16

    if ch == 1:
        pad = 1
    else:
        pad = ((1,1),(1,1),(0,0))

    dataBorder = np.pad(data, pad_width=pad, mode='symmetric')

    newData = np.zeros_like(data)

    for y in range(0, height):
        for x in range(0, width):
            newData[y, x] = applyConvMask(dataBorder, y, x, width, height, convolutionMask, constant)

    return newData

# ------------------------------------------------------------------

def edges(data, width, height):
    data = blur(data, width, height, 1)

    convolutionMask = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    constant = 1/4

    #convolutionMask = np.array([[1, 0, -1], [0, 0, 0], [-1, 0, 1]])
    #constant = 1

    dataBorder = np.pad(data, 1, mode='symmetric')
    newData = np.zeros_like(data)

    # for line in data:
    # for pixel in line:
    for y in range(0, height):
        for x in range(0, width):
            newData[y, x] = applyConvMask(dataBorder, y, x, width, height, convolutionMask, constant)

    return newData

# ------------------------------------------------------------------

def rotate(data, width, height, code, ch):    
    newData = np.zeros_like(data)

    direction = 'doleva' if code[0:1] == 'l' else 'doprava'
    angle = int(code[1:]) % 360

    tmp = angle // 90
    print( "Otáčím o úhel " + str(tmp*90) + "° " + direction + "...")

    if direction == 'doprava':
        tmp = 4 - tmp

    if ch == 1:
        transCoord = (1,0)
    else:
        transCoord = (1,0,2)

    # 90
    if tmp == 1:
        for (i, line) in enumerate(data):         
            newData[i] = line[::-1]
        newData = np.transpose(newData, transCoord)
    # 180
    elif tmp == 2:
        for (i, line) in enumerate(data):    
            # from bottom = reversed line
            newData[-i] = line[::-1]
    # 270
    elif tmp == 3:
        for (i, line) in enumerate(data):         
            newData[-i] = line[::1]
        newData = np.transpose(newData, transCoord)
    # 360
    elif tmp == 0:
        return data

    return newData

# ------------------------------------------------------------------

def letsDoOperations(data, w, h):
    operations = sys.argv[2:]
    mode = 'RGB'

    if len(data.shape) == 2:
        channels = 1
        mode = 'L'
    else:
        channels = data.shape[2] 


    print("Obraz se zpracovává...")

    for x in operations:
        if x == 'inv':
            print( "Invertuji...")
            data = inverse(data)

        elif x == 'grey' or x == 'gray':
            if mode == 'L':
                print("Obraz již je černobílý.")
                break
            print( "Převádím do odstínů šedi...")
            data = grey(data)
            mode = 'L'

        elif x == 'light':
            print( "Zesvětluji...")
            data = lighter(data)

        elif x == 'dark':
            print( "Ztmavuji...")
            data = darker(data)

        elif x == 'edges':
            print( "Vykresluji hrany...")
            if mode != 'L':
                data = grey(data)
            data = edges(data, w, h)
            mode = 'L'

        elif x == 'h-flip':
            print( "Převracím vodorovně...")
            data = horizontalFlip(data, w)

        elif x == 'v-flip':
            print( "Převracím svisle...")
            data = verticalFlip(data, h)

        elif x == 'blur':
            print( "Rozmazávám...")
            data = blur(data, w, h, channels)

        elif 'rotate' in x:
            data = rotate(data, w, h, x.split("-")[1], channels)
        else:
            if x != 'show':
                print("Tuto operaci neznám: " + x)
            continue

            #newIm = Image.fromarray(data, 'RGB')
    
    out = Image.fromarray(data, mode)

    if 'show' in sys.argv:
        operations.remove('show')       
        out.show()
 	
    name = ''.join(operations) + '.jpg'
    print("Ukládám obrázek pod názvem: " + name )
    out.save(name)

# ------------------------------------------------------------------
# ------------------------------------------------------------------

cols, rows = os.get_terminal_size()

if len(sys.argv) == 2 and sys.argv[1] == 'help':
    C = '\033[92m'
    END = '\033[0m'

    tmp = '\n' + '-'*cols \
            + '\nObecný předpis pro použití konzolové aplikace:' \
          + C + '\n"semestralka.py cesta/k/obrazku operace"\n' + END \
          + '-'*cols + '\n\n'

    tmp += C + 'Dostupné operace:' + END + '\n-----------------\n' \
          + C + 'inv' + END + ' - inverzní obraz\n' \
          + C + 'grey / gray' + END + ' - převod do odstínů šedi\n' \
          + C + 'light' + END + ' - zesvětlení\n' \
          + C + 'dark' + END + ' - ztmavení\n' \
          + C + 'edges' + END + ' - zvýraznění hran\n' \
          + C + 'h-flip' + END + ' - horizontální převrácení/zrcadlení\n' \
          + C + 'v-flip' + END + ' - vertikální převrácení/zrcadlení\n' \
          + C + 'rotate-l(úhel)' + END + ' - rotace o násobky 90° proti směru hodinových ručiček, doleva\n' \
          + C + 'rotate-r(úhel)' + END + ' - rotace o násobky 90° po směru hodinových ručiček, doprava\n' \
          '-- funkce bere i úhly vyšší než 360°\n' \
          '-- při zadání jiného úhlu než násobek 90, se úhel přepočítá na nejnižší násobek 90\n' \
          + C + 'blur' + END + ' - rozostření\n' \
          + C + 'edges' + END + ' - zvýraznění hran\n\n' \
          'Operace je možné řetězit.\n' \
          +'-'*cols + '\n'

    print(tmp)
elif len(sys.argv) >= 2:
    try:
        pass
        im = Image.open(sys.argv[1])

        width, height = im.size

        imageData = np.asarray(im)

        #im.show()

        data = letsDoOperations(imageData, width, height)



    except IOError:
        print('Obrázek nebyl nalezen, nebo chybí práva pro jeho otevření.')
        sys.exit(0)

else:
    print('Pro nápovědu napište "semestralka.py help"')
