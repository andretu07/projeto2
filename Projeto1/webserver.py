#!/usr/bin/python3

import cgi
import string
import html.parser
from backend import NR_PCS, backend_func

def init_HTML_headers():
	print ("Content-type: text/html\n\n")

def init_HTML_head_tag(cond):
	print ("<head>")
	if(cond == 0):
		print ("<title>Trabalho 1 de Redes</title>")
	elif(cond == 1):
		print ("<title>Resultado de todos os Daemons</title>")
	else:
		print ("<title>Página inválida</title>")
	print ("</head>")

def getName(i):
	return "PC" + str(i);

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

def getCommand(i):
	if (i == 1):
		return "ps"
	elif (i == 2):
		return "df"
	elif (i == 3):
		return "finger"
	elif (i == 4):
		return "uptime"

def create_backend_message():
	global form
	message = ""

	for i in range(1,NR_PCS+1):
		message = message + getName(i) + "\t";
		for j in range(1,5):
			key = getName(i) + "_cmd" + str(j)
			if(key in form):
				message = message + getCommand(j) 
				key = getName(i) + "_cmd" + str(j) + "_args"
				if(key in form):
					message = message + " " + form.getvalue(key) + "\t"
				else:
					message = message + "\t"
		message = message[0:len(message)-1]
		if(i != NR_PCS):
			message = message + "\n"
	return message

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



init_HTML_headers()

#First start
form = cgi.FieldStorage()
form_is_defined = form.keys()
if not form_is_defined or len(form_is_defined) == 3:
	init_HTML_head_tag(0)
	print ("""<p>Selecione os comandos que deseja e digite seus respectivos argumentos para cada computador</p>
			<form name="commands" action="webserver.py" method="post">""")
	for i in range(1,NR_PCS+1):
		print (getSubForm(i))
	print ("""<button type="reset" value="Reset">Limpar tudo</button>
			<button type="submit" value="Submit">Enviar</button>
			</form>""")
else:
	init_HTML_head_tag(1)
	message = create_backend_message()
	message = backend_func(message)
	parse_backend_message(message)
	print ("""<br/>
			<form name="commands" action="webserver.py" method="post">
			<button type="submit" value="Submit">Voltar ao Inicio</button>
			</form>""")