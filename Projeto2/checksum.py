import hashlib

def generateChecksum(arquivo):
	arq = open(arquivo, 'rb').read()
	hash = hashlib.md5()
	hash.update(arq)
	return hash.hexdigest()

#teste = generateChecksum('teste.txt')
#print (teste)
