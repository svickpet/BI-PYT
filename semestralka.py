import numpy as np
import sys
from PIL import Image
from copy import deepcopy


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
    for line in data:
        for pixel in line:
            for i in range(len(pixel)):
                pixel[i] = pixel[i] + (255 - pixel[i]) * (1 / 4)
    return data

# ------------------------------------------------------------------

def darker(data):
    for line in data:
        for pixel in line:
            for i in range(len(pixel)):
                pixel[i] = pixel[i] * (1 - 1 / 2)
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

def applyConvMask(data, y, x, convolutionMask, constant):

    if len(data.shape) == 2:
        channels = 1
    else:
        channels = data.shape[2] 
   
    l = ()
  
    if 0 < x < width-1 and 0 < y < height-1:
        l += (data[y-1:y+2 , x-1:x+2],)

    else:
        return 0
    
    #for i in range(-1, 2):
    #    for j in range(-1, 2):
    #        if 0 <= x + j < width and 0 <= y + i < height:
    #           
    #            pixelR += data[y + i, x + j, 0] * convolutionMask[1 + i, 1 + j] * constant
    #            pixelG += data[y + i, x + j, 1] * convolutionMask[1 + i, 1 + j] * constant
    #            pixelB += data[y + i, x + j, 2] * convolutionMask[1 + i, 1 + j] * constant

    #print(l)

    n = ()
    for x in l:
        #print(x)
        n += ((x*convolutionMask).sum() * constant,)

    #print("...")
    #print(n[0])
    return n[0]

# ------------------------------------------------------------------

def blur(data, width, height):
    # convolutionMask = numpy.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    # constant = 1 / 9
    convolutionMask = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    constant = 1 / 16

    newData = np.zeros_like(data)

    for y in range(0, height):
        for x in range(0, width):
            newData[y, x] = applyConvMask(data, y, x, convolutionMask, constant)

    return newData

# ------------------------------------------------------------------

def sharpen(data, width, height):
    # convolutionMask = numpy.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    # constant = 1 / 9
    convolutionMask = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    constant = 1/2

    newData = np.zeros_like(data)

    for y in range(0, height):
        for x in range(0, width):
            newData[y, x] = applyConvMask(data, y, x, convolutionMask, constant)

# ------------------------------------------------------------------

def edges(data, width, height):
    data = grey(data)
    data = blur(data, width, height)

    convolutionMask = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    constant = 1/4

    # convolutionMask = numpy.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    # constant = 1

    newData = np.zeros_like(data)
    # data = grey(data)

    # for line in data:
    # for pixel in line:
    for y in range(0, height):
        for x in range(0, width):
            newData[y, x] = applyConvMask(data, y, x, convolutionMask, constant)

    return newData

# ------------------------------------------------------------------

def rotate(data, width, height, angle):    
    newData = np.zeros_like(data)

    tmp = angle // 90
    print( str(angle) + " " + str(tmp) )

    # 90
    if tmp == 1:
        for (i, line) in enumerate(data):         
            newData[i] = line[::-1]
        newData = np.transpose(newData, (1,0,2))
    # 180
    elif tmp == 2:
        for (i, line) in enumerate(data):    
            # from bottom = reversed line
            newData[-i] = line[::-1]
    # 270
    elif tmp == 3:
        for (i, line) in enumerate(data):         
            newData[-i] = line[::1]
        newData = np.transpose(newData, (1,0,2))
    # 360
    elif tmp == 4:
        return data

    return newData

# ------------------------------------------------------------------

def letsDoOperations(data, w, h):
    operations = sys.argv[2:]
    mode = 'RGB'
    print("Obraz se zpracovává...")

    for x in operations:
        if x == 'inv':
            data = inverse(data)

        elif x == 'grey':
            data = grey(data)
            mode = 'L'

        elif x == 'light':
            data = lighter(data)

        elif x == 'dark':
            data = darker(data)

        elif x == 'edges':
            data = edges(data, w, h)
            mode = 'L'

        elif x == 'h-flip':
            data = horizontalFlip(data, w)

        elif x == 'v-flip':
            data = verticalFlip(data, h)

        elif x == 'blur':
            data = blur(data, w, h)

        elif x == 'sharp':
            data = sharpen(data, w, h)

        elif 'rotate' in x:
            data = rotate(data, w, h, int( x.split("-")[1] ))
        else:
            if x != 'show':
                print("Tuto operaci neznám: " + x)
            continue

            #newIm = Image.fromarray(data, 'RGB')
        out = Image.fromarray(data, mode) 	
        out.save(x + '.jpg')

        #if 'show' in sys.argv:        
        #    out.show()

        out.show()

# ------------------------------------------------------------------
# ------------------------------------------------------------------

if len(sys.argv) == 2 and sys.argv[1] == 'help':
    # TODO obarvit
    tmp = '\n"semestralka.py cesta/k/obrazku operace"\n\n' \
          'Dostupné operace:\n-----------------\n' \
          'inv - inverzní obraz\n' \
          'grey - převod do odstínů šedi\n' \
          'light - zesvětlení\n' \
          'dark - ztmavení\n' \
          'edges - zvýraznění hran\n' \
          'h-flip - horizontální převrácení\n' \
          'v-flip - vertikální převrácení\n'

    print(tmp)
elif len(sys.argv) >= 2:
    try:
        pass
        im = Image.open(sys.argv[1])

        width, height = im.size

        imageData = np.asarray(im)

        im.show()

        letsDoOperations(imageData, width, height)

    except IOError:
        print('Obrázek nebyl nalezen, nebo chybí práva pro jeho otevření.')
        sys.exit(0)

else:
    print('Pro nápovědu napište "semestralka.py help"')
