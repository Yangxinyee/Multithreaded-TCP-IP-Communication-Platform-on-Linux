import socket
import threading
import queue
import json  # json.dumps(some)打包   json.loads(some)解包
import time
import tkinter as tk
import tkinter.messagebox
import sys
import os
import pyautogui
IP = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
PORT = 8888
que = queue.Queue()                             # 用于存放客户端发送的信息的队列
users = []                                      # 用于存放在线用户的信息  [conn, user, addr]
lock = threading.Lock()                         # 创建锁, 防止多个线程写入数据的顺序打乱
# listbox1 = ''  # 用于显示在线用户的列表框
ii = 0  # 用于判断是开还是关闭列表框
threads = [] # 用于存储线程tid
# 事先约定的消息格式
# 普通的用户字符串消息 data = ' ' + users[j][1] + '：' + message[1] #message[1] = 用户:;【消息发送对象】users[j][1]是发送方名称
# 服务器通信的前期准备
# 1.初始化socket
# 2.执行bind函数，将服务能力绑定在已知的地址和端口
# 3.执行listen函数，将基础socket转换为服务器端特有的socket监听客户端请求
# 用户列表消息
# 将在线用户存入online列表并返回
def onlines():
    online = []
    for i in range(len(users)):
        online.append(users[i][1])
    return online

class server_deal: # 这是服务器页面
    global ban
    global users
    def __init__(self, window):
        self.window = window
        # 注册窗口
        self.window.title("管理员窗口")
        # self.window.geometry("300x140+605+320")
        self.window.geometry("450x360+500+220")
        self.window.resizable(0, 0)  # 限制窗口大小
        self.User = tk.StringVar()
        self.User.set('')
        # 创建多行文本框, 显示在线用户
        self.listbox1 = tkinter.Listbox(root)
        self.listbox1.place(x=310, y=0, width=130, height=320)
        # 查看在线用户按钮
        self.button1 = tkinter.Button(root, text='用户列表', command=self.show_users)
        self.button1.place(x=330, y=325, width=90, height=30)
        # # 显示用户的多行文本框
        # self.listbox1 = tkinter.Listbox(root)
        # self.listbox1.place(x=445, y=0, width=130, height=320)
        # 用户名标签
        self.labelUser = tk.Label(window, text='用户名')
        self.labelUser.place(x=20, y=100, width=100, height=20)
        self.entryUser = tk.Entry(window, width=80, textvariable=self.User)
        self.entryUser.place(x=120, y=100, width=130, height=20)
        # 禁言
        # self.window.bind('<Return>', self.deal_ban)  # 回车绑定禁言功能
        self.button = tk.Button(self.window, text="禁言", command=self.deal_ban)
        self.button.place(x=60, y=210, width=70, height=30)
        # 解禁
        self.button = tk.Button(self.window, text="解禁", command=self.deal_unban)
        self.button.place(x=185, y=210, width=70, height=30)
        #关闭窗口就结束进程
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
        # 销毁root窗口
        self.window.destroy()
        try:
            os._exit(0)
        except:
            print("failed to close")

    def show_users(self):
        global ii
        if ii == 1:
            # self.listbox1.place(x=445, y=0, width=130, height=320)
            self.listbox1.place_forget()  # 隐藏控件
            ii = 0
        else:
            self.listbox1.place(x=310, y=0, width=130, height=320)
            # self.listbox1.place_forget()  # 隐藏控件
            ii = 1
        self.listbox1.delete(0, tkinter.END)  # 清空列表框
        number = ('   在线用户数: ' + str(len(users)))
        self.listbox1.insert(tkinter.END, number)
        self.listbox1.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
        self.listbox1.insert(tkinter.END, '【群发】')
        self.listbox1.itemconfig(tkinter.END, fg='green')
        for i in range(len(users)):
            self.listbox1.insert(tkinter.END, (users[i][1]))
            self.listbox1.itemconfig(tkinter.END, fg='green')


class ChatServer(threading.Thread): # ChatServer 继承了threading.Thread
    global users, que, lock
    def __init__(self, port): # 析构函数用来创建套接字文件
        threading.Thread.__init__(self) # 保留了threading.thread的析构函数
        self.ADDR = ('', port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建一个IPV4、TCP的套接字 用于监听服务器请求
        ss = self.s
        print("thread name = {}, thread id = {}".format(threading.current_thread().name, threading.current_thread().ident))  # 表明ChatServer运行于主线程
    # 用于接收所有客户端发送信息的函数

    def tcp_connect(self, conn, addr):   # 客户端和服务器连接成功就会创建一个新线程执行此函数addr是地址 ip+端口号
        # 连接后将用户信息添加到users列表
        print("thread name = {}, thread id = {}".format(threading.current_thread().name,
                                                        threading.current_thread().ident))
        user = conn.recv(1024)  # 接收用户名
        user = user.decode()
        for i in range(len(users)):
            if user == users[i][1]:
                print('User already exist')
                user = '' + user + '_2'
        if user == 'no':
            user = addr[0] + ':' + str(addr[1])
        users.append((conn, user, addr))
        print('新的连接:', addr, ':', user, end='')         # 打印用户名
        d = onlines()                                      # 有新连接则刷新客户端的在线用户显示
        self.recv(d, addr)  #  slef.recv 函数用于初次连接后将用户列表加入消息队列广播给所有客户端
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
                        # 1.获取os所在的目录
                        working_path = os.getcwd()
                        # 2.读取发送时的文件名
                        file_name = os.path.basename(file_path)
                        # 3.叠加得到新路径（文件保存路径）
                        file_path = os.path.join(working_path, 'server_photos', file_name)
                        now_size = 0
                        with open(file_path, 'wb') as f:
                            while now_size < file_size:
                                tmp_data = conn.recv(1024)
                                now_size += len(tmp_data)
                                f.write(tmp_data)
                        with open(file_path, 'rb') as f:
                            tmp_data = f.read()
                            self.recv(data, addr)  # 保存信息到队列
                            que.put(("图片", tmp_data))
                        # que.put(("图片", new_data))
                except:
                    self.recv(data, addr)  # 保存信息到队列
            conn.close()
        except:
            print(user + ' 断开连接')
            self.delUsers(conn, addr)                             # 将断开用户移出users
            conn.close()
            self.show_users()

    # 判断断开用户在users中是第几位并移出列表, 刷新客户端的在线用户显示
    def delUsers(self, conn, addr):  # 定义删除用户函数
        a = 0
        for i in users:
            if i[0] == conn:
                users.pop(a)
                print(' 在线用户: ', end='')         # 打印剩余在线用户(conn)
                d = onlines()
                self.recv(d, addr)
                print(d)
                break
            a += 1

    def show_users(self):
        p1.listbox1.delete(0, tkinter.END)  # 清空列表框
        number = ('   在线用户数: ' + str(len(users)))
        p1.listbox1.insert(tkinter.END, number)
        p1.listbox1.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
        p1.listbox1.insert(tkinter.END, '【群发】')
        p1.listbox1.itemconfig(tkinter.END, fg='green')
        for i in range(len(users)):
            p1.listbox1.insert(tkinter.END, (users[i][1]))
            p1.listbox1.itemconfig(tkinter.END, fg='green')

    # 将接收到的信息(ip,端口以及发送的信息)存入que队列
    def recv(self, data, addr):
        global users
        lock.acquire()
        # 每次有消息发来都更新一下在线用户列表
        try:
            data = json.loads(data)
            que.put((addr, data))  # 将消息加入队列
        #
        except:
            que.put((addr, data))  # 将消息加入队列
        finally:
            lock.release()

    # 将队列que中的消息发送给所有连接到的用户
    def sendData(self): # 这是mainthread分支出的第一个子线程
        # global ban
        print("thread name = {}, thread id = {}".format(threading.current_thread().name,
                                                        threading.current_thread().ident))
        while True:
            if not que.empty():
                data = ''
                reply_text = ''
                message = que.get()                               # 取出队列第一个元素 message[0] = addr, message[1] = data
                print(message)
                if isinstance(message[1], str):                   # 如果data是str则返回Ture,isinstance判断类型是否对应字符串
                    # print()
                    # print(users[0][0])
                    for i in range(len(users)):
                        # user[i][1]是用户名, users[i][2]是addr, 将message[0]改为用户名
                        source_user = 0
                        if message[0] == '!':
                            data = ' ' + 'server' + '：' + message[1]
                            print(' this: message is from server')  # 打印该信息的发送源
                            print('The User {} has been banned'.format(list(message[1].split(":;"))[2]))
                        if message[0] == '@':
                            data = ' ' + 'server' + '：' + message[1]
                            print(' this: message is from server')  # 打印该信息的发送源
                            print('The User {} has been freed'.format(list(message[1].split(":;"))[2]))
                        else:
                            for j in range(len(users)):
                                if message[0] == users[j][2]: # message[0] = addr, message[1] = data 判断该信息是哪个用户发出来的
                                    print(users[j][2])
                                    print(' this: message is from user[{}]'.format(j)) # 打印该信息的发送源
                                    data = ' ' + users[j][1] + '：' + message[1] #message[1] = 用户:;【消息发送对象】
                                print(data)
                        users[i][0].send(data.encode()) # 每条消息都会发生送给所有人 这条语句是将data编码并且发送到每个user的套接字里面
                # data = data.split(':;')[0]
                if isinstance(message[1], list) or isinstance(message[1], dict):  # 同上
                    # 如果是list或dict则打包后直接发送
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
                            print("服务器接收数据失败") # 接收时间长于5s说明消息丢失
                            # trans_flag = 1
                    photo_message = que.get()
                    print(type(photo_message))
                    # print(photo_message)
                    print("The message is from user" + message[1]['from_user'])
                    time.sleep(0.5)    # 确保当前字典消息已经送达
                    for i in range(len(users)):
                        users[i][0].sendall(photo_message[1])
                        print("server sent photo message")


    def run(self):  # 重写run方法 run是mainthread线程分支出的第一个子线程 对于一个thread类来说，run是主线程自动分支出来的，名称为Thread-1
        self.s.bind(self.ADDR) # 将套接字绑定到已有端口
        self.s.listen(5)
        print('服务器正在运行中...')
        print("thread name = {}, thread id = {}".format(threading.current_thread().name,
                                                        threading.current_thread().ident))
        q = threading.Thread(target=self.sendData) # senddata是主线程分支出的第二个子线程，名称为Tread-2, 让它启动，确保其在连接前已经处于可发送状态
        q.setDaemon(True)
        threads.append(q)
        q.start()
        add_thread_flag=0
        while True:
            conn, addr = self.s.accept()  # accept()接受一个客户端的连接请求，并返回一个新的套接字，如果没有接收到请求，那么这里是被阻塞状态
            t = threading.Thread(target=self.tcp_connect, args=(conn, addr)) # 按顺序每个tcp_connect线程从thread-3开始
            t.setDaemon(True)
            t.start()
        self.s.close()


if __name__ == '__main__':
    cserver = ChatServer(PORT)
    cserver.start() # 申请系统线程，这里是main线程
    root = tk.Tk()
    p1 = server_deal(root)  # 这两个页单，可单独运行
    root.mainloop()

