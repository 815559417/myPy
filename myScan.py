#coding=UTF-8
import optparse
import socket
def connScan(tgtHost,tgtPort):
	try:
		connSkt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		connSkt.connect((tgtHost,tgtPort))
		print('[+]%d/tcp open' % tgtPort)
		connSkt.close()
	except:
		print('[-]%d/tcp closed' % tgtPort)

def portScan(tgtHost,tgtPorts):
	try:
		tgtIP = socket.gethostbyname(tgtHost)
	except:
		print("[-] Cannot resolve '%s':Unknown host" % tgtHost)
		return
	try:
		tgtName = socket.gethostbyaddr(tgtIP)
		print('\n[+] Scan Results for:' + tgtName[0])
	except:
		print('\n[+] Scan Results for:' + tgtIP)
	socket.setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		print('Scanning port' + str(tgtPort))
		connScan(tgtHost,int(tgtPort))