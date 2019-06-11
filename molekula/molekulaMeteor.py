import random, os, time

class eSeq:
	END = '\033[0m'
	CURSOR_OFF = '\033[?25l'
	CURSOR_ON = '\033[?25h'
	CLEAR = '\033[2J'
	GREENBG = '\033[42m'
	YELLOWBG = '\033[43m'
	BLUEBG = '\033[44m'
	REDBG = '\033[41m'
	PINKBG = '\033[45m'
	CYANBG = '\033[46m'
	WHITEBG = '\033[47m'
	GREEN  = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	RED = '\033[31m'
	PINK = '\033[35m'
	CYAN = '\033[36m'
	WHITE = '\033[37m'

def drawCollision(x, y):	
	bottom = (x,y+1)
	right = (x+1,y)
	top = (x,y-1)	
	left = (x-1,y)

	symbolTop = '|'
	symbolBottom = '|'
	symbolLeft = '-'
	symbolRight = '-'

	print(eSeq.WHITE)

	print(f'\033[{str(right[1])};{str(right[0])}H' + symbolRight, end='', flush=True)
	print(f'\033[{str(left[1])};{str(left[0])}H' + symbolLeft, end='', flush=True)
	print(f'\033[{str(bottom[1])};{str(bottom[0])}H' + symbolBottom , end='', flush=True)
	print(f'\033[{str(top[1])};{str(top[0])}H' + symbolTop, end='', flush=True)

	return bottom, right, top, left

def eraseCollision(c):
	if c == 0:
		return
	
	for i in c:
		print(f'\033[{str(i[1])};{str(i[0])}H' + ' ', end='', flush=True)

# ---------------------------------------------------------------------------------------------------

print(eSeq.CLEAR + eSeq.CURSOR_OFF)			# clear terminal and hide cursor

cols, rows = os.get_terminal_size()			# size of terminal

# some initialization
x2 = y2 = x3 = y3 = x4 = y4 = x5 = y5 = 0								
ret = colCount = howManyStepsCollision = 0

# intro message
try:
	for i in range(3):
		message = eSeq.RED + 'Error!' + eSeq.END + ' Kulový blesk se dostal do terminálu!'
		coordMessage = (cols-len(message))//2
		print(f'\033[{str(rows//2)};{str(coordMessage)}H' + message)
		time.sleep(0.8)
		print(f'\033[{str(rows//2)};{str(coordMessage)}H' + ' '*len(message))
		time.sleep(0.8)
except KeyboardInterrupt:
	print(eSeq.CURSOR_ON + eSeq.END + eSeq.CLEAR)
	quit()

# random coordinate - where molecule should start
x = random.randint(1, cols)
y = random.randint(1, rows)	

# random direction
i = random.randint(1,4)

sleepTime, steps = 0.02, 0

# design of molecule
symbol = 'o'
symbolTail = '*'
colorOfFirst = eSeq.WHITE
colorOfSecond = eSeq.YELLOW
colorOfThird = eSeq.RED

# infinite movement
try:
	while True:
		steps += 1
		howManyStepsCollision -= 1
		#print('\033[{};{}H\033[42m \033[0m'.format(str(y), str(x)), end='', flush=True)	
		print(f'\033[{str(y)};{str(x)}H' + colorOfFirst + symbol + eSeq.END, end='', flush=True)				# python3.6 and above
	
		time.sleep(sleepTime)	
		
		if steps > 1:
			print(f'\033[{str(y2)};{str(x2)}H' + colorOfSecond + symbolTail, end='', flush=True)
			time.sleep(sleepTime)
		if steps > 2:
			print(f'\033[{str(y3)};{str(x3)}H' + colorOfSecond + symbolTail, end='', flush=True)
			time.sleep(sleepTime)
		if steps > 3:
			print(f'\033[{str(y4)};{str(x4)}H' + colorOfThird + symbolTail, end='', flush=True)
			time.sleep(sleepTime)
		if steps > 4:
			print(f'\033[{str(y5)};{str(x5)}H' + colorOfThird + symbolTail + eSeq.END, end='', flush=True)
			time.sleep(sleepTime)
			print(f'\033[{str(y5)};{str(x5)}H ', end='', flush=True)	# delete last symbol

		# change directions when point has collision with border	
		if y == rows:						# bottom
			i = 2 if i==1 else 4
		if x == cols:						# right 
			i = 3 if i==1 else 4
		if y == 1:							# top
			i = 3 if i==4 else 1
		if x == 1:							# left
			i = 2 if i==4 else 1

		# managing drawing of collisions
		if howManyStepsCollision == 0:
			eraseCollision(ret)	

		if y == rows or y == 1 or x == cols or x == 1:
			ret = drawCollision(x,y)
			colCount += 1
			howManyStepsCollision = 2

		# shift values
		x5,y5,x4,y4,x3,y3,x2,y2 = x4,y4,x3,y3,x2,y2,x,y

		# change coordinates in the context of direction
		if i == 1:		# right down
			y = y+1
			x = x+1
		elif i == 2: 	# right up
			y = y-1 
			x = x+1
		elif i == 3: 	# left down
			y = y+1
			x = x-1
		elif i == 4: 	# left up
			y = y-1
			x = x-1

except KeyboardInterrupt:
	print(eSeq.CURSOR_ON + eSeq.END + eSeq.CLEAR)
finally:
	print('Kulový blesk byl zastaven a terminál nedošel k úhoně. Haleluja!\nCelkem ' + str(steps) 
			+ 'x se posunul a ' + str(colCount) + 'x narazil do okrajů terminálu.')


