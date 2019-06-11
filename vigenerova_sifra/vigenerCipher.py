import string, sys

END = '\033[0m'
BLUE = '\033[34m'

oneLetter = {'a', 'i', 'o', 'u', 'k', 's', 'v', 'z'}

twoLetters = {'ac', 'an', 'at', 'ar', 'az', 'ba', 'by', 'co', 'ci', 'da', 'di',
              'do', 'eg', 'er', 'es', 'ha', 'ho', 'hu', 'id', 'ja', 'je', 'ji',
              'jo', 'ke', 'ku', 'li', 'ma', 'me', 'mi', 'mu', 'my', 'na', 'ne',
              'ni', 'no', 'ob', 'od', 'oj', 'ok', 'on', 'op', 'or', 'os', 'po',
              'se', 'si', 'ta', 'te', 'ti', 'to', 'tu', 'ty', 'uc', 'ud', 'um',
              'ul', 'uz', 've', 'vi', 'vy', 'za', 'ze'}


def codeString(understandable, secretPassword):
    cipher = ''
    word = ''
    secretPassword = secretPassword.upper()
    lengthPassword = len(secretPassword)
    i = 0

    for letter in understandable:

        l = ord(letter)

        l -= ord(secretPassword[i % lengthPassword]) - 65

        if letter.isupper():
            while l > ord('Z'):
                l -= 26
            while l < ord('A'):
                l += 26

        if letter not in string.ascii_letters:
            l = ord(letter)
            i -= 1

            if len(word) == 1 and word.lower() not in oneLetter:
                return ''

            if len(word) == 2 and word.lower() not in twoLetters:
                return ''

            word = ''

        else:
            word += chr(l)

        cipher += chr(l)

        i += 1

    return cipher

# ---------------------------------------------------------------------------------------


firstPhase = set()
res = set()


i = 0
with open("./cipher.txt", "r") as f:
    userInput = f.read()

    # first phase --------------------------------------------------
    # encoding few first words
    with open("./passwords.txt", "r") as g:
        for password in g:
            password = password[0:-1].lower()
            if password in firstPhase:
                continue
            
            cipher = codeString(userInput[0:208], password)
            if cipher == '':
                continue

            firstPhase.add((cipher, password))
            

    # second phase -------------------------------------------------
    # encoding all words
    for line in firstPhase:
        password = line[1]
        cipher = codeString(userInput, password)

        if cipher == '':
            continue

        res.add((cipher, password))

i = 0

for b in res:
    if len(sys.argv) == 2 and sys.argv[1] == "tofile":
        with open("thatPassword" + str(i) + ".txt","w") as thatPassword:
            thatPassword.write(b[1] + "\n")
        with open("decipher" + str(i) + ".txt","w") as dc:
            dc.write(b[0] + "\n")
        i += 1
    else:
        print(BLUE + "heslo: " + b[1] + END + "\n\n" + b[0])



