import socket
import select
import sys
import binascii

inisocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
download_path = "/sdcard/AppProject/"
"""if len(sys.argv) != 3:
	print ("Masukan Alamat dan port yang ingin dihubungkan")
	exit()
address = str(sys.argv[1])
port = int(sys.argv[2])"""
address = "192.168.43.1"
port = 12345
inisocket.connect((address,port))

while True:
	sockets_list = [sys.stdin, inisocket]
	
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
	
	for socks in read_sockets:
		if socks == inisocket:
			pesan = socks.recv(2089)
			if "[FILE]" in pesan.decode('utf-8'):
				fn = pesan.decode('utf-8').split("::")[0].replace("[FILE]", "").replace("\n", "")
				f = open(download_path+fn, "w")
				fc = binascii.unhexlify(pesan.decode('utf-8').split("::")[1].encode('utf-8')).decode('utf-8')
				f.write(fc)
				f.close()
				print("File " + fn + " telah disimpan")
			else:
				print (pesan.decode("utf-8"))
		else:
			pesan = sys.stdin.readline()
			if "/send" in pesan:
				fn = pesan.replace("/send ", "")
				fn2 = fn.split("/")[-1]
				f = open(fn.replace("\n", ""), "r")
				inisocket.send("[FILE]".encode('utf-8') + fn2.encode('utf-8') + "::".encode('utf-8') + binascii.hexlify(f.read().encode('utf-8')))
				sys.stdout.write("File Terkirim\n")
				sys.stdout.flush()
			else:
				inisocket.send(pesan.encode("utf-8"))
				sys.stdout.write("Anda >")
				sys.stdout.write(pesan)
				sys.stdout.flush()
	
inisocket.close()
