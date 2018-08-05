from socket import *
import sys
import ipaddress

def monta_mensagem_pesquisa():
	while 1:
		raio_busca = float(input("Digite o raio de busca: "))
		if raio_busca>0:
			raio_busca = str(raio_busca)
			break
		else:
			print ("O raio deve ser positivo...")
	latitude = float(input("Digite a sua latitude: "))
	longitude = float(input("Digite a sua longitude: "))
	latitude = str(latitude)
	longitude = str(longitude)
	return raio_busca+'_'+latitude+'_'+longitude

def monta_mensagem_insercao():
	while 1:
		preco_comb = int(input("Digite o preco do combustivel (sem virgula. ex: 3999 para 3,999): "))
		if isinstance(preco_comb, int):
			preco_comb = str(preco_comb)
			break
		else:
			print ("Valor passado incorretamente...")
	latitude = float(input("Digite a latitude do posto de combustivel: "))
	longitude = float(input("Digite a longitude do posto de combustivel: "))
	latitude = str(latitude)
	longitude = str(longitude)
	return preco_comb+'_'+latitude+'_'+longitude

def monta_mensagem_de_envio(id_msg):
	while 1:
		print ("[D]Inserir preco, [P]Pesquisar menor preco, [S]Sair")
		tipo_msg = input("Digite seu comando: ").upper()
		if tipo_msg == 'P' or tipo_msg == 'D':
			while 1:
				print ("[0]Diesel, [1]Alcool, [2]Gasolina")
				tipo_comb = input("Digite o tipo do combustivel: ")
				if int(tipo_comb) in {0, 1, 2}:
					tipo_comb = str(tipo_comb)
					break
				else:
					print ("Tipo inexistente...")
			if tipo_msg == 'P':
				return tipo_msg+'_'+str(id_msg)+'_'+tipo_comb+'_'+monta_mensagem_pesquisa()
			else:
				return tipo_msg+'_'+str(id_msg)+'_'+tipo_comb+'_'+monta_mensagem_insercao()
		elif tipo_msg == 'S':
			return tipo_msg
		else:
			print ("Valor invalido...")

def retorna_ipv6(server_name):
	resposta = gethostbyaddr(server_name)
	resposta2 = str(resposta[2])
	resposta2 = resposta2.strip('[')
	resposta2 = resposta2.strip(']')
	resposta2 = resposta2.strip("'")
	try:
		ipaddress.IPv6Address(resposta2)
		return resposta2
	except Exception as e:
		return '::ffff:'+resposta2

def interpreta_resposta(msg, rcv_msg, id_msg):
	if rcv_msg.split("_")[0] == str(id_msg):
		print ("resposta recebida: "+rcv_msg)
		if 'D' == msg[0]:
			print ("["+str(server_addr)+"]: dados inseridos com sucesso\n")
		elif 'P' == msg[0]:
			if 'N' == rcv_msg[2]:
				print ("["+str(server_addr)+"]: nenhum resultado encontrado...\n")
			else:
				resp_id, resp_preco, resp_latitude, resp_longitude = rcv_msg.split("_")
				resp_preco = float(resp_preco)/1000
				print ("["+str(server_addr)+"]: o menor preco encontrado e "+str(resp_preco)+" na localizacao ("+resp_latitude+","+resp_longitude+")\n")

if __name__ == "__main__":
	server_name = sys.argv[1]
	server_port = int(sys.argv[2])
	server_name = retorna_ipv6(server_name)
	client_socket = socket(AF_INET6, SOCK_DGRAM)
	id_msg=0
	print ("")
	while 1:
		id_msg+=1
		msg = monta_mensagem_de_envio(id_msg)
		if msg == 'S':
			break
		try:
			client_socket.sendto(msg.encode(), (server_name, server_port))
			client_socket.settimeout(5.0)
			rcv_msg, server_addr = client_socket.recvfrom(2048)
			client_socket.settimeout(None)
			rcv_msg = rcv_msg.decode()
			interpreta_resposta(msg, rcv_msg, id_msg)
		except Exception as e:
			print ("resposta nao recebida, tentando novamente...")
			try:
				client_socket.sendto(msg.encode(), (server_name, server_port))
				client_socket.settimeout(5.0)
				rcv_msg, server_addr = client_socket.recvfrom(2048)
				client_socket.settimeout(None)
				rcv_msg = rcv_msg.decode()
				interpreta_resposta(msg, rcv_msg, id_msg)
			except Exception as e:
				print ("resposta nao recebida na segunda tentativa, tente novamente...\n")
	client_socket.close()
