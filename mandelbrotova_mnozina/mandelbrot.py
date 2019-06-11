#python3

import sys
import colorsys

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def mandelbrot(real, imag, maxIter):
	#c = z
	re = real
	im = imag
	for n in range(maxIter):	
		#if abs(z) > 2:
		#if z.real * z.real + z.imag * z.imag > 4:
		re2 = re*re
		im2 = im*im
		if re2+im2> 4:
			return n
		#z = z*z + c
		im = 2*re*im + imag
		re = re2-im2 + real

	return maxIter
	
# http://www.cuug.ab.ca/dewara/mandelbrot/images.html
# second coordinate needs be opposite (else mirrored)
goodValues = [		(0.0, 0.0, 2.0),												# 0
						(-0.7463, -0.1102, 0.005),									# 1
						(-0.925, -0.266, 0.032),									# 2
						(-0.7453, -0.1127, 6.5E-4),								# 3
						(-0.722, -0.246, 0.019),									# 4
						(-0.76, -0.09, 0.03),										# 5
						(-0.748, -0.1, 0.0014),										# 6
						(-0.74529, -0.113075, 1.5E-4),							# 7
						(-0.745428, -0.113009, 3.0E-5),							# 8
						(-1.25066, -0.02012, 1.7E-4),								# 9
						(-0.235125, -0.827215, 4.0E-5),							# 10	
						(0.432539867562512, -0.226118675951818, 1.82E-7),	# 11
						(-0.16070135, -1.0375665, 1.0E-5),						# 12
						(-0.81153120295763, -0.20142958206181, 3.0E-4),		# 13
						(0.452721018749286, -0.39649427698014, 1.1E-8),		# 14
						(0.3369844464869, -0.048778219666, 1.8E-9),			# 15
						(-0.0452407411, -0.986816213, 1.75E-7),				# 16
						(-0.0452407411, -0.9868162204352258, 4.4E-9),		# 17
						(-0.0452407411, -0.9868162204352258, 2.7E-10),		# 18
						(0.45272105023, -0.396494224267, 2.7E-9),				# 19
						(-1.15412664822215, -0.30877492767139, 3.1E-9),		# 20
						(0.432539867562512, -0.226118675951765, 3.2E-6)]	# 21
if len(sys.argv) == 1:
	index = 0 
else:
	if int(sys.argv[1]) > len(goodValues):
		print("There is no coordinates with this index. Try lower number.")
		exit()
	index = int(sys.argv[1])

with open("m" + str(index) + ".ppm", "bw") as f:
	size = 800
	
	#f.write(b'P6\n' + size + b' ' + size + b'\n255\n')
	f.write(b'P6\n800 800\n255\n')
	img = bytearray()
	
	maxOfTries = 360

	coordX,coordY,offset = goodValues[index]
	
	
	#coordX = -(coordMin - coordMax)

	fromX,toX = coordX-offset, coordX+offset
	fromY,toY = coordY-offset, coordY+offset

	#for i in range(size):
	#	n = (offset*2/size) * i
	#	arrX.append(n+coordX-offset)
	#	arrY.append(n+coordY-offset)

	arrX = [fromX + x*(toX-fromX)/size for x in range(size)]
	arrY = [fromY + x*(toY-fromY)/size for x in range(size)]
	
	i = 0

	for x in arrY:
		for y in arrX:
			ret = mandelbrot(y,x,maxOfTries)			
			
			if (ret == maxOfTries):
				img.append(0)
				img.append(0)
				img.append(0)
			else:
				#colour = ret % 255
				#colour = 255//(ret+1)
				#colour = (-255//(ret+1)) % 255
				#colour = (ret<<1) % 255
				#img.append(colour)
				#img.append(colour)
				#img.append(0)
			
				h = (ret/maxOfTries)	#hue
				s = 1				#saturation
				v = (h*3.0)		#value
				if v > 1:
					v = 1
							
				#r,g,b = colorsys.hsv_to_rgb(h,s,v)
				r,g,b = hsv2rgb(h,s,v)
				if i > 1:
					print(str(h) + " " + str(s) + " " + str(v))
					print(str(r) + " " + str(g) + " " + str(b))
					i += 1

				img.append(int(r))
				img.append(int(g))
				img.append(int(b))


	f.write(img)



	
