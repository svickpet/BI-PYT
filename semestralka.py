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
    #print(g2.shape)
    #for line in data:
    #    for pixel in line:
    #        pixel[1] = pixel[2] = pixel[0]
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
    for line in data:
        for i in range(width // 2):
            tmp = list(line[i])
            (line[i], line[width - 1 - i]) = line[width - 1 - i], tmp

    return data


# ------------------------------------------------------------------


def verticalFlip(data, height):
    for i in range(height // 2):
        tmp = deepcopy(data[i])  # TODO jde to i bez deepcopy?
        data[i], data[height - 1 - i] = data[height - 1 - i], tmp

    return data


# ------------------------------------------------------------------


def applyConvMask(data, y, x, convolutionMask, constant):
    # convolutionMask = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    # convolutionMask = numpy.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    # constant = 1

    pixelR = pixelG = pixelB = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + j < width and 0 <= y + i < height:
                # for k in range(len(data)):
                pixelR += data[y + i, x + j, 0] * convolutionMask[1 + i, 1 + j] * constant
                pixelG += data[y + i, x + j, 1] * convolutionMask[1 + i, 1 + j] * constant
                pixelB += data[y + i, x + j, 2] * convolutionMask[1 + i, 1 + j] * constant

                # print(str(x + i) + ' ' + str(y + j) + " - " + str(1+i) + " " + str(1+j))

                # pixelR %= 256
                # pixelG %= 256
                # pixelB %= 256

    pixel = (pixelR, pixelG, pixelB)
    # print(pixel)
    return pixel


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

    return newData


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

        elif x == 'h-flip':
            data = horizontalFlip(data, w)

        elif x == 'v-flip':
            data = verticalFlip(data, h)

        elif x == 'blur':
            data = blur(data, w, h)

        elif x == 'sharp':
            data = sharpen(data, w, h)

        else:
            if x != 'show':
                print("Tuto operaci neznám: " + x)
            continue

            #newIm = Image.fromarray(data, 'RGB')
        out = Image.fromarray(data, mode) 	
        out.save(x + '.jpg')

        if 'show' in sys.argv:        
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
