import numpy
import sys
from PIL import Image
from copy import deepcopy

# TODO ukladani obrazku, ne zobrazovani
# TODO rozostreni obrazku konvolucni maska: 1,1,1 1,1,1 1,1,1 * 1/9
#    nebo [[1,2,1], [2,4,2,], [1,2,1]] * 1/16 - Gauss"


def inverse(data):
    data = 255 - data
    return data


# ------------------------------------------------------------------


def grey(data):
    # print(data[1])
    for line in data:
        for pixel in line:
            pixel[1] = pixel[2] = pixel[0]
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


def applyConvMask(data, y, x, convolutionMask, constant):  # TODO parametr convolutionMask, constant
    # convolutionMask = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    # convolutionMask = numpy.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    # constant = 1

    pixelR = pixelG = pixelB = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            # TODO okraje
            if 0 <= x + j < height and 0 <= y + i < width:
                # for k in range(len(data)):
                pixelR += data[y + i, x + j, 0] * (convolutionMask[1 + i, 1 + j] * constant)
                pixelG += data[y + i, x + j, 1] * (convolutionMask[1 + i, 1 + j] * constant)
                pixelB += data[y + i, x + j, 2] * (convolutionMask[1 + i, 1 + j] * constant)

                # print(str(x + i) + ' ' + str(y + j) + " - " + str(1+i) + " " + str(1+j))

                pixelR %= 256
                pixelG %= 256
                pixelB %= 256

    pixel = (pixelR, pixelG, pixelB)
    # print(pixel)
    return pixel


# ------------------------------------------------------------------


def edges(data):

    convolutionMask = numpy.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    constant = 1

    # data = grey(data)

    # for line in data:
    # for pixel in line:
    for y in range(0, height):
        for x in range(0, width):
            data[y, x] = applyConvMask(data, y, x, convolutionMask, constant)


# ------------------------------------------------------------------


def letsDoOperations(data, w, h):
    operations = sys.argv[2:]

    print("Obraz se zpracovává...")

    for x in operations:
        if x == 'inv':
            data = inverse(data)

        elif x == 'grey':
            data = grey(data)

        elif x == 'light':
            data = lighter(data)

        elif x == 'dark':
            data = darker(data)

        elif x == 'edges':
            edges(data)

        elif x == 'h-flip':
            horizontalFlip(data, w)

        elif x == 'v-flip':
            pass
            verticalFlip(data, h)

        else:
            print("Tuto operaci neznám: " + x)
            continue
        # TODO dalsi funkce

        newIm = Image.fromarray(data, 'RGB')
        newIm.show()


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
        im = Image.open(sys.argv[1]).convert('RGB')
        # print(im)

        imageData = numpy.array(im)
        # print(imageData)
        # print(len(imageData))

        width, height = im.size
        # print(str(width) + " " + str(height))
        # print("mode: " + im.mode)

        im.show()

        letsDoOperations(imageData, width, height)

    except IOError:
        print('Obrázek nebyl nalezen, nebo chybí práva pro jeho otevření.')
        sys.exit(0)

else:
    print('Pro nápovědu napište "semestralka.py help"')
