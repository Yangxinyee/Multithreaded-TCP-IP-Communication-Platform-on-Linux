import socket
import threading
import json  # json.dumps(some)打包   json.loads(some)解包
import tkinter as tk
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText  # 导入多行文本框用到的包
import tkinter.filedialog
import os
import datetime
import pyscreenshot as ImageGrab
import MD5
from PIL import ImageTk
import re
import pyautogui
import time
import cv2
from PIL import Image
from matplotlib import pyplot as plt
import wave
import pyaudio
from playsound import playsound
from tkinter import font
IP = ''
PORT = ''
user = ''
# que = queue.Queue() # 用于接收消息的队列
listbox1 = ''  # 用于显示在线用户的列表框
ii = 0  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = '【群发】'  # 聊天对象, 默认为群聊
ban_flag = False
photos = []
link_cnt = 0 # 用于链接绑定计数
photo_list = [] # 用于映射图片文件
record_sound_id = 0 # 用于记录当前的录音段数，方便生成文件


class log:  # 这是登录页面
    def __init__(self, window):
        self.window = window
        # 登录窗口 初始位置和长宽高和背景设置
        self.window.title("聊天登录窗口")
        self.sw = self.window.winfo_screenwidth()
        self.sh = self.window.winfo_screenheight()
        self.w = 400
        self.h = 500
        self.x = (self.sw - self.w) / 2
        self.y = (self.sh - self.h) / 2
        self.window.geometry("%dx%d+%d+%d" % (self.w, self.h, self.x, self.y))
        self.window.resizable(0, 0)
        # 图片，自行编辑
        self.loggin_benner = Image.open('aikun.png')
        self.loggin_benner = self.loggin_benner.resize((400, 300))
        self.login_benner = ImageTk.PhotoImage(self.loggin_benner)
        self.imgLabel = tk.Label(self.window, image=self.login_benner)
        self.imgLabel.place(x=0, y=0)
        # 调整字体
        self.window.my_font1 = font.Font(family="微软雅黑", size=12, weight=font.BOLD)
        self.window.my_font2 = font.Font(family="Times New Roman", size=12)
        self.window.my_font3 = font.Font(family="华光胖头鱼_CNKI", size=8)
        # 标签 地址；用户；密码
        tk.Label(self.window, text="地 址:", font=self.window.my_font1).place(x=80, y=320)
        tk.Label(self.window, text="昵 称：", font=self.window.my_font1).place(x=80, y=360)
        tk.Label(self.window, text="密 码：", font=self.window.my_font1).place(x=80, y=400)
        # 文本框 地址
        self.IP1 = tk.StringVar()
        self.IP1.set('127.0.0.1:8888')  # 默认显示的ip和端口
        self.entryIP = tk.Entry(self.window, textvariable=self.IP1, font=self.window.my_font2)
        self.entryIP.place(x=140, y=320)
        # 文本框 用户名
        self.User = tk.StringVar()
        self.User.set('')
        self.entryUser = tk.Entry(self.window, textvariable=self.User, font=self.window.my_font2)
        self.entryUser.place(x=140, y=360)
        # 文本框 密码
        self.Passwd = tk.StringVar()
        self.Passwd.set('')
        self.entryPasswd = tk.Entry(self.window, textvariable=self.Passwd, show="●")
        self.entryPasswd.place(x=140, y=400)
        # 登录
        window.bind('<Return>', self.login)  # 回车绑定登录功能
        self.button = tk.Button(self.window, text="登录", command=self.login, font=self.window.my_font1)
        self.button.place(x=100, y=440)
        self.button1 = tk.Button(self.window, text="注册", command=self.change, font=self.window.my_font1)
        self.button1.place(x=230, y=440)
        # 提示标签
        self.tsLabel = tk.Label(self.window, text="Designed for aikun chatroom", fg="pink", font=self.window.my_font3)
        self.tsLabel.pack(side=tk.BOTTOM, expand='no', anchor='se')

    def change(self):
        self.button.destroy()
        register(root)

    def check_user(self, user, key):
        print("login: user: " + user + ", key: " + key)
        pre_user = False
        is_user = True
        with open("data/user.txt", 'r', encoding="utf-8") as user_data:
            for line in user_data:
                line = line.replace("\n", "")
                if is_user and line == user:
                    pre_user = True
                elif (not is_user) and pre_user:
                    return line == key
                is_user = not is_user
        return False

    def login(self):
        global IP
        global PORT
        global user
        IP, PORT = self.entryIP.get().split(':')  # 获取IP和端口号
        passwd = self.entryPasswd.get()  # 获取密码
        # 密码传md5
        passwd = MD5.gen_md5(passwd)
        PORT = int(PORT)  # 端口号需要为int类型
        user = self.entryUser.get()
        if not user:
            tkinter.messagebox.showerror('温馨提示', message='请输入任意的用户名！')
        else:
            # 检查用户名和密码是否正确
            if not self.check_user(user, passwd):
                tkinter.messagebox.showerror('温馨提示', message='请输入正确的密码！')
            else:
                self.window.destroy()  # 关闭窗口


class register:  # 这是注册页面
    def __init__(self, window):
        self.window = window
        # 注册窗口
        self.window.title("注册")
        self.window.geometry("300x140+605+320")
        self.window.resizable(0, 0)  # 限制窗口大小
        self.User = tkinter.StringVar()
        self.User.set('')
        self.Passwd = tkinter.StringVar()
        self.Passwd.set('')
        self.ConfPasswd = tkinter.StringVar()
        self.ConfPasswd.set('')
        # 用户名标签
        self.labelUser = tkinter.Label(window, text='用户名')
        self.labelUser.place(x=20, y=10, width=100, height=20)
        self.entryUser = tkinter.Entry(window, width=80, textvariable=self.User)
        self.entryUser.place(x=120, y=10, width=130, height=20)
        # 密码标签
        self.labelPasswd = tkinter.Label(window, text='密码')
        self.labelPasswd.place(x=30, y=40, width=80, height=20)
        self.entryPasswd = tkinter.Entry(window, width=80, textvariable=self.Passwd)
        self.entryPasswd.place(x=120, y=40, width=130, height=20)
        # 确认密码标签
        self.labelconPasswd = tkinter.Label(window, text='确认密码')
        self.labelconPasswd.place(x=30, y=70, width=80, height=20)
        self.entryconPasswd = tkinter.Entry(window, width=80, textvariable=self.ConfPasswd)
        self.entryconPasswd.place(x=120, y=70, width=130, height=20)
        # 按钮
        self.window.bind('<Return>', self.regi)  # 回车绑定登录功能
        self.button = tk.Button(self.window, text="注册", command=self.regi)
        self.button.place(x=55, y=100, width=70, height=30)
        self.button = tk.Button(self.window, text="返回", command=self.change)
        self.button.place(x=180, y=100, width=70, height=30)

    def change(self):
        self.button.destroy()
        log(root)

    def check_regi(self):
        user = self.entryUser.get()
        passwd = self.entryPasswd.get()
        # 密码传md5
        passwd = MD5.gen_md5(passwd)
        conpasswd = self.entryconPasswd.get()
        conpasswd = MD5.gen_md5(conpasswd)
        try:
            with open("data/user.txt", 'r', encoding="utf-8") as user_data:
                is_user = True
                for line in user_data:
                    line = line.replace("\n", "")
                    if is_user and line == user:
                        # 用户名已被注册
                        return 1
                    is_user = not is_user
            # 添加用户和密码md5
            if conpasswd == passwd:
                with open("data/user.txt", 'a', encoding="utf-8") as user_data:
                    user_data.write(user + "\n")
                    user_data.write(passwd + "\n")
                    # 注册成功
                    print("register: user: " + user + ", key: " + passwd)
                return 2
            else:
                tkinter.messagebox.showerror('温馨提示', message='两次输入的密码不一致！')

        except Exception as e:
            print("添加用户数据出错：" + str(e))
            return False

    def regi(self):
        flag = self.check_regi()
        if flag == 1:
            tkinter.messagebox.showerror('温馨提示', message='该用户名已被注册，请重新输入！')
        elif flag == 2:
            # 注册成功，返回登录页面
            tkinter.messagebox.showinfo('温馨提示', '注册成功！')
            self.button.destroy()
            log(root)

root = tk.Tk()
p1 = log(root)  # 这两个页单，可单独运行
root.mainloop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))  # 申请和对应的端口建立连接执行connect函数向服务器端的地址和端口发起连接请求

if user:
    s.send(user.encode())  # 发送用户名
else:
    s.send('no'.encode())  # 没有输入用户名则标记no

# 如果没有用户名则将ip和端口号设置为用户名
addr = s.getsockname()  # 获取客户端ip和端口号
addr = addr[0] + ':' + str(addr[1])
if user == '':
    user = addr
print(user)
# 聊天窗口
# 创建图形界面
root = tkinter.Tk()
root.title(user)  # 窗口命名为用户名
root['height'] = 400
root['width'] = 580
root.resizable(0, 0)  # 限制窗口大小

# 创建多行文本框
listbox = ScrolledText(root)
listbox.place(x=5, y=0, width=570, height=320)
# 文本框使用的字体颜色
listbox.tag_config('red', foreground='red')
listbox.tag_config('blue', foreground='blue')
listbox.tag_config('green', foreground='green')
listbox.tag_config('pink', foreground='pink')
listbox.insert(tkinter.END, '欢迎加入聊天室 ！', 'blue')

# 表情功能代码部分
# 使用全局变量, 方便创建和销毁
b1 = ''
b2 = ''
b3 = ''
b4 = ''
b5 = ''
b6 = ''
b7 = ''
b8 = ''
b9 = ''
b10 = ''
b11 = ''
b12 = ''
b13 = ''
b14 = ''
b15 = ''
b16 = ''
b17 = ''
b18 = ''
b19 = ''
b20 = ''
# 将图片打开存入变量中
p1 = tkinter.PhotoImage(file='./emoji/doge.png')
p2 = tkinter.PhotoImage(file='./emoji/OK.png')
p3 = tkinter.PhotoImage(file='./emoji/保佑.png')
p4 = tkinter.PhotoImage(file='./emoji/偷笑.png')
p5 = tkinter.PhotoImage(file='./emoji/傲娇.png')
p6 = tkinter.PhotoImage(file='./emoji/再见.png')
p7 = tkinter.PhotoImage(file='./emoji/加油.png')
p8 = tkinter.PhotoImage(file='./emoji/口罩.png')
p9 = tkinter.PhotoImage(file='./emoji/吃瓜.png')
p10 = tkinter.PhotoImage(file='./emoji/吐.png')
p11 = tkinter.PhotoImage(file='./emoji/吓.png')
p12 = tkinter.PhotoImage(file='./emoji/呆.png')
p13 = tkinter.PhotoImage(file='./emoji/呲牙.png')
p14 = tkinter.PhotoImage(file='./emoji/哈哈.png')
p15 = tkinter.PhotoImage(file='./emoji/哈欠.png')
p16 = tkinter.PhotoImage(file='./emoji/响指.png')
p17 = tkinter.PhotoImage(file='./emoji/哦呼.png')
p18 = tkinter.PhotoImage(file='./emoji/哭泣.png')
p19 = tkinter.PhotoImage(file='./emoji/喜极而泣.png')
p20 = tkinter.PhotoImage(file='./emoji/喜欢.png')
# 用字典将标记与表情图片一一对应, 用于后面接收标记判断表情贴图
dic = {'doge': p1, 'OK': p2, '保佑': p3, '偷笑': p4, '傲娇': p5, '再见': p6, '加油': p7, '口罩': p8,
       '吃瓜': p9, '吐': p10, '吓': p11, '呆': p12, '呲牙': p13, '哈哈': p14, '哈欠': p15, '响指': p16,
       '哦呼': p17, '哭泣': p18, '喜极而泣': p19, '喜欢': p20}
ee = 0  # 判断表情面板开关的标志


# 发送表情图标记的函数, 在按钮点击事件中调用
def mark(exp):  # 参数是发的表情图标记, 发送后将按钮销毁
    global ee
    if '【群发】' not in users:
        users.append('【群发】')
    if not judge_send_legal():
        return
    mes = exp + ':;' + user + ':;' + chat
    s.send(mes.encode())
    b1.destroy()
    b2.destroy()
    b3.destroy()
    b4.destroy()
    b5.destroy()
    b6.destroy()
    b7.destroy()
    b8.destroy()
    b9.destroy()
    b10.destroy()
    b11.destroy()
    b12.destroy()
    b13.destroy()
    b14.destroy()
    b15.destroy()
    b16.destroy()
    b17.destroy()
    b18.destroy()
    b19.destroy()
    b20.destroy()
    ee = 0

# 对应的函数
def bb1():
    mark('doge')
def bb2():
    mark('OK')
def bb3():
    mark('保佑')
def bb4():
    mark('偷笑')
def bb5():
    mark('傲娇')
def bb6():
    mark('再见')
def bb7():
    mark('加油')
def bb8():
    mark('口罩')
def bb9():
    mark('吃瓜')
def bb10():
    mark('吐')
def bb11():
    mark('吓')
def bb12():
    mark('呆')
def bb13():
    mark('呲牙')
def bb14():
    mark('哈哈')
def bb15():
    mark('哈欠')
def bb16():
    mark('响指')
def bb17():
    mark('哦呼')
def bb18():
    mark('哭泣')
def bb19():
    mark('喜极而泣')
def bb20():
    mark('喜欢')


def express():
    global b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, b19, b20, ee
    if ee == 0:
        ee = 1
        b1 = tkinter.Button(root, command=bb1, image=p1,
                            relief=tkinter.FLAT, bd=0)
        b2 = tkinter.Button(root, command=bb2, image=p2,
                            relief=tkinter.FLAT, bd=0)
        b3 = tkinter.Button(root, command=bb3, image=p3,
                            relief=tkinter.FLAT, bd=0)
        b4 = tkinter.Button(root, command=bb4, image=p4,
                            relief=tkinter.FLAT, bd=0)
        b5 = tkinter.Button(root, command=bb5, image=p5,
                            relief=tkinter.FLAT, bd=0)
        b6 = tkinter.Button(root, command=bb6, image=p6,
                            relief=tkinter.FLAT, bd=0)
        b7 = tkinter.Button(root, command=bb7, image=p7,
                            relief=tkinter.FLAT, bd=0)
        b8 = tkinter.Button(root, command=bb8, image=p8,
                            relief=tkinter.FLAT, bd=0)
        b9 = tkinter.Button(root, command=bb9, image=p9,
                            relief=tkinter.FLAT, bd=0)
        b10 = tkinter.Button(root, command=bb10, image=p10,
                            relief=tkinter.FLAT, bd=0)
        b11 = tkinter.Button(root, command=bb11, image=p11,
                            relief=tkinter.FLAT, bd=0)
        b12 = tkinter.Button(root, command=bb12, image=p12,
                            relief=tkinter.FLAT, bd=0)
        b13 = tkinter.Button(root, command=bb13, image=p13,
                            relief=tkinter.FLAT, bd=0)
        b14 = tkinter.Button(root, command=bb14, image=p14,
                            relief=tkinter.FLAT, bd=0)
        b15 = tkinter.Button(root, command=bb15, image=p15,
                            relief=tkinter.FLAT, bd=0)
        b16 = tkinter.Button(root, command=bb16, image=p16,
                            relief=tkinter.FLAT, bd=0)
        b17 = tkinter.Button(root, command=bb17, image=p17,
                            relief=tkinter.FLAT, bd=0)
        b18 = tkinter.Button(root, command=bb18, image=p18,
                            relief=tkinter.FLAT, bd=0)
        b19 = tkinter.Button(root, command=bb19, image=p19,
                            relief=tkinter.FLAT, bd=0)
        b20 = tkinter.Button(root, command=bb20, image=p20,
                             relief=tkinter.FLAT, bd=0)
        #一行四个 放五行
        b1.place(x=15, y=200)
        b2.place(x=45, y=200)
        b3.place(x=75, y=200)
        b4.place(x=105, y=200)
        b5.place(x=15, y=230)
        b6.place(x=45, y=230)
        b7.place(x=75, y=230)
        b8.place(x=105, y=230)
        b9.place(x=15, y=260)
        b10.place(x=45, y=260)
        b11.place(x=75, y=260)
        b12.place(x=105, y=260)
        b13.place(x=15, y=290)
        b14.place(x=45, y=290)
        b15.place(x=75, y=290)
        b16.place(x=105, y=290)
        b17.place(x=15, y=170)
        b18.place(x=45, y=170)
        b19.place(x=75, y=170)
        b20.place(x=105, y=170)
    else:
        ee = 0
        b1.destroy()
        b2.destroy()
        b3.destroy()
        b4.destroy()
        b5.destroy()
        b6.destroy()
        b7.destroy()
        b8.destroy()
        b9.destroy()
        b10.destroy()
        b11.destroy()
        b12.destroy()
        b13.destroy()
        b14.destroy()
        b15.destroy()
        b16.destroy()
        b17.destroy()
        b18.destroy()
        b19.destroy()
        b20.destroy()

# 创建表情按钮
eBut = tkinter.Button(root, text='表情', command=express)
eBut.place(x=5, y=320, width=60, height=30)
# -----------------------------------------------------------
# extra section-snakegame and screenshot
g1 = ''
g2 = ''
g3 = ''
g4 = ''
switch = 0
# 触发视觉贪吃蛇游戏
def Game1():
    global switch
    g1.destroy()
    g2.destroy()
    g3.destroy()
    g4.destroy()
    time.sleep(0.05)
    switch = 0
    os.system('python VisionGameSnake.py')
# 触发基础贪吃蛇
def Game2():
    global switch
    g1.destroy()
    g2.destroy()
    g3.destroy()
    g4.destroy()
    time.sleep(0.05)
    switch = 0
    os.system('python basic_snake.py')

# 全屏截图
def CaptureFullScreen():
    global switch
    g1.destroy()
    g2.destroy()
    g3.destroy()
    g4.destroy()
    time.sleep(0.05)
    switch = 0
    im = ImageGrab.grab()  # 截取目标图像
    print("全屏截图成功")
    path = r"./screenshot/Fullshot.jpg"
    directory, file_name = os.path.split(path)
    while os.path.isfile(path):
        pattern = '(\d+)\)\.'
        if re.search(pattern, file_name) is None:
            file_name = file_name.replace('.', '(0).')
        else:
            current_number = int(re.findall(pattern, file_name)[-1])
            new_number = current_number + 1
            file_name = file_name.replace(f'({current_number}).', f'({new_number}).')
        path = os.path.join(directory + os.sep + file_name)
    im.save(path)
    return
# 窗口截图模块
def CaptureScreen():
    global switch
    g1.destroy()
    g2.destroy()
    g3.destroy()
    g4.destroy()
    time.sleep(0.05)
    switch = 0
    x = root.winfo_x()
    y = root.winfo_y()
    w = root.winfo_width()
    h = root.winfo_height()
    im = pyautogui.screenshot(region=[x, y, w, h])  # x,y,w,h
    print("聊天窗口截图成功")
    path1 = r"./screenshot/Winshot.jpg"
    directory1, file_name1 = os.path.split(path1)
    while os.path.isfile(path1):
        pattern = '(\d+)\)\.'
        if re.search(pattern, file_name1) is None:
            file_name1 = file_name1.replace('.', '(0).')
        else:
            current_number = int(re.findall(pattern, file_name1)[-1])
            new_number = current_number + 1
            file_name1 = file_name1.replace(f'({current_number}).', f'({new_number}).')
        path1 = os.path.join(directory1 + os.sep + file_name1)
    im.save(path1)
    return


def extra():
    global g1, g2, g3, g4, switch
    if switch == 0:
        switch = 1
        g1 = tkinter.Button(root, text='进阶游戏', command=Game1,
                            relief=tkinter.FLAT, bd=0)
        g2 = tkinter.Button(root, text='全屏截图', command=CaptureFullScreen,
                            relief=tkinter.FLAT, bd=0)
        g3 = tkinter.Button(root, text='聊天截图', command=CaptureScreen,
                            relief=tkinter.FLAT, bd=0)
        g4 = tkinter.Button(root, text='基础游戏', command=Game2,
                            relief=tkinter.FLAT, bd=0)
        g1.place(x=352, y=243)
        g2.place(x=352, y=294)
        g3.place(x=352, y=268)
        g4.place(x=352, y=217)
    else:
        switch = 0
        g1.destroy()
        g2.destroy()
        g3.destroy()
        g4.destroy()

# 创建拓展功能按钮
extraBut = tkinter.Button(root, text='拓展', command=extra)
extraBut.place(x=370, y=320, width=60, height=30)


# 文件功能代码部分
def open_choose_img():
    file_path = tkinter.filedialog.askopenfilename(title=u'选择文件')
    chat_send_file(file_path)


def chat_send_file(file_path):
    if '【群发】' not in users:
        users.append('【群发】')
    # 判断是否满足发送条件
    if not judge_send_legal():
        return
    # 告诉server 发送聊天文件
    if not os.path.isfile(file_path):
        # tkinter.messagebox.showwarning('提示', '未选择文件!')
        return
    if not os.path.exists(file_path):
        tkinter.messagebox.showwarning('提示', '选择的文件不存在!')
        return
    suffix = file_path.split(".")[-1]       # 获取文件的后缀
    file = open(file_path, "rb")      # 图片和文字的读取方法区别在于 其要用二进制方法读取
    data = file.read()
    print(type(data))
    if len(data) == 0:
        tkinter.messagebox.showwarning('提示', '选择的文件内容为空!')
        return
    # 1.获取os所在的目录
    working_path = os.getcwd()
    # 2.读取发送时的文件名
    real_file_name = ''
    real_file_name = file_name = os.path.basename(file_path)
    # 3.叠加得到新路径（文件保存路径）
    file_path = os.path.join(working_path, 'client_photos', file_name)
    send_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_data = {'type': "图片", 'from_user': user, 'to_id': chat,
                 'send_date': send_date, 'file_length': len(data),
                 'file_suffix': suffix, 'file_name': file_path, 'real_file_name': real_file_name}
    s.send(json.dumps(send_data).encode())
    time.sleep(0.5)  # 确保该消息送达
    s.sendall(data)
    file.close()


photo_button = tkinter.Button(root, text='文件', command=open_choose_img)
photo_button.place(x=70, y=320, width=60, height=30)
#---------------------------------------------------------------------
#自拍
def zipai():
    cap = cv2.VideoCapture(0)  # 打开摄像头

    while (1):
        # get a frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示
        # show a frame
        cv2.imshow("capture", frame)  # 生成摄像头窗口
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 如果按下q 就截图保存并退出
            cv2.imwrite("test.png", frame)  # 保存路径
            break

    cap.release()
    cv2.destroyAllWindows()

def show_zipai():
    global flag1
    flag1 = 0
    if flag1 == 0:
        flag1 = 1
        zipai()
        im = Image.open('./test.png')
        #im.show()
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文乱码
        plt.subplot(121)
        plt.imshow(im)
        plt.title('您的自拍')
        # 不显示坐标轴
        plt.axis('off')
        plt.show()


eeBut = tkinter.Button(root, text='自拍', command=show_zipai)
eeBut.place(x=135, y=320, width=60, height=30)

# ---------------------------------------------------------------------
#语音
def record():
    global record_sound_id
    # 定义数据流块
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    # 录音时间 8s
    RECORD_SECONDS = 8
    # 要写入的文件名
    # 处理一下音频存放路径
    record_sound_id += 1
    # 1.获取os所在的目录
    working_path = os.getcwd()
    # 3.叠加得到新路径（文件保存路径）
    tmp_file_path = os.path.join(working_path, 'client_photos', 'wav_output_'+ str(record_sound_id)+ '.wav')
    WAVE_OUTPUT_FILENAME = tmp_file_path
    # 创建PyAudio对象
    p = pyaudio.PyAudio()
    # 打开数据流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("* recording")
    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    # 停止数据流
    stream.stop_stream()
    stream.close()
    # 关闭PyAudio
    p.terminate()
    # 写入录音文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    chat_send_sound(WAVE_OUTPUT_FILENAME)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def record_sound():
    if '【群发】' not in users:
        users.append('【群发】')
    if not judge_send_legal():
        return
    global flag
    flag = 0
    if flag == 0:
        flag = 1
        record()
        time.sleep(3)
    else:
        flag = 0

eeBut = tkinter.Button(root, text='语音输入', command=record_sound)
eeBut.place(x=200, y=320, width=80, height=30)

def chat_send_sound(file_path):
    # 判断用户有没有发送消息的资格
    if '【群发】' not in users:
        users.append('【群发】')
    if not judge_send_legal():
        return
    if not os.path.exists(file_path):
        tkinter.messagebox.showwarning('提示', '音频存盘失败!')
        return
    suffix = file_path.split(".")[-1]  # 获取文件的后缀
    file = open(file_path, "rb")  # 图片和文字的读取方法区别在于 其要用二进制方法读取
    data = file.read()
    print(type(data))
    if len(data) == 0:
        tkinter.messagebox.showwarning('提示', '该音频内容为空!')
        return
    send_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_real_name = os.path.basename(file_path)
    send_data = {'type': "音频", 'from_user': user, 'to_id': chat,
                 'send_date': send_date, 'file_length': len(data),
                 'file_suffix': suffix, 'file_name': file_path, 'real_file_name': file_real_name}
    s.send(json.dumps(send_data).encode())
    time.sleep(0.5) # 确保该消息送达
    s.sendall(data)
    file.close()

#-------------------------------------------------------------------
#播放音乐
m1 = ''
m2 = ''
m3 = ''
m4 = ''
key = 0

def play_sound1():
    global flag1
    flag1 = 0
    if flag1 == 0:
        flag1 = 1
        playsound('music/Justin Bieber - Yummy.wav')
        time.sleep(3)
    else:
        flag1 = 0

def play_sound2():
    global flag2
    flag2 = 0
    if flag2 == 0:
        flag2 = 1
        playsound('music/Justin Bieber,Quavo - Intentions.wav')
        time.sleep(3)
    else:
        flag2 = 0

def play_sound3():
    global flag3
    flag3 = 0
    if flag3 == 0:
        flag3 = 1
        playsound('music/Justin Bieber - Changes.wav')
        time.sleep(3)
    else:
        flag3 = 0

def play_sound4():
    global flag4
    flag4 = 0
    if flag4 == 0:
        flag4 = 1
        playsound('music/Justin Bieber - All Around Me.wav')
        time.sleep(3)
    else:
        flag4 = 0

def extra1():
    global m1, m2, m3, m4, key
    if key == 0:
        key = 1
        m1 = tkinter.Button(root, text=' 音乐1', command=play_sound1,
                            relief=tkinter.FLAT, bd=0)
        m2 = tkinter.Button(root, text=' 音乐2', command=play_sound2,
                            relief=tkinter.FLAT, bd=0)
        m3 = tkinter.Button(root, text=' 音乐3', command=play_sound3,
                            relief=tkinter.FLAT, bd=0)
        m4 = tkinter.Button(root, text=' 音乐4', command=play_sound4,
                            relief=tkinter.FLAT, bd=0)
        m1.place(x=285, y=217, width=80, height=30)
        m2.place(x=285, y=243, width=80, height=30)
        m3.place(x=285, y=268, width=80, height=30)
        m4.place(x=285, y=294, width=80, height=30)
    else:
        key = 0
        m1.destroy()
        m2.destroy()
        m3.destroy()
        m4.destroy()

eeBut = tkinter.Button(root, text='播放音乐', command=extra1)
eeBut.place(x=285, y=320, width=80, height=30)
# ---------------------------------------------------------------------
# 创建多行文本框, 显示在线用户
listbox1 = tkinter.Listbox(root)
listbox1.place(x=445, y=0, width=130, height=320)


def showUsers():
    global listbox1, ii
    if ii == 1:
        listbox1.place(x=445, y=0, width=130, height=320)
        ii = 0
    else:
        listbox1.place_forget()  # 隐藏控件
        ii = 1

# 查看在线用户按钮
button1 = tkinter.Button(root, text='用户列表', command=showUsers)
button1.place(x=485, y=320, width=90, height=30)

# 创建输入文本框和关联变量
a = tkinter.StringVar()
a.set('')
entry = tkinter.Entry(root, width=120, textvariable=a)
entry.place(x=5, y=350, width=570, height=40)


def judge_send_legal():
    global chat, ban_flag
    if ban_flag == True:
        tkinter.messagebox.showerror('温馨提示', message='您已被禁言！')
        return False
    if chat not in users:
        tkinter.messagebox.showerror('温馨提示', message='没有聊天对象!')
        return False
    if chat == user:
        tkinter.messagebox.showerror('温馨提示', message='自己不能和自己进行对话!')
        return False
    return True


def send(*args):
    # 没有添加的话发送信息时会提示没有聊天对象
    if '【群发】' not in users:
        users.append('【群发】')
    print(chat)
    if not judge_send_legal():
        return
    mes = entry.get() + ':;' + user + ':;' + chat  # 添加聊天对象标记
    s.send(mes.encode())
    a.set('')  # 发送后清空文本框


# 创建发送按钮
button = tkinter.Button(root, text='发送', command=send)
button.place(x=515, y=353, width=60, height=30)
root.bind('<Return>', send)  # 绑定回车发送信息


# 私聊功能
def private(*args):
    global chat
    # 获取点击的索引然后得到内容(用户名)
    indexs = listbox1.curselection()
    print(indexs)
    index = indexs[0]
    if index > 0:
        chat = listbox1.get(index)
        # 修改客户端名称
        if chat == '【群发】':
            root.title(user)
            return
        ti = user + '  -->  ' + chat
        root.title(ti)


# 在显示用户列表框上设置绑定事件
listbox1.bind('<ButtonRelease-1>', private)

def open_file(event, file_path):
    dir_path = os.path.dirname(file_path)
    name = os.path.basename(file_path)
    os.system('nautilus ' + dir_path)


def handlerAdaptor(fun, **kwds):
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


# 用于时刻接收服务端发送的信息并打印
def recv():
    global users, ban_flag, link_cnt, photo_list
    while True:
        data = s.recv(1024)
        data = data.decode()
        print(type(data))
        # 没有捕获到异常则表示接收到的是在线用户列表
        try:
            data = json.loads(data)
            print(data, 1)
            if isinstance(data, list):
                users = data
                listbox1.delete(0, tkinter.END)  # 清空列表框
                number = ('   在线用户数: ' + str(len(data)))
                listbox1.insert(tkinter.END, number)
                listbox1.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
                listbox1.insert(tkinter.END, '【群发】')
                listbox1.itemconfig(tkinter.END, fg='green')
                for i in range(len(data)):
                    listbox1.insert(tkinter.END, (data[i]))
                    listbox1.itemconfig(tkinter.END, fg='green')
            if isinstance(data, dict):
                print(data, 2)
                time.sleep(0.5)  # 防止消息没送达
                if (data['to_id'] not in (user, '【群发】')) and data['from_user'] != user:
                    now_size, file_size = 0, data['file_length']
                    while now_size < file_size:
                        tmp_data = s.recv(1024)
                        now_size += len(tmp_data)
                    continue
                try:
                    file_path = data.get('file_name')
                    file_path = os.path.basename(file_path)
                    working_path = os.getcwd()
                    file_path = os.path.join(working_path, "client_photos", file_path)
                    print(file_path)
                    file_size = data.get('file_length')
                    now_size = 0
                    with open(file_path, 'wb') as f:
                        while now_size < file_size:
                            tmp_data = s.recv(1024)
                            now_size += len(tmp_data)
                            f.write(tmp_data)
                    # 设置消息title和字体
                    msg_title1 = '\n' * 2 + data['from_user'] + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【群发消息】' + '\n'
                    msg_title2 = '\n' * 2 + data['from_user'] + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【私聊消息】' + '\n'
                    listbox.my_font3 = font.Font(font=("微软雅黑", 8))
                    listbox.my_font4 = font.Font(font=("微软雅黑", 10))
                    if data['to_id'] == '【群发】' and data['from_user'] != user:
                        listbox.insert(tkinter.END, msg_title1, 'blue')  # 群发消息对其他用户显示蓝色
                        listbox.tag_configure(link_cnt, foreground='blue', underline=True)
                        listbox.insert(tkinter.END, data['real_file_name'], link_cnt)
                        link_cnt += 1
                    if data['to_id'] == user:
                        listbox.insert(tkinter.END, msg_title2, 'pink')  # 私聊消息对私聊者显示粉色
                        listbox.tag_configure(link_cnt, foreground='blue', underline=True)
                        listbox.insert(tkinter.END, '{}'.format(data['real_file_name']), link_cnt)
                        link_cnt += 1
                    if data['from_user'] == user:
                        listbox.insert(tkinter.END, msg_title1, 'blue')  # 群发和私聊消息对自己显示蓝色
                        listbox.tag_configure(link_cnt, foreground='blue', underline=True)
                        listbox.insert(tkinter.END, '{}'.format(data['real_file_name']), link_cnt)
                        link_cnt += 1
                    photo_list.append(file_path)
                    print(photo_list)
                    for i in range(len(photo_list)):
                        listbox.tag_bind(i, '<Button-1>', handlerAdaptor(open_file, file_path = photo_list[i]))
                    print("......")
                except:
                    print('failed to recv data from server!')
        except:
            if isinstance(data, dict):
                print(data, 3)
            else:
                data = data.split(':;')
                print(data)
                data1 = data[0].strip()  # 消息
                data2 = data[1]  # 发送信息的用户名
                data3 = data[2]  # 聊天对象
                markk = data1.split('：')[1]
                # 判断是不是图片
                pic = markk.split('#')
                # 判断是不是表情
                # 如果字典里有则贴图
                if (markk in dic) or pic[0] == '``':
                    if data3 == '【群发】':
                        data4 = '\n' * 2 + data2 + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【群发消息】' + '\n'
                        if data2 == user:  # 如果是自己则将则字体变为蓝色
                            listbox.insert(tkinter.END, data4, 'green')
                        else:
                            listbox.insert(tkinter.END, data4, 'blue')  # END将信息加在最后一行
                    elif data2 == user or data3 == user:  # 显示私聊
                        data4 = '\n' * 2 + data2 + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【私聊消息】' + '\n'
                        if data2 == user:
                            listbox.insert(tkinter.END, data4, 'green')  # END将信息加在最后一行
                        if data3 == user:
                            listbox.insert(tkinter.END, data4, 'pink')  # END将信息加在最后一行
                    listbox.image_create(tkinter.END, image=dic[markk])
                else:
                    data1 = '\n' + data1
                    if data3 == '【群发】':
                        data4 = '\n' * 2 + data2 + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【群发消息】' + '\n'
                        if data2 == user:  # 如果是自己则将则字体变为蓝色
                            listbox.insert(tkinter.END, data4, 'green')
                            listbox.insert(tkinter.END, data1.split("：")[-1], 'blue')
                        else:
                            listbox.insert(tkinter.END, data4, 'blue')  # END将信息加在最后一行
                            listbox.insert(tkinter.END, data1.split("：")[-1], 'blue')
                        if len(data) == 4:
                            listbox.insert(tkinter.END, '\n' + data[3], 'pink')
                    elif data2 == user or data3 == user:  # 显示私聊
                        if data1 == "\nserver：【禁言警告】" and data2 == 'server':  # 如果检测到标志信息
                            data4 = '\n' * 2 + 'server' + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【禁言警告】' + '\n'
                            ban_flag = True
                            listbox.insert(tkinter.END, data4, 'red')  # END将信息加在最后一行
                            print(data1)
                        elif data1 == "\nserver：【解禁提示】" and data2 == 'server':
                            data4 = '\n' * 2 + 'server' + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【解禁提示】' + '\n'
                            ban_flag = False
                            listbox.insert(tkinter.END, data4, 'green')  # END将信息加在最后一行
                            print(data1)
                        else:
                            data4 = '\n' * 2 + data2 + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【私聊消息】' + '\n'
                            if data2 == user:
                                listbox.insert(tkinter.END, data4, 'green')  # END将信息加在最后一行
                            if data3 == user:
                                listbox.insert(tkinter.END, data4, 'pink')  # END将信息加在最后一行
                            data1 = data1.split('：')[-1]
                            listbox.insert(tkinter.END, data1, 'blue')
                listbox.see(tkinter.END)  # 显示在最后


r = threading.Thread(target=recv)
time.sleep(1)
r.start()  # 开始线程接收信息

root.mainloop()
s.close()  # 关闭图形界面后关闭TCP连接
