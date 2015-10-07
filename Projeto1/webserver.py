#!/usr/bin/python3

"""
    @author: Arieh Fabbro, Camilo Moreira, Cristian Pendenza
    @lastmod: 06/10/2015
"""

import cgi
import string
import html.parser
from backend import NR_PCS, send_requests

"""
	Procedimento que inicializa os cabecalhos da pagina Web
	Alguns cabecalhos como data e servidor sendo usado sao 
	atualizados pelo próprio servidor Web
"""
def init_HTML_headers():
	print ("Content-type: text/html\n\n")

"""
	Funcao que retorna a <head> do HTML.
	O titulo da pagina muda para diferentes ocasioes.
	@param cond identificador da mensagem desejada
"""

def init_HTML_head_tag(cond):
	print ("<head>")
	if(cond == 0):
		print ("<title>Trabalho 1 de Redes</title>")
	elif(cond == 1):
		print ("<title>Resultado de todos os Daemons</title>")
	else:
		print ("<title>Pagina invalida</title>")
	print ("</head>")

"""
	Funcao que retorna PC + i em forma de String.
	Foi-se decidido este padrao para nome de computadores.
	@param i numero do PC
"""

def getName(i):
	return "PC" + str(i);

"""
	Funcao que retorna uma parte do form onde PC_NAME é 
	substituido pelo nome do PC.
	@param i numero do PC 
"""

def getSubForm(i):
	html = """PC_NAME
			<br/>
			<input type="hidden" name="PC_NAME_defined" value="PC_NAME_defined">
			<br/>ps 
			<input type="checkbox" name="PC_NAME_cmd1">
			<input type="text" name="PC_NAME_cmd1_args" placeholder="args">
			<br/>df 
			<input type="checkbox" name="PC_NAME_cmd2">
			<input type="text" name="PC_NAME_cmd2_args" placeholder="args">
			<br/>uptime 
			<input type="checkbox" name="PC_NAME_cmd3">
			<input type="text" name="PC_NAME_cmd3_args" placeholder="args">
			<br/>finger 
			<input type="checkbox" name="PC_NAME_cmd4">
			<input type="text" name="PC_NAME_cmd4_args" placeholder="args">
			<br/>
			<br/>"""
	html = html.replace('PC_NAME',getName(i))
	return html

"""
	Funcao que retorna o comando que deve ser executado em forma de texto.
	@param i numero do comando
"""

def getCommand(i):
	if (i == 1):
		return "ps"
	elif (i == 2):
		return "df"
	elif (i == 3):
		return "finger"
	elif (i == 4):
		return "uptime"

"""
	Funcao que cria uma mensagem que sera enviada que sera enviada ao
	backend. Ela lê as informacoes presentes no form, interpreta e
	cria uma string que sera analisada pelo backend.
	A mensagem separa os PCs pelo caractere \n e separa
	diferentes comandos por \t. 
	Os argumentos dos comandos sao separados por espacos simples. 
"""

def create_backend_message():
	global form
	message = ""

	for i in range(1,NR_PCS+1):
		message = message + getName(i) + "\t";
		for j in range(1,5):
			#cria o "name" do item do form
			key = getName(i) + "_cmd" + str(j)
			#procura por este "name" e adiciona o comando se encontrado
			if(key in form):
				message = message + getCommand(j) 
				#cria o "name_args" do item do form
				key = getName(i) + "_cmd" + str(j) + "_args"
				#procura por este "name_args" e adiciona argumentos se encontrado
				#note que argumentos nao sao adicionados se o comando não é encontrado
				if(key in form):
					message = message + " " + form.getvalue(key) + "\t"
				else:
					message = message + "\t"
		#remove o ultimo \t inserido depois do loop
		message = message[0:len(message)-1]
		#adiciona \n entre PCs na mensagem
		if(i != NR_PCS):
			message = message + "\n"
	return message

"""
	Funcao que recebe uma lista de strings e exibe em varias strings de acordo
	com as informacoes do form.
	Analogo a create_backend_message(), mas ao invés de criar, ele interpreta 
	e exibe os Resultados
	@param message lista de string com varias RESPONSES
"""

def parse_backend_message(message):
	global form
	print("<pre>")
	m = 0
	for i in range(1,NR_PCS+1):
		print ("Resultados do " + getName(i) + "<br/>")
		for j in range(1,5):
			key = getName(i) + "_cmd" + str(j)
			if(key in form):
				print (message[m][11:] + "<br/>")
				m=m+1
	print("</pre>")

"""
	Fluxo inicial do programa.
	Inicializa o html e cria o form se não está criado ou nada está selecinado
	quando é enviado.
	Processa o resultado quando opções do form estão selecionadas.
"""

#Insere os cabecalhos na pagina
init_HTML_headers()

#Procura pelo form na pagina
form = cgi.FieldStorage()
form_is_defined = form.keys()
#Se o form nao e encontrado ou nao tem opcoes selecionadas, cria o form em html.
if not form_is_defined or len(form_is_defined) == 3:
	#Seleciona <head> apropriada
	init_HTML_head_tag(0)
	print ("""<p>Selecione os comandos que deseja e digite seus respectivos argumentos para cada computador</p>
			<form name="commands" action="webserver.py" method="post">""")
	#cria uma parte do form para cada computador
	for i in range(1,NR_PCS+1):
		print (getSubForm(i))
	#adiciona os botoes do form 
	print ("""<button type="reset" value="Reset">Limpar tudo</button>
			<button type="submit" value="Submit">Enviar</button>
			</form>""")
else:
	#Seleciona <head> apropriada
	init_HTML_head_tag(1)
	#Cria mensagem para o backend, envia e processa lista de strings que chegou
	message = create_backend_message()
	message = send_requests(message)
	parse_backend_message(message)
	#adiciona os botoes para resetar o form
	print ("""<br/>
			<form name="commands" action="webserver.py" method="post">
			<button type="submit" value="Submit">Voltar ao Inicio</button>
			</form>""")