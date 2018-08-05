from socket import *
import sys
import math

def salva_dados(msg):
	tipo_msg,id_msg,tipo_comb,preco_comb,latitude,longitude = msg.split("_")
	if msg[4] == '0':
		arq = open('diesel.txt', 'a+')
	elif msg[4] == '1':
		arq = open('alcool.txt', 'a+')
	elif msg[4] == '2':
		arq = open('gasolina.txt', 'a+')
	else:
		print ("combustivel informado nao existe")
		return
	arq.write(preco_comb+'_'+latitude+'_'+longitude+'\n')
	arq.close()
	return id_msg

def is_posto_dentro_do_raio(linha, raio, latitude, longitude):
	xa=float(latitude)
	ya=float(longitude)
	xb=float(linha[1])
	yb=float(linha[2])
	resultado = math.sqrt((xb-xa)**2+(yb-ya)**2)
	print ("distancia para ponto "+str(linha)+" e "+str(resultado))
	if resultado<=float(raio):
		return True
	else:
		return False

def pesquisa_dados(msg):
	tipo_msg,id_msg,tipo_comb,raio_busca,latitude,longitude = msg.split("_")
	try:
		if msg[4] == '0':
			arq = open('diesel.txt', 'r')
		elif msg[4] == '1':
			arq = open('alcool.txt', 'r')
		elif msg[4] == '2':
			arq = open('gasolina.txt', 'r')
		else:
			print ("combustivel informado nao existe")
			return
	except FileNotFoundError:
		return id_msg+"_N"
	menor_preco = -1
	posto_menor_preco = "N"
	texto = arq.readlines()
	for linha in texto:
		linha = linha.strip('\n')
		linha_aux = linha.split("_")
		if is_posto_dentro_do_raio(linha_aux, raio_busca, latitude, longitude):
			if int(linha_aux[0])<menor_preco or menor_preco==-1:
				menor_preco=int(linha_aux[0])
				posto_menor_preco = linha
		print ("menor preco: "+str(menor_preco))
	arq.close()
	return id_msg+"_"+posto_menor_preco

def interpreta_msg(msg):
	if 'D' == msg[0]:
		return salva_dados(msg)
	elif 'P' == msg[0]:
		return pesquisa_dados(msg)

if __name__ == "__main__":
	server_port = int(sys.argv[1])
	server_socket = socket(AF_INET6, SOCK_DGRAM)
	server_socket.bind(('::', server_port))
	print ("Servidor pronto para receber dados...\n")
	while 1:
		msg, client_addr = server_socket.recvfrom(2048)
		msg = msg.decode()
		print ("[" + str(client_addr) + "]: " + str(msg))
		new_msg = interpreta_msg(msg)
		print ("")
		server_socket.sendto(new_msg.encode(), client_addr)
