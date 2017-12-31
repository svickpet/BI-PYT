import numpy
import sys
from PIL import Image


def letsDoOperations(data):
    pass

# ------------------------------------------------------------------
# ------------------------------------------------------------------

if len(sys.argv) == 2 and sys.argv[1] == 'help':
    # TODO obarvit
    tmp = '\n"semestralka.py cesta/k/obrazku operace"\n\n' \
          'Dostupné operace:\n-----------------\n' \
          'inv - inverzní obraz\n' \
          'sed - převod do odstínů šedi\n'

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
