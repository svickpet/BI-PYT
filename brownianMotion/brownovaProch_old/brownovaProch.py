import random, os, time, sys

#pro lepsi prechody barev jsem je "precislovala"
barvy = {
	1: 42,
	2: 43,
	3: 41,
	4: 45,
	5: 44,
	6: 46
}

cols, rows = os.get_terminal_size()

#stred terminalu
c_stred = cols // 2
r_stred = rows // 2

#vychozi nastaveni, smazani terminalu, posunuti do stredu
print("\033[2J\033[?25l")
print("\033[{};{}H".format(r_stred, c_stred), end="", flush=True)
#print("\033[42m  \033[0m", end="", flush=True)

x, y = c_stred, r_stred

pole = {}
space = 2

while True:
	smer = random.randint(1,4)
	
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

	if (x,y) in pole:
		pole[(x,y)] += 1
	else:
		pole[(x,y)] = 1

	num = pole[x,y]//2+1	

	if len(sys.argv) == 1:
		print("\033[47m" + " "*space + "\b"*space + "\033[0m", end="", flush=True)

	elif len(sys.argv) and len(sys.argv[1]) == 1:
		symbol = sys.argv[1]
		print("\033[30;{}m".format(barvy.setdefault(num,47)) + "{}".format(symbol)*space + "\b"*space + "\033[0m", end="", flush=True)

	
	time.sleep(0.1)
	print("\033[{}m".format(barvy.setdefault(num,47)) + " "*space + "\b"*space + "\033[0m", end="", flush=True)

	if x-space<0 or y-space<0 or x+space>cols or y+space>rows:
		break;
	

print("\033[{};0H\033[?25h".format(rows), end="", flush=True)
		


