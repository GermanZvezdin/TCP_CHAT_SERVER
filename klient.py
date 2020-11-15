# HTTP-клиент (пример работы с клиентами)
import socket
import json
import threading
def rcv_func(sock):
    data = None
    while True:
        try:
            data = sock.recv(2 ** 14)
            print(data.decode("utf-8"))
        except:
            pass

sock = socket.socket()
sock.connect(("127.0.0.1", 5050))

print("""Добропожаловать в  TCP-SERVER CHAT !
Введите свое имя:""", sep=' ')
name = input()
mess = {
        "user_name": name,
        "target_name": None,
        "message": None
}
sock.send(json.dumps(mess).encode())
print(f"""Добро пожаловать в чат {name}, введи сообщение или напиши quit для выхода""")

x = threading.Thread(target=rcv_func, args=(sock,))
x.start()

while(True):

    user_mess = input()
    if(user_mess == "quit"):
        break
    lst = user_mess.split(' ', maxsplit=1)
    lst[0] = lst[0].replace('[', '', 1)
    lst[0] = lst[0].replace(']', '', 1)

    print(lst)
    if(len(lst) > 1):
        mess = {
            "user_name": name,
            "target_name": lst[0],
            "message": lst[1]
        }
        sock.send(json.dumps(mess).encode())


print(f"До свидания {name}!")
sock.close()
