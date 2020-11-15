import socket
import threading
from time import sleep
import json

user_list = {}


def thread_func(conn, adr):
    name = None
    global user_list
    while True:
        data = conn.recv(2 ** 14)
        if data:
            json_obj = json.loads(data.decode("utf-8"))
            print(json_obj)
            if json_obj['target_name'] == None:
                user_list[json_obj['user_name']] = conn
                name = json_obj['user_name']
            else:
                try:
                    mess = f"From {json_obj['user_name']} text: " + json_obj['message']
                    user_list[json_obj['target_name']].send(mess.encode())
                except:
                    print(f"Not user - {json_obj['target_name']}")
                    conn.send(f"Пользователь {json_obj['target_name']} не в сети.".encode())
        else:
            print("timeout")
            break

    conn.close()
    del user_list[name]
    sleep(0.1)


sock = socket.socket()
sock.bind(('127.0.0.1', 5050))
sock.listen(10)

while True:
    conn, adr = sock.accept()
    if conn in user_list:
        continue
    x = threading.Thread(target=thread_func, args=(conn, adr,))
    x.start()
