import random, os, time, sys

class eSeq:
	END = '\033[0m'
	CURSOR_OFF = '\033[?25l'
	CURSOR_ON = '\033[?25h'
	CLEAR = '\033[2J'
	LEFT_TOP = '\033[;f'

# "precislovani" barev, vyuziti pozdeji pri voleni barvy podle poctu navstiveni
barvy = {
	0: 42,
	1: 43,
	2: 41,
	3: 45,
	4: 44,
	5: 46
}

t = 0.05
space = 2
cols, rows = os.get_terminal_size()

# -----------------------------------

def printHelp():
	print('\033[32m' + 'Po zavolani programu bez parametru se spusti vychozi verze - program nasimuluje Náhodnou procházku s různě dlouhým krokem, obarvi navstivena mista podle poctu navstiveni, vse zaznamena do souboru a skonci při dotknuti se okraje konzole.\n\n' +
		'Program lze spustit i s parametrem "-read" - program precte posledni ulozeny zaznam prochazky a zobrazi ho na konzoli.\n\n' +
		'Dalsi moznost je spustit program s jednim parametrem ve tvaru jednoho symbolu -> "chodici" objekt bude oznacen timto znakem, jinak je oznacen bilym ctvereckem. (Doporucuji symbol "0" ;))' + '\033[0m')

# -----------------------------------

def readSouradnice():
	#print("ctu souradnice")
	print(eSeq.CLEAR)
	with open('./zaznam.txt', 'r', encoding='utf-8') as soubor:
		zaznam = soubor.read()
		parts = zaznam.split(',')
		
		i = 0
		#print("\033[2J\033[?25l")
		while i+1 < len(parts):
			item = parts[i].split('=')
			hodnota = int(item[1])
			souradnice = item[0]
	
			#print(barvy.setdefault(hodnota,47))			

			print("\033[{}H\033[{}m".format(souradnice,barvy.setdefault(hodnota,47)) 
					+ " "*space + "\033[0m", 
					end="", flush=True)
			i += 1
		print(f"\033[{rows};0H\033[?25h", end="", flush=True)

# -----------------------------------

def brown(symbol=' '):

	#stred terminalu
	c_stred = cols // 2
	r_stred = rows // 2

	#vychozi nastaveni, smazani terminalu, posunuti do stredu...
	print(eSeq.CLEAR + eSeq.CURSOR_OFF)
	print(f"\033[{r_stred};{c_stred}H", end="", flush=True)

	x, y = c_stred, r_stred
	pole = {}
	try:
		#otevreni souboru
		with open('./zaznam.txt', 'w', encoding='utf-8') as soubor:
			while True:
				if (x,y) in pole:				# pokud jsme bod jiz navstivili
					pole[(x,y)] += 1
				else:
					pole[(x,y)] = 1

				num = pole[x,y]//2	

				# "chodici" bod - bily ctyruhelnik s pripadnym znakem 
				print("\033[31;47m" + "{}".format(symbol)*space + "\b"*space + "\033[0m", end="", flush=True)

				time.sleep(t)
				print("\033[{}m".format(barvy.setdefault(num,47)) + ' '*space + "\b"*space + "\033[0m", end="", flush=True)

				if x-space<1 or y==1 or x+space>=cols or y==rows:
					break;

				smer = random.randint(1,4)

				#zapis souradnic
				#soubor.write("{};{}={},".format(y,x,pole[(x,y)]))
				soubor.write("{};{}={},".format(y,x,num))

				if smer == 1:	#nahoru
					print("\033[1A", end="", flush=True)
					y -= 1
				elif smer == 2:	#dolu
					print("\033[1B", end="", flush=True)
					y += 1
				elif smer == 3:	#doprava
					print("\033[{}C".format(space), end="", flush=True)
					x += space
				elif smer == 4:	#doleva
					print("\033[{}D".format(space), end="", flush=True)	
					x -= space

			print("\033[{};0H\033[?25h".format(rows), end="", flush=True)
	except KeyboardInterrupt:
		print(eSeq.CURSOR_ON + eSeq.CLEAR + eSeq.LEFT_TOP)
	finally:
		print("Obrazek byl ulozen do souboru zaznam.txt.\n"
				+"Pro jeho otevreni spustte program s parametrem '-read'.")

# -----------------------------------
# MAIN

if len(sys.argv) > 2:
	print('Mnoho argumentu.\nZavolejte program s parametrem "-help" pro vice informaci.')	

elif len(sys.argv) == 2:
	if sys.argv[1] == "-help":
		printHelp()

	elif sys.argv[1] == "-read":
		readSouradnice()

	elif len(sys.argv[1]) == 1:	# pokud je parametrem jediny znak
		symbol = sys.argv[1]				# nastav symbol na zvoleny znak
		brown(symbol)

	else:
		print('Nespravny argument.\nZavolejte program s parametrem "-help" pro vice informaci.')

else:
	brown()	


