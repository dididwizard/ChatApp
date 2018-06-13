#Kode untuk server
import socket
import select
import sys
from threading import Thread
import binascii


inisocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

download_path = "/sdcard/"

ipaddress = "192.168.43.1"

port = 12345

list_of_clients = []

def clientthread(conn, addr):
	while True:
		try:
			pesan = conn.recv(2024)
			if pesan:
				if addr[0] == "192.168.43.1":
					if "[FILE]" in pesan.decode('utf-8'):
						fn = pesan.decode('utf-8').split("::")[0].replace("[FILE]", "").replace("\n", "")
						f = open(download_path+fn, "w")
						fc = binascii.unhexlify(pesan.decode('utf-8').split("::")[1].encode('utf-8')).decode('utf-8')
						f.write(fc)
						f.close()
						print("File " + fn + " telah diterima")
						broadcast("[Server] Syarief Telah Mengirim File ".encode('utf-8')+fn.encode('utf-8')+"\n".encode('utf-8'), conn)
						broadcast("[Server] Ketik : /save <filename> untuk menyimpan file".encode('utf-8'), conn)
					elif "/save " in pesan.decode('utf-8'):
						frn = pesan.decode('utf-8').replace("/save ", "").replace("\n", "")
						fr = open(download_path+frn, "r")
						conn.send("[FILE]".encode('utf-8')+frn.encode('utf-8')+"::".encode('utf-8')+binascii.hexlify(fr.read().encode('utf-8')))
						print("Syarief telah menerima File " + frn)
						broadcast("[Server] Syarief telah menerima File ".encode('utf-8') + frn.encode('utf-8'), conn)
					else:
						print ("<Syarief> " + pesan.decode("utf-8"))
						msg = "<Syarief> ".encode("utf-8") + pesan
						broadcast(msg, conn)
				elif addr[0] == "192.168.43.113":
					if "[FILE]" in pesan.decode('utf-8'):
						fn = pesan.decode('utf-8').split("::")[0].replace("[FILE]", "").replace("\n", "")
						f = open(download_path+fn, "w")
						fc = binascii.unhexlify(pesan.decode('utf-8').split("::")[1].encode('utf-8')).decode('utf-8')
						f.write(fc)
						f.close()
						print("File " + fn + " telah diterima")
						broadcast("[Server] Didid Telah Mengirim File ".encode('utf-8')+fn.encode('utf-8')+"\n".encode('utf-8'), conn)
						broadcast("[Server] Ketik : /save <filename> untuk menyimpan file".encode('utf-8'), conn)
					elif "/save " in pesan.decode('utf-8'):
						frn = pesan.decode('utf-8').replace("/save ", "").replace("\n", "")
						fr = open(download_path+frn, "r")
						conn.send("[FILE]".encode('utf-8')+frn.encode('utf-8')+"::".encode('utf-8')+binascii.hexlify(fr.read().encode('utf-8')))
						print("Didid telah menerima File " + frn)
						broadcast("[Server] Didid telah menerima File ".encode('utf-8') + frn.encode('utf-8'), conn)
					else:
						print ("<Didid> " + pesan.decode("utf-8"))
						msg = "<Didid> ".encode("utf-8") + pesan
						broadcast(msg, conn)
			else:
				remove(conn)
		except:
			continue
def broadcast(pesan, koneksi):
    for clients in list_of_clients:
        if clients!=koneksi:
            try:
                clients.send(pesan)
            except:
                clients.close()

                remove(clients)

def remove(koneksi):
    if koneksi in list_of_clients:
        list_of_clients.remove(koneksi)
        
def startServer():
	print("Server Running...\n")
	inisocket.bind((ipaddress,port))
	inisocket.listen(5)

	while True:
		conn, addr = inisocket.accept()
		list_of_clients.append(conn)
		if addr[0] == "192.168.43.1":
			print ("Syarif telah Terhubung ")
			conn.send("Welcome Syarief".encode("utf-8"))
			
		elif addr[0] == "192.168.43.113":
			print ("Didid telah Terhubung ")
			conn.send("Welcome Didid".encode("utf-8"))
			
		t = Thread(target=clientthread, args=(conn, addr))
		t.start()
	conn.close()
	inisocket.close

def showStatus():
	if serverstatus == "off":
		print("Server is not Running")
	else:
		print("Server is not Running")

def exitServer():
	sys.exit()

def readKey():
	option = input(">> ")
	if "1" in option:
		startServer()
	if "2" in option:
		showStatus()
		readKey()
	if "3" in option:
		exitServer()
	if "1" not in option and "2" not in option and "3" not in option:
		readKey()

print("Welcome to\n")
print("==========================\n")
print("Simple Chat Server v0.5 Alpha\n")
print("==========================\n\n")
print("Options :\n")
print("1. Start Server\n")
print("2. Server Status\n")
print("3. Exit\n")
readKey()
