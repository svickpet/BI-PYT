import random, os, time

class eSeq:
	END = '\033[0m'
	GREENBG = '\033[42m'
	CURSOR_OFF = '\033[?25l'
	CURSOR_ON = '\033[?25h'
	CLEAR = '\033[2J'


print(eSeq.CLEAR + eSeq.CURSOR_OFF)			# clear terminal and hide cursor

cols, rows = os.get_terminal_size()			# size of terminal

# random coordinate - where point should start
x = random.randint(1, cols)
y = random.randint(1, rows)	

# random direction
i = random.randint(1,4)

# infinite movement
try:
	while True:
		#print('\033[{};{}H\033[42m \033[0m'.format(str(y), str(x)), end='', flush=True)	
		print(f'\033[{str(y)};{str(x)}H' + 
				'*' + eSeq.END, 
				end='', flush=True)				# python3.6 and above
	
		time.sleep(0.05)
		print('\b ')

		# change directions when point has collision with border	
		if y == rows:					
			i = 2 if i==1 else 4 
		if x == cols:
			i = 3 if i==1 else 4
		if y == 1:
			i = 3 if i==4 else 1
		if x == 1:
			i = 2 if i==4 else 1

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
	print(eSeq.CURSOR_ON)
finally:
	print('Molekula byla zastavena.')


