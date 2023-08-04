import socket
import threading
import queue
import json  # json.dumps(some)pack   json.loads(some)unpack
import time
import tkinter as tk
import tkinter.messagebox
import sys
import os
import pyautogui
IP = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
PORT = 8888
que = queue.Queue()                             # A queue for storing information sent by the client
users = []                                      # It is used to store online user information  [conn, user, addr]
lock = threading.Lock()                         # Create locks that prevent the order in which multiple threads write data from being scrambled
ii = 0  # Used to determine whether to open or close a list box
threads = [] # Used to store thread ids
# A pre-agreed message format
# Normal user string message data = ' ' + users[j][1] + '：' + message[1] #message[1] = user:;【Message sending object】users[j][1]Is the name of the sender
# Preparations for server communication
# 1.initialize socket
# 2.Execute the bind function to bind the service capability to a known address and port
# 3.Execute the listen function to convert the base socket to a server-side specific socket to listen to client requests
# User list message
# Put online users in the online list and return
def onlines():
    online = []
    for i in range(len(users)):
        online.append(users[i][1])
    return online

class server_deal: # This is the server page
    global ban
    global users
    def __init__(self, window):
        self.window = window
        # Registration window
        self.window.title("管理员窗口")
        # self.window.geometry("300x140+605+320")
        self.window.geometry("450x360+500+220")
        self.window.resizable(0, 0)  # Limit window size
        self.User = tk.StringVar()
        self.User.set('')
        # Create a multi-line text box to display online users
        self.listbox1 = tkinter.Listbox(root)
        self.listbox1.place(x=310, y=0, width=130, height=320)
        # View the online user button
        self.button1 = tkinter.Button(root, text='用户列表', command=self.show_users)
        self.button1.place(x=330, y=325, width=90, height=30)
        # # Displays a multiline text box for the user
        # self.listbox1 = tkinter.Listbox(root)
        # self.listbox1.place(x=445, y=0, width=130, height=320)
        # User name tag
        self.labelUser = tk.Label(window, text='用户名')
        self.labelUser.place(x=20, y=100, width=100, height=20)
        self.entryUser = tk.Entry(window, width=80, textvariable=self.User)
        self.entryUser.place(x=120, y=100, width=130, height=20)
        # banned to post
        # self.window.bind('<Return>', self.deal_ban)  # Carriage return binding prohibition function
        self.button = tk.Button(self.window, text="禁言", command=self.deal_ban)
        self.button.place(x=60, y=210, width=70, height=30)
        # lift a ban
        self.button = tk.Button(self.window, text="解禁", command=self.deal_unban)
        self.button.place(x=185, y=210, width=70, height=30)
        # Close the window to end the process
        self.window.protocol("WM_DELETE_WINDOW", self.end)
        self.show_users()

    def deal_ban(self):
        ban_name = self.entryUser.get()
        data = "【禁言警告】" + ":;" + "server" + ":;" + ban_name
        que.put(("!", data))
        tk.messagebox.showinfo('温馨提示', message='禁言成功！')


    def deal_unban(self):
        unban_name = self.entryUser.get()
        data = "【解禁提示】" + ":;" + "server" + ":;" + unban_name
        que.put(("@", data))
        tk.messagebox.showinfo('温馨提示', message='解禁成功！')

    def end(self):
        # Destroy root window
        self.window.destroy()
        try:
            os._exit(0)
        except:
            print("failed to close")

    def show_users(self):
        global ii
        if ii == 1:
            # self.listbox1.place(x=445, y=0, width=130, height=320)
            self.listbox1.place_forget()  # Hidde the control button
            ii = 0
        else:
            self.listbox1.place(x=310, y=0, width=130, height=320)
            # self.listbox1.place_forget()  # Hidde the control button
            ii = 1
        self.listbox1.delete(0, tkinter.END)  # Clear list box
        number = ('   在线用户数: ' + str(len(users)))
        self.listbox1.insert(tkinter.END, number)
        self.listbox1.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
        self.listbox1.insert(tkinter.END, '【群发】')
        self.listbox1.itemconfig(tkinter.END, fg='green')
        for i in range(len(users)):
            self.listbox1.insert(tkinter.END, (users[i][1]))
            self.listbox1.itemconfig(tkinter.END, fg='green')


class ChatServer(threading.Thread): # ChatServer inherits from threading.Thread
    global users, que, lock
    def __init__(self, port): # The destructor is used to create the socket file
        threading.Thread.__init__(self) # The destructor from threading.thread is retained
        self.ADDR = ('', port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create an IPV4, TCP socket to listen for server requests
        ss = self.s
        print("thread name = {}, thread id = {}".format(threading.current_thread().name, threading.current_thread().ident))  # Indicates that ChatServer is running on the main thread
    
    # A function that receives messages sent by all clients
    def tcp_connect(self, conn, addr):   # A successful connection between the client and the server creates a new thread that executes this function addr is the address ip+ port number
        # Add the user information to the users list after the connection
        print("thread name = {}, thread id = {}".format(threading.current_thread().name,
                                                        threading.current_thread().ident))
        user = conn.recv(1024)  # Receiving user name
        user = user.decode()
        for i in range(len(users)):
            if user == users[i][1]:
                print('User already exist')
                user = '' + user + '_2'
        if user == 'no':
            user = addr[0] + ':' + str(addr[1])
        users.append((conn, user, addr))
        print('新的连接:', addr, ':', user, end='')         # Print user name
        d = onlines()                                      # Refresh the online user display on the client when a new connection is available
        self.recv(d, addr)  #  The slef.recv function is used to broadcast the user list to all clients in a message queue after the initial connection
        self.show_users()
        try:
            while True:
                data = conn.recv(1024)
                data = data.decode()
                try:
                    data = json.loads(data)
                    if isinstance(data, dict):
                        file_size = data.get('file_length')
                        file_path = data.get('file_name')
                        # 1. Obtain the directory where the os is stored
                        working_path = os.getcwd()
                        # 2. Read the file name when the file is sent
                        file_name = os.path.basename(file_path)
                        # 3. Overlay to get a new path (file saving path)
                        file_path = os.path.join(working_path, 'server_photos', file_name)
                        now_size = 0
                        with open(file_path, 'wb') as f:
                            while now_size < file_size:
                                tmp_data = conn.recv(1024)
                                now_size += len(tmp_data)
                                f.write(tmp_data)
                        with open(file_path, 'rb') as f:
                            tmp_data = f.read()
                            self.recv(data, addr)  # Save the message to the queue
                            que.put(("图片", tmp_data))
                        # que.put(("图片", new_data))
                except:
                    self.recv(data, addr)  # Save the message to the queue
            conn.close()
        except:
            print(user + ' 断开连接')
            self.delUsers(conn, addr)                             # Move the disconnected user out of users
            conn.close()
            self.show_users()

    # Determine the number of the disconnected user in the users list, remove the disconnected user from the list, and refresh the online user display on the client
    def delUsers(self, conn, addr):  # Define the delete user function
        a = 0
        for i in users:
            if i[0] == conn:
                users.pop(a)
                print(' 在线用户: ', end='')         # Print Remaining Online Users (conn)
                d = onlines()
                self.recv(d, addr)
                print(d)
                break
            a += 1

    def show_users(self):
        p1.listbox1.delete(0, tkinter.END)  # Clear list box
        number = ('   在线用户数: ' + str(len(users)))
        p1.listbox1.insert(tkinter.END, number)
        p1.listbox1.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
        p1.listbox1.insert(tkinter.END, '【群发】')
        p1.listbox1.itemconfig(tkinter.END, fg='green')
        for i in range(len(users)):
            p1.listbox1.insert(tkinter.END, (users[i][1]))
            p1.listbox1.itemconfig(tkinter.END, fg='green')

    # The received information (ip, port, and sent information) is stored in the que queue
    def recv(self, data, addr):
        global users
        lock.acquire()
        # Update the online user list every time a message comes in
        try:
            data = json.loads(data)
            que.put((addr, data))  # Queue the message
        #
        except:
            que.put((addr, data))  # Queue the message
        finally:
            lock.release()

    # Sends messages in the queue que to all connected users
    def sendData(self): # This is the first child thread that the mainthread branches out of
        # global ban
        print("thread name = {}, thread id = {}".format(threading.current_thread().name,
                                                        threading.current_thread().ident))
        while True:
            if not que.empty():
                data = ''
                reply_text = ''
                message = que.get()                               # Fetch the first element of the queue, message[0] = addr, message[1] = data
                print(message)
                if isinstance(message[1], str):                   # Return true if data is str, and isinstance determines whether the type corresponds to a string
                    # print()
                    # print(users[0][0])
                    for i in range(len(users)):
                        # user[i][1] is user name, users[i][2] is addr, Change message[0] to the user name
                        source_user = 0
                        if message[0] == '!':
                            data = ' ' + 'server' + '：' + message[1]
                            print(' this: message is from server')  # Print the sending source of the message
                            print('The User {} has been banned'.format(list(message[1].split(":;"))[2]))
                        if message[0] == '@':
                            data = ' ' + 'server' + '：' + message[1]
                            print(' this: message is from server')  # Print the sending source of the message
                            print('The User {} has been freed'.format(list(message[1].split(":;"))[2]))
                        else:
                            for j in range(len(users)):
                                if message[0] == users[j][2]: # message[0] = addr, message[1] = data Determine which user sent the message
                                    print(users[j][2])
                                    print(' this: message is from user[{}]'.format(j)) # Print the sending source of the message
                                    data = ' ' + users[j][1] + '：' + message[1] # message[1] = user:;【消息发送对象】
                                print(data)
                        users[i][0].send(data.encode()) # Each message is sent to everyone and this statement encodes data and sends it to each user's socket
                # data = data.split(':;')[0]
                if isinstance(message[1], list) or isinstance(message[1], dict):  # ditto
                    # If it is a list or dict, package it and send it directly
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            users[i][0].send(data.encode())
                        except:
                            pass
                if isinstance(message[1], dict):
                    wait_times = 0
                    while que.empty():
                        print("The data hasn's already arrived")
                        time.sleep(0.5)
                        wait_times += 0.5
                        if wait_times >= 10:
                            print("服务器接收数据失败") # If the receiving time is longer than 5 seconds, the message is lost
                            # trans_flag = 1
                    photo_message = que.get()
                    print(type(photo_message))
                    # print(photo_message)
                    print("The message is from user" + message[1]['from_user'])
                    time.sleep(0.5)    # Ensure that the current dictionary message has been delivered
                    for i in range(len(users)):
                        users[i][0].sendall(photo_message[1])
                        print("server sent photo message")


    def run(self):  # Overwrite the run method run is the first subthread to be branched from the mainthread thread. For a Thread class, run is automatically branched from the mainthread and is named thread-1
        self.s.bind(self.ADDR) # Bind a socket to an existing port
        self.s.listen(5)
        print('The server is running...')
        print("thread name = {}, thread id = {}".format(threading.current_thread().name,
                                                        threading.current_thread().ident))
        q = threading.Thread(target=self.sendData) # senddata is the second child thread that branches out of the main thread, named Tread-2, let it start, making sure it is in a sendable state before connecting
        q.setDaemon(True)
        threads.append(q)
        q.start()
        add_thread_flag=0
        while True:
            conn, addr = self.s.accept()  # accept() accepts a connection request from a client and returns a new socket. If no request is received, it is blocked
            t = threading.Thread(target=self.tcp_connect, args=(conn, addr)) # Each tcp connect thread starts from Thread-3 in sequence
            t.setDaemon(True)
            t.start()
        self.s.close()


if __name__ == '__main__':
    cserver = ChatServer(PORT)
    cserver.start() # Apply for the system thread, in this case the main thread
    root = tk.Tk()
    p1 = server_deal(root)  # These two sheets can be run separately
    root.mainloop()

