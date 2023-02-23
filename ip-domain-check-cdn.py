#!/usr/bin/python3
import socket, os, sys
import glob
import ipaddress

# default directory for checking ip behind cdn
dir = '/mnt/c/Users/H/Desktop/Hamnal/cidrs'


# read cidrs in default path and check for ip in cidr
def readfiles(inp):
	with open(f"{dir}/all.txt") as inpfile:
		for line in inpfile:
			line = line.replace("\n", "")
			tf = ipaddress.ip_address(inp) in ipaddress.ip_network(line)
			if tf:
				return inp
			else:
				return False


# convert domain to ip
def checkdomain(domain):
	try:
		ip = socket.gethostbyname(domain)
		a = readfiles(ip)

		# a = os.system(f'grep -rnw {dir} -e {ip}') ##################################
		if a != 0:
			open('cdn-domain-no.txt', 'a+').write(f"{domain}, {ip}"+'\n')
		else:
			open('cdn-domain-yes.txt', 'a+').write(f"{domain}, {ip}"+'\n')

	except:
		print(f'Error: {domain}')


# check ip in list of cdns ips
def checkip(ip):
	a = readfiles(ip)
	# a = os.system(f'grep -rnw {dir} -e {ip}') ##################################
	if a != 0:
		open('cdn-ip-no.txt', 'a+').write(ip+'\n')
	else:
		open('cdn-ip-yes.txt', 'a+').write(ip+'\n')


# start
try:
	os.system("clear -x")
	# read line by line input file
	with open(sys.argv[1]) as inpfile:
		print(f"[+] input file: {sys.argv[1]}")
		for line in inpfile:
			isip = 0
			line = line.replace('\n', '')
			# check for line is ip or domain
			try:
				if socket.inet_aton(line):
					isip = 1
			except: 
				pass
			# check input or domain for existing ip in defaul list
			if isip == 0:
				checkdomain(line)
			else:
				checkip(line)

	print("Done! Result saved!")


except IndexError:
	exit('Target website without http or https\nUse: python {} web.txt\n'.format(sys.argv[0]))

except:
	exit('File does not exist')

