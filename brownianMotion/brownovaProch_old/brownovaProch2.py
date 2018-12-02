import random, os, time, sys

class eSeq:
	END = '\033[0m'
	CURSOR_OFF = '\033[?25l'
	CURSOR_ON = '\033[?25h'
	CLEAR = '\033[2J'

#pro lepsi prechody barev jsem je "precislovala"
barvy = {
	1: 42,
	2: 43,
	3: 41,
	4: 45,
	5: 44,
	6: 46
}

space = 2
cols, rows = os.get_terminal_size()

def readSouradnice():
	#print("ctu souradnice")
	with open('./zaznam.txt', 'r', encoding='utf-8') as soubor:
		zaznam = soubor.read()
		parts = zaznam.split(',')
		#print(parts)

		i = 0
		print("\033[2J\033[?25l")
		while i+1 < len(parts):
			item = parts[i].split('=')
			#print(item)
			hodnota = int(item[1])
			souradnice = item[0]
	
			#print(barvy.setdefault(hodnota,47))			

			print("\033[{}H\033[{}m".format(souradnice,barvy.setdefault(hodnota,47)) + " "*space + "\033[0m", end="", flush=True)
			i += 1
		print("\033[{};0H\033[?25h".format(rows), end="", flush=True)

if len(sys.argv) > 2:
	print('Mnoho argumentu.\nZavolejte program s parametrem "help" pro vice informaci.')
	sys.exit()

if len(sys.argv) == 2:
	if sys.argv[1] == "-help":
		print('\033[32m' + 'Po zavolani programu bez parametru se spusti vychozi verze - program nasimuluje Náhodnou procházku s různě dlouhým krokem, obarvi navstivena mista podle poctu navstiveni, vse zaznamena do souboru a skonci při dotknuti se okraje konzole.\n\n' +
		'Program lze spustit i s parametrem "read" - program precte posledni ulozeny zaznam prochazky a zobrazi ho na konzoli.\n\n' +
		'Dalsi moznost je spustit program s jednim parametrem ve tvaru jednoho symbolu - "chodici" objekt bude oznacen timto znakem, jinak je oznacen bilym ctvereckem. (Doporucuji symbol "0" ;))' + '\033[0m')
		sys.exit()
	elif len(sys.argv[1]) == 1:
		symbol = sys.argv[1]
	elif sys.argv[1] == "-read":
		readSouradnice()
		sys.exit()



#stred terminalu
c_stred = cols // 2
r_stred = rows // 2

#vychozi nastaveni, smazani terminalu, posunuti do stredu
print("\033[2J\033[?25l")
print("\033[{};{}H".format(r_stred, c_stred), end="", flush=True)
#print("\033[42m  \033[0m", end="", flush=True)

x, y = c_stred, r_stred

pole = {}

try:

	#otevreni souboru
	with open('./zaznam.txt', 'w', encoding='utf-8') as soubor:

		while True:
			if (x,y) in pole:
				pole[(x,y)] += 1
			else:
				pole[(x,y)] = 1

			num = pole[x,y]//2+1	

			if len(sys.argv) == 1:
				print("\033[47m" + " "*space + "\b"*space + "\033[0m", end="", flush=True)

			elif len(sys.argv) == 2 and len(sys.argv[1]) == 1:
				symbol = sys.argv[1]
				print("\033[30;{}m".format(barvy.setdefault(num,47)) + "{}".format(symbol)*space + "\b"*space + "\033[0m", end="", flush=True)
	
			time.sleep(0.1)
			print("\033[{}m".format(barvy.setdefault(num,47)) + " "*space + "\b"*space + "\033[0m", end="", flush=True)

			if x-space<1 or y==1 or x+space>=cols or y==rows:
				break;

			smer = random.randint(1,4)
	
			#zapis souradnic
			soubor.write("{};{}={},".format(y,x,pole[(x,y)]))


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

	

		#if x-space<0 or y<0 or x>cols-space or y>rows:
		#	break;
	

	print("\033[{};0H\033[?25h".format(rows), end="", flush=True)
except KeyboardInterrupt:
	print(eSeq.CURSOR_ON)
finally:
	print("Obrazek byl ulozen do souboru zaznam.txt. Pro jeho otevreni spustte program s parametrem '-read'.")
		


