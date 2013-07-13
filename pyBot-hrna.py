#!/usr/bin/python3

import socket

##config##

nick = "pyHbot"
host = "b0xi.eu"
port = 6667
ident = "pyHbot"
chan = "#tsunku"
realname = "pyHbot"

##END of cfg##

pyBot = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

pyBot.connect ((host, port))
print ("connecting to", host, "in port", port)
pyBot.send(b"NICK pyHbot")
pyBot.send(b"USER pyHbot b0xi BULLCRAP :pyHbot")	#yhdistää palvelimellllle...


while True:
print ("IM ALIVE")		#mitä tästä eteenpäin?.. eikä tämäkää toimi :D







