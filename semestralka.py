import numpy
import sys
from PIL import Image


def inv(data):
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


def light(data):
    for line in data:
        for pixel in line:
            for i in range(len(pixel)):
                pixel[i] = pixel[i] + (255 - pixel[i]) * (1/4)
    return data

# ------------------------------------------------------------------

def letsDoOperations(data):
    operations = sys.argv[2:]

    for x in operations:
        if x == 'inv':
            data = inv(data)

        elif x == 'grey':
            data = grey(data)

        elif x == 'light':
            data = light(data)


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
          'grey - převod do odstínů šedi\n'

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

        letsDoOperations(imageData)

    except IOError:
        print('Obrázek nebyl nalezen, nebo chybí práva pro jeho otevření.')
        sys.exit(0)

else:
    print('Pro nápovědu napište "semestralka.py help"')
