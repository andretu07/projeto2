#!C:\Users\Cristian\AppData\Local\Programs\Python\Python35\python.exe

import cgi
import string
import html.parser

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

print ("Content-type: text/html\n\n")

#PERGUNTAR AO BACKEND QUANTOS COMPUTADORES ESTAO LIGADOS
nr_PCs = 3

#First start
form = cgi.FieldStorage()
form_is_defined = form.keys()
if not form_is_defined or len(form_is_defined) == 3:
	print ("<head><title>Trabalho 1 de Redes</title></head>")
	print ("""<p>Selecione os comandos que deseja e digite seus respectivos argumentos para cada computador</p>
			<form name="commands" action="webserver.py" method="post">""")
	for i in range(0,nr_PCs):
		print (getSubForm(i+1))
	print ("""<button type="reset" value="Reset">Limpar tudo</button>
			<button type="submit" value="Submit">Enviar</button>
			</form>""")
else:
	#ENVIAR COMANDOS AS MAQUINAS LIGADAS
	print ("""<br/>
			<form name="commands" action="webserver.py" method="post">
			<button type="submit" value="Submit">Voltar ao Inicio</button>
			</form>""")

#DEBUG - CHAVES DEFINIDAS
print (form_is_defined)