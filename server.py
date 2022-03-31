import socket
from _thread import *
import sys
from module.player import Players
import pickle

server = "192.168.1.83"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3)
print("Waiting for a connection, Serveur Started")

players = Players()


def threaded_client(conn, player_id):
    conn.send(pickle.dumps(players.send_player(player_id)))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players.update(data)

            if not data:
                print("Disconnected")
                break
            else:
                reply = players.sendable(player_id)

                print('Received: ', data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to :", addr)

    start_new_thread(threaded_client, (conn, currentPlayer,))
    currentPlayer += 1
