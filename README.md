# Python-Sockets

Trabalho da disciplina Redes de Computadores 2
Comunicação utilizando sockets, implementada em python

# Como funciona

Os sockets são construídos baseados em endereços IPv4 e utilizando o protocolo TCP
A ideia é que os clients enviem mensagens ao servidor, que por sua vez deve retransmitir para todos os outros clients ligados a ele

Os clients tem acesso às mensagens transmitidas antes da sua entrada e elas são retransmitidas apenas para ele, ou seja, acesso completo ao histórico de mensagem desde o inicio do servidor

Os clients possuem o comando !quit que os desconecta do servidor, e há um client especial chamado admin(login: admin e senha:admin) que possui o comando !shutdown.
Este comando emite um alerta de 10s(countdown com retorno de mensagem a cada segundo) indicando o encerramento do servidor, porém é necessário ainda corrigir falha em que o servidor não encerra.
