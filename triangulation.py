#!/usr/bin/python3
import platform
Windows = platform.system() == 'Windows'

def cc_intersection(P0, P1, r0, r1):
	""" Circle-Circle Intersection
	P0, P1 are coordinates of circle centers
	r0, r1 are the radii of said circles
	Returns ([x1,y1],[x2,y2])
	"""

	from math import sqrt, fabs

	P2   = [None,None]
	P3_1 = [None,None]
	P3_2 = [None,None]

	d = sqrt((P0[0]-P1[0])**2+(P0[1]-P1[1])**2)

	a = (r0**2-r1**2+d**2)/(2*d)
	
	h = sqrt(fabs(r0**2-a**2))

	P2[0]   = P0[0]+a*(P1[0]-P0[0])/d
	P2[1]   = P0[1]+a*(P1[1]-P0[1])/d

	P3_1[0] = P2[0]+h*(P1[1]-P0[1])/d
	P3_1[1] = P2[1]-h*(P1[0]-P0[0])/d

	P3_2[0] = P2[0]-h*(P1[1]-P0[1])/d
	P3_2[1] = P2[1]+h*(P1[0]-P0[0])/d

	return P3_1, P3_2

def calc_center(p):
	""" Calculate Center
	p is a list of intersection points
	this function turns those points into lines according to y=ax+b
	raises Exception when the lines don't intersect
	returns [y,x]
	"""

	# lines are sets of two coordinates through which the line travels
	# eg. l1 = [[1,3],[4,6]]
	l1 = p[0]
	l2 = p[1]
	xdiff = (l1[0][0]-l1[1][0], l2[0][0]-l2[1][0])
	ydiff = (l1[0][1]-l1[1][1], l2[0][1]-l2[1][1])

	def det(a, b):
		return a[0]*b[1]-a[1]*b[0]

	div = det(xdiff, ydiff)
	if div == 0:
		raise Exception('Lines don\'t intersect')

	d = (det(*l1), det(*l2))
	x = det(d, xdiff)/div
	y = det(d, ydiff)/div

	return [int(round(21-y)), int(round(x))]

def location(P0, P1, P2, r0, r1, r2):
	""" Location
	P0, P1, P2 are lists containing coordinates of circle centers
	r0, r1, r2 are integers describing the radii of the circles
	calls cc_intersection to determine the intersection
	if three points within p0, p1 and p2 are equal return said point as [x,y]
	else calculate the center of those points
	"""

	p0 = cc_intersection(P0, P1, r0, r1)
	p1 = cc_intersection(P1, P2, r1, r2)
	p2 = cc_intersection(P2, P0, r2, r0)

	p = [p0, p1, p2]

	for i in range(3):
		for j in range(2):
			for k in range(2):
				p[i][j][k] = round(p[i][j][k])

	for i in range(2):
		for j in range(2):
			for k in range(2):
				if p[0][i] == p[1][j] == p[2][k]:
					return p[0][i]
				else:
					return calc_center(p)

def dBm_to_m(MHz, dBm):
	""" Decibel-meter to Meter
	MHz is an int describing the frequency of the wifi access point in MHz
	dBm is an int describing the signal strength of said access point in dBm
	returns the meters as int
	"""
	from math import log10

	global Windows

	if platform.system() == 'Windows':
		dBm = (dBm/2)-100

	# FSPL is the factor for the loss of signal strength innate to wifi
	FSPL = 27.55
	meters = round((10**((FSPL-(20*log10(MHz))-dBm)/20))*0.5, 2)

	if meters > 50:
		menu()

	return meters

def get_dBm(APName):
	""" Get Signal Strength
	APName is a string containing the name of the access point of which you want the signal strength
	This function runs a command on your system based on the detected Operating System to scan for the access point
	The result of the scan is written to a file and then read as a list to easily split the contents we need: signal
	strength and frequency returns the signal strength and frequency as integers
	"""

	import subprocess

	global Windows

	if platform.system() == 'Windows':
		netscan = subprocess.run('netsh wlan show networks mode = bssid', shell=True, stdout=subprocess.PIPE)
		f = open('netscan.txt', 'w')
		f.write(netscan.stdout.decode('utf-8'))
		f.close()

	else:
		subprocess.run(['sudo iwlist wlo1 scan | grep -i -B 5 {} > ./netscan.txt'.format(APName)], shell=True)

	f = open('netscan.txt')
	lines = f.readlines()
	f.close()

	frequency = 0
	signal = 0

	if platform.system() == 'Windows':
		data = []
		for l in range(len(lines)):
			lines[l] = lines[l].strip()
			#if 'V1F4' in l:
			#	data.append(l[l.index(l):l.index(l)+6])
			if 'Radio type' in lines[l]:
				freq = lines[l].split(':')
				freq = freq[1].strip()
				if freq == '802.11ac':
					frequency = 5230
				else:
					frequency = 2470

			if 'Signal' in lines[l]:
				sig = lines[l].split(':')
				sig = sig[1].strip()
				sig = sig[:-1]
				signal = int(sig)
	else:
		for l in range(len(lines)):
			lines[l] = lines[l].strip()
			if 'Frequency:' in lines[l]:
				freq = lines[l].split(':')
				freq = freq[1].split(' ')
				frequency = int(float(freq[0])*1000)

			if 'Signal' in lines[l]:
				sig = lines[l].split('=')
				sig = sig[-1].split(' ')
				signal = int(sig[0])

	return frequency, signal

def menu():
	""" Menu
	The same as Main() but Menu() because it used to be a menu in days past asking for names and coordinates of access points
	In this function you can set the names and coordinates of the access points
	P0, P1, P2 are the coordinates: [x,y]
	AP0, AP1, AP2 are the names as string
	"""

	print('Scanning...')

	from termcolor import colored

	P0 = [14,8]
	P1 = [2,8]
	P2 = [10,2]

	AP0 = 'v1f4ap1'
	AP1 = 'v1f4ap2'
	AP2 = 'v1f4ap3'

	class AccessPointError(Exception):
		""" An exception to raise when something is not quite right with the access points
		does nothing else"""

		pass

	def get_apNames():
		""" Calls get_apCoords for some inexplicable reason...
		this function might have done something at some point, but it no longer does
		I don't really have a clue :/"""

		nonlocal AP0, AP1, AP2

		return get_apCoords()

	def get_apCoords():
		""" Get your location
		uses nonlocal variables as seen below
		raises (and catches) AccessPointError when any of the access points have the same coordinates
		catches NameError when something was entered the wrong way, this dates back to when it was a menu
		calls get_dBm, dBm2m to get the users location
		returns (and prints) the location of the user as [y,x]
		"""

		nonlocal AP0, AP1, AP2, P0, P1, P2

		try:

			if P0 == P1 or P1 == P2 or P2 == P0:
				raise AccessPointError

			else:

				dbP0 = get_dBm(AP0)
				dbP1 = get_dBm(AP1)
				dbP2 = get_dBm(AP2)

				r0 = dBm_to_m(dbP0[0], dbP0[1])
				r1 = dBm_to_m(dbP1[0], dbP1[1])
				r2 = dBm_to_m(dbP2[0], dbP2[1])

				r0 = round(r0, 2)
				r1 = round(r1, 2)
				r2 = round(r2, 2)

				print('\n======[Location Data]=======')
				print('AP1: {:>4} MHz, {:>3} dBm, distance: {:1.2f}m'.format(dbP0[0], dbP0[1], r0*2))
				print('AP2: {:>4} MHz, {:>3} dBm, distance: {:1.2f}m'.format(dbP1[0], dbP1[1], r1*2))
				print('AP3: {:>4} MHz, {:>3} dBm, distance: {:1.2f}m'.format(dbP2[0], dbP2[1], r2*2))

				l = location(P0, P1, P2, r0, r1, r2)
				print('You are at: {}'.format(l))
				return l

		# except NameError as e:
		# 	print(e)
		# 	print(colored('Wrong format', 'red'))
		# 	get_apCoords()

		except AccessPointError:
			print(colored('Something is wrong with the Access Points coordinates, please re-enter', 'red'))
			get_apCoords()

	return get_apNames()