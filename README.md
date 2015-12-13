# Trabalhos da Disciplina REDES - UFSCar

#Primeiro trabalho de redes

Grupo: Arieh Fabbro, Camilo Moreira, Cristian Pendenza

O primeiro trabalho de redes permitir a um usuário realizar uma busca de resultados de comandos de linha, a partir de um conjunto de máquinas Linux, através de uma interface web.

Dependências: Python 3.5 ou superior. Não funciona com versões anteriores a 3.4.X.

Modo de Usar:

1 - Coloque a página index.html na pasta root do seu servidor web. O arquivo pode ser renomeado se necessário.<br/>

2 - Coloque os arquivos webserver.py e backend.py na pasta /cgi-bin/ do seu servidor web.<br/>

3 - Deixe rodando 1 ou mais daemons, do arquivo daemon.py. Os daemons funcionam na porta 12000. Neste caso, os daemons precisam estar em PCs diferentes <br/>

4 - No arquivo do backend, atualize os IPs dos daemons que serão conectados.<br/>

<strong>ATENÇÃO:</strong> Se os daemons não estiverem rodando e os IPS desatualizados no backend, o passo 5 não vai funcionar.

4 - Entre na página Web que inseriu na página 1 e o projeto funcionará.<br/>

#Segundo trabalho de redes

Grupo: André Uenishi, Arieh Fabbro, Edna Partricia Martins e Fernando Messias da Silva

Programa feito no Python 3.

Cada integrante teve a responsabilidade de fazer os seguintes trechos do programa:

André Uenishi: Fazer o Go back N sem corrupção e sem perdas.

Arieh Fabbro: Fazer a estrutura base, código de enviar e receber pacotes sem corrupção e perdas.

Edna Patricia Martins: Fazer o código referente a perda dos pacotes depois do Go back N com corrupção ter sido feito.

Fernando Messias da Silva: Fazer o código referente a corrupção dos pacotes depois do Go back N ter sido feito.

O merge do projeto foi simples, o grupo do André, Edna e Fernando não tinha começado a fazer o trabalho e o Arieh já havia começado fizemos o merge colocando o que foi feito no trabalho do Arieh no novo grupo.
