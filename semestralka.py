import numpy
import sys
from PIL import Image

# TODO ukladani obrazku, ne zobrazovani


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
                pixel[i] = pixel[i] + (255 - pixel[i]) * (1/4)
    return data

# ------------------------------------------------------------------


def darker(data):
    for line in data:
        for pixel in line:
            for i in range(len(pixel)):
                pixel[i] = pixel[i] * (1 - 1/2)
    return data

# ------------------------------------------------------------------


def horizontalFlip(data, width):
    for line in data:
        for i in range(width//2):

            tmp = list(line[i])
            (line[i], line[width-1-i]) = line[width-1-i], tmp

    return data

# ------------------------------------------------------------------


def letsDoOperations(data, w, h):
    operations = sys.argv[2:]

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
            pass
            # edges(data)

        elif x == 'h-flip':
            horizontalFlip(data, w)

        elif x == 'v-flip':
            pass
            # verticalFlip(data)

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
