"""=======================================================================================
INFORMATION ABOUT CODE *Coding ISO9001:2015 Standards
==========================================================================================
Chat Application with GUI and MultiMessage Feature using Socket programing and Tkinter
Change tkinter Version in Python 3 to Tkinter
This Script needs to be run before ChatUser2.py
Author: Prajinkya Pimpalghare
Date: 03-December-2017
Version: 1.0
Input Variable: None
==========================================================================================="""
import socket
from tkinter import Frame, Tk, Label, Entry, E, Button, W
from threading import Thread


class Server(object):
    def __init__(self):
        self.message = ""
        self.display_file = "Chat.txt"
        self.host = socket.gethostname()
        self.port = 1111
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.client_socket, self.machine_name = self.server_socket.accept()
            client = self.machine_name
        except BaseException as error:
            print("Error:", error)

    def sender(self, message):
        """
        For sending message and updating the file for GUI
        :param message:
        """
        self.message = message
        try:
            with open(self.display_file, 'a+') as file:
                file.write("#" + self.message + "\n")
            self.client_socket.send(self.message.encode())
        except BaseException as error:
            print("Error:", error)

    def receiver(self):
        """
        For Sending the message and updating the file for GUI
        """
        try:
            self.message = self.client_socket.recv(1024)
            with open(self.display_file, 'a+') as file:
                file.write("$" + self.message.decode() + "\n")
        except BaseException as error:
            print("Error:", error)


class ChatBox(Frame, object):
    def __init__(self, master, server):
        """
        For Creating the GUI for Chat application
        :param master:
        :param server:
        """
        super(ChatBox, self).__init__(master)
        self.server = server
        self.label = {}
        self.display_file = "Chat.txt"
        open(self.display_file, "a+").close()
        self.message = Entry(self)
        Label(self,text="YOU").grid(row=0,column=1,sticky=E)
        Label(self, text="SENDER").grid(row=0, column=0, sticky=W)
        self.message.grid(row=9, column=0)
        self.message.insert([27], "")
        Button(self, text=">>>", command=self.send_message, bg="green").grid(row=9, column=1, sticky=W)

    def main(self):
        """
        Main function for staring the message receiving action with GUI
        """
        try:
            with open(self.display_file, "r+") as file:
                for rowNm, line in enumerate(file.readlines()[-8:]):
                    if line[0] is "$":
                        Label(self, text=line.strip("$").strip(), bg="lightgreen").grid(row=rowNm+1, column=0,
                                                                                        sticky=W)
                    else:
                        Label(self, text=line.strip("#").strip(), bg="lightgreen").grid(row=rowNm+1, column=1,
                                                                                        sticky=E)
            self.message.delete(0, 'end')
            Thread(target=self.receive_message).start()
        except BaseException as error:
            print("Error:", error)

    def send_message(self):
        """
        It will clear up the screen and call the main msg sending function
        """
        self.server.sender(self.message.get())
        for index in range(1, 9):
            Label(self, text="                            ").grid(row=index, column=1, sticky=E)
            Label(self, text="                            ").grid(row=index, column=0, sticky=W)
        self.main()

    def receive_message(self):
        """
        It will call main receiver function
        """
        self.server.receiver()
        try:
            for index in range(1, 9):
                Label(self, text="                            ").grid(row=index, column=1, sticky=E)
                Label(self, text="                            ").grid(row=index, column=0, sticky=W)
            with open(self.display_file, "r+") as file:
                for rowNm, line in enumerate(file.readlines()[-8:]):
                    if line[0] is "$":
                        Label(self, text=line.strip("$").strip(), bg="lightgreen").grid(row=rowNm+1, column=0,
                                                                                        sticky=W)
                    else:
                        Label(self, text=line.strip("#").strip(), bg="lightgreen").grid(row=rowNm+1, column=1,
                                                                                        sticky=E)
        except BaseException as error:
            print("Error:", error)


if __name__ == '__main__':
    SERVER = Server()
    ROOT = Tk()
    ROOT.title("User One")
    BOX = ChatBox(master=ROOT, server=SERVER)
    while True:
        try:
            BOX.main()
            BOX.pack()
            ROOT.mainloop()
        except BaseException as error:
            print("Application has been closed", error)
            exit(0)
