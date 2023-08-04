import socket
import threading
import json
import tkinter as tk
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText  # Import the package used for multi-line text boxes
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
listbox1 = ''  # A list box for displaying online users
ii = 0  # Used to determine whether to open or close a list box
users = []  # List of online users
chat = '【群发】'  # Chat object, the default is group chat
ban_flag = False
photos = []
link_cnt = 0 # Used for link binding counts
photo_list = [] # Used to map image files
record_sound_id = 0 # Record the current number of recordings for file generation


class log:  # This is the login page
    def __init__(self, window):
        self.window = window
        # Login window initial position and length, width, height and background Settings
        self.window.title("聊天登录窗口") # "Login Window"
        self.sw = self.window.winfo_screenwidth()
        self.sh = self.window.winfo_screenheight()
        self.w = 400
        self.h = 500
        self.x = (self.sw - self.w) / 2
        self.y = (self.sh - self.h) / 2
        self.window.geometry("%dx%d+%d+%d" % (self.w, self.h, self.x, self.y))
        self.window.resizable(0, 0)
        # Picture, can be edited by yourself
        self.loggin_benner = Image.open('aikun.png')
        self.loggin_benner = self.loggin_benner.resize((400, 300))
        self.login_benner = ImageTk.PhotoImage(self.loggin_benner)
        self.imgLabel = tk.Label(self.window, image=self.login_benner)
        self.imgLabel.place(x=0, y=0)
        # Adjust font
        self.window.my_font1 = font.Font(family="微软雅黑", size=12, weight=font.BOLD)
        self.window.my_font2 = font.Font(family="Times New Roman", size=12)
        self.window.my_font3 = font.Font(family="华光胖头鱼_CNKI", size=8)
        # Label address; The user; cipher
        tk.Label(self.window, text="地 址:", font=self.window.my_font1).place(x=80, y=320)
        tk.Label(self.window, text="昵 称：", font=self.window.my_font1).place(x=80, y=360)
        tk.Label(self.window, text="密 码：", font=self.window.my_font1).place(x=80, y=400)
        # Text box & address
        self.IP1 = tk.StringVar()
        self.IP1.set('127.0.0.1:8888')  # ip and port are displayed by default
        self.entryIP = tk.Entry(self.window, textvariable=self.IP1, font=self.window.my_font2)
        self.entryIP.place(x=140, y=320)
        # Text box & user name
        self.User = tk.StringVar()
        self.User.set('')
        self.entryUser = tk.Entry(self.window, textvariable=self.User, font=self.window.my_font2)
        self.entryUser.place(x=140, y=360)
        # Text box & password
        self.Passwd = tk.StringVar()
        self.Passwd.set('')
        self.entryPasswd = tk.Entry(self.window, textvariable=self.Passwd, show="●")
        self.entryPasswd.place(x=140, y=400)
        # log in
        window.bind('<Return>', self.login)  # Enter Bind the login function
        self.button = tk.Button(self.window, text="登录", command=self.login, font=self.window.my_font1)
        self.button.place(x=100, y=440)
        self.button1 = tk.Button(self.window, text="注册", command=self.change, font=self.window.my_font1)
        self.button1.place(x=230, y=440)
        # reminder tag
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
        IP, PORT = self.entryIP.get().split(':')  # Obtain the IP address and port number
        passwd = self.entryPasswd.get()  # Get password
        # MD5 encryption algorithm
        passwd = MD5.gen_md5(passwd)
        PORT = int(PORT)  # The port number must be an int
        user = self.entryUser.get()
        if not user:
            tkinter.messagebox.showerror('温馨提示', message='请输入任意的用户名！') # 'Reminder ', message=' Please enter any user name! '
        else:
            # Check that the user name and password are correct
            if not self.check_user(user, passwd):
                tkinter.messagebox.showerror('温馨提示', message='请输入正确的密码！') # 'Warm reminder ', message=' Please enter the correct password! '
            else:
                self.window.destroy()  # close the window


class register:  # This is the registration page
    def __init__(self, window):
        self.window = window
        # Registration window
        self.window.title("注册")
        self.window.geometry("300x140+605+320")
        self.window.resizable(0, 0)  # Limit window size
        self.User = tkinter.StringVar()
        self.User.set('')
        self.Passwd = tkinter.StringVar()
        self.Passwd.set('')
        self.ConfPasswd = tkinter.StringVar()
        self.ConfPasswd.set('')
        # User name tag
        self.labelUser = tkinter.Label(window, text='用户名')
        self.labelUser.place(x=20, y=10, width=100, height=20)
        self.entryUser = tkinter.Entry(window, width=80, textvariable=self.User)
        self.entryUser.place(x=120, y=10, width=130, height=20)
        # password tag
        self.labelPasswd = tkinter.Label(window, text='密码')
        self.labelPasswd.place(x=30, y=40, width=80, height=20)
        self.entryPasswd = tkinter.Entry(window, width=80, textvariable=self.Passwd)
        self.entryPasswd.place(x=120, y=40, width=130, height=20)
        # Confirm password tag
        self.labelconPasswd = tkinter.Label(window, text='确认密码')
        self.labelconPasswd.place(x=30, y=70, width=80, height=20)
        self.entryconPasswd = tkinter.Entry(window, width=80, textvariable=self.ConfPasswd)
        self.entryconPasswd.place(x=120, y=70, width=130, height=20)
        # button
        self.window.bind('<Return>', self.regi)
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
        # MD5 encryption algorithm
        passwd = MD5.gen_md5(passwd)
        conpasswd = self.entryconPasswd.get()
        conpasswd = MD5.gen_md5(conpasswd)
        try:
            with open("data/user.txt", 'r', encoding="utf-8") as user_data:
                is_user = True
                for line in user_data:
                    line = line.replace("\n", "")
                    if is_user and line == user:
                        # The user name has been registered
                        return 1
                    is_user = not is_user
            # Add User and Password (md5)
            if conpasswd == passwd:
                with open("data/user.txt", 'a', encoding="utf-8") as user_data:
                    user_data.write(user + "\n")
                    user_data.write(passwd + "\n")
                    # registered successfully
                    print("register: user: " + user + ", key: " + passwd)
                return 2
            else:
                tkinter.messagebox.showerror('温馨提示', message='两次输入的密码不一致！') # 'Warm reminder ', message=' The two entered passwords do not match! '

        except Exception as e:
            print("Error adding user data:" + str(e))
            return False

    def regi(self):
        flag = self.check_regi()
        if flag == 1:
            tkinter.messagebox.showerror('温馨提示', message='该用户名已被注册，请重新输入！') # 'Warm reminder ', message=' The user name has been registered, please re-enter! '
        elif flag == 2:
            # 注册成功，返回登录页面
            tkinter.messagebox.showinfo('温馨提示', '注册成功！') # 'Warm tips ',' Registration successful! '
            self.button.destroy()
            log(root)

root = tk.Tk()
p1 = log(root)  # These two sheets can be run separately
root.mainloop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))  # Establish a connection with the corresponding port. Run the connect function to send connection requests to the IP address and port of the server

if user:
    s.send(user.encode())  # Send username
else:
    s.send('no'.encode())  # no is marked if no user name is entered

# If there is no user name, set the ip and port number to the user name
addr = s.getsockname()  # Obtain the client ip address and port number
addr = addr[0] + ':' + str(addr[1])
if user == '':
    user = addr
print(user)
# chat window
# Create a graphical interface
root = tkinter.Tk()
root.title(user)  # The window name is user name
root['height'] = 400
root['width'] = 580
root.resizable(0, 0)  # Limit window size

# Create a multiline text box
listbox = ScrolledText(root)
listbox.place(x=5, y=0, width=570, height=320)
# The font color used by the text box
listbox.tag_config('red', foreground='red')
listbox.tag_config('blue', foreground='blue')
listbox.tag_config('green', foreground='green')
listbox.tag_config('pink', foreground='pink')
listbox.insert(tkinter.END, '欢迎加入聊天室 ！', 'blue')

# Expression function code part
# Use global variables for easy creation and destruction
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
# Open the image and store it in a variable
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
# Use the dictionary to correspond the mark to the expression picture one by one, which is used to judge the expression map after receiving the mark
dic = {'doge': p1, 'OK': p2, '保佑': p3, '偷笑': p4, '傲娇': p5, '再见': p6, '加油': p7, '口罩': p8,
       '吃瓜': p9, '吐': p10, '吓': p11, '呆': p12, '呲牙': p13, '哈哈': p14, '哈欠': p15, '响指': p16,
       '哦呼': p17, '哭泣': p18, '喜极而泣': p19, '喜欢': p20}
ee = 0  # Determine the logo of the emoticon panel switch


# A function that sends emoticons to be called during button click events
def mark(exp):  # The parameter is the emoji sent mark, and the button will be destroyed after sending
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

# emoji
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
        # There are five lines in a row of four
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

# Create emoticon button
eBut = tkinter.Button(root, text='表情', command=express)
eBut.place(x=5, y=320, width=60, height=30)
# -----------------------------------------------------------
# extra section-snakegame and screenshot
g1 = ''
g2 = ''
g3 = ''
g4 = ''
switch = 0

# Trigger visual snake game
def Game1():
    global switch
    g1.destroy()
    g2.destroy()
    g3.destroy()
    g4.destroy()
    time.sleep(0.05)
    switch = 0
    os.system('python VisionGameSnake.py')
    
# Trigger base greedy snake
def Game2():
    global switch
    g1.destroy()
    g2.destroy()
    g3.destroy()
    g4.destroy()
    time.sleep(0.05)
    switch = 0
    os.system('python basic_snake.py')

# Full screen capture
def CaptureFullScreen():
    global switch
    g1.destroy()
    g2.destroy()
    g3.destroy()
    g4.destroy()
    time.sleep(0.05)
    switch = 0
    im = ImageGrab.grab()  # Capture the target image
    print("The full screen capture succeeded. Procedure")
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

# Screenshot module
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
    print("The screenshot of the chat window succeeded")
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
        g1 = tkinter.Button(root, text='进阶游戏', command=Game1, # Advanced game
                            relief=tkinter.FLAT, bd=0)
        g2 = tkinter.Button(root, text='全屏截图', command=CaptureFullScreen, # Full screen capture
                            relief=tkinter.FLAT, bd=0)
        g3 = tkinter.Button(root, text='聊天截图', command=CaptureScreen, # Chat screenshot
                            relief=tkinter.FLAT, bd=0)
        g4 = tkinter.Button(root, text='基础游戏', command=Game2, # Basic game
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

# Create an extension button
extraBut = tkinter.Button(root, text='拓展', command=extra)
extraBut.place(x=370, y=320, width=60, height=30)


# File function code part
def open_choose_img():
    file_path = tkinter.filedialog.askopenfilename(title=u'选择文件')
    chat_send_file(file_path)


def chat_send_file(file_path):
    if '【群发】' not in users:
        users.append('【群发】')
    # Check whether the sending conditions are met
    if not judge_send_legal():
        return
    # Tell the server to send the chat file
    if not os.path.isfile(file_path):
        # tkinter.messagebox.showwarning('提示', '未选择文件!') # 'Hint ',' No file selected! '
        return
    if not os.path.exists(file_path):
        tkinter.messagebox.showwarning('提示', '选择的文件不存在!') # 'Hint ',' The selected file does not exist! '
        return
    suffix = file_path.split(".")[-1]       # Gets the file suffix
    file = open(file_path, "rb")      # The difference between the reading method of pictures and text is that they are to be read by binary method
    data = file.read()
    print(type(data))
    if len(data) == 0:
        tkinter.messagebox.showwarning('提示', '选择的文件内容为空!') # 'Hint ',' The selected file content is empty! '
        return
    # 1.Gets the directory where the os is located
    working_path = os.getcwd()
    # 2.Read the file name at the time of sending
    real_file_name = ''
    real_file_name = file_name = os.path.basename(file_path)
    # 3.Overlay to get a new path (file save path)
    file_path = os.path.join(working_path, 'client_photos', file_name)
    send_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_data = {'type': "图片", 'from_user': user, 'to_id': chat,
                 'send_date': send_date, 'file_length': len(data),
                 'file_suffix': suffix, 'file_name': file_path, 'real_file_name': real_file_name}
    s.send(json.dumps(send_data).encode())
    time.sleep(0.5)  # Ensure that the message is delivered
    s.sendall(data)
    file.close()


photo_button = tkinter.Button(root, text='文件', command=open_choose_img)
photo_button.place(x=70, y=320, width=60, height=30)
#---------------------------------------------------------------------
#自拍
def zipai():
    cap = cv2.VideoCapture(0)

    while (1):
        # get a frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # The camera is opposed to people, and the image is switched back to normal display
        # show a frame
        cv2.imshow("capture", frame)  # Generate camera window
        if cv2.waitKey(1) & 0xFF == ord('q'):  # If you press q to save the screenshot and exit
            cv2.imwrite("test.png", frame)  # save path
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
        plt.rcParams['font.sans-serif'] = ['SimHei']  # unidentifiable Chinese code
        plt.subplot(121)
        plt.imshow(im)
        plt.title('Your selfie')
        # Do not display coordinate axes
        plt.axis('off')
        plt.show()


eeBut = tkinter.Button(root, text='自拍', command=show_zipai)
eeBut.place(x=135, y=320, width=60, height=30)

# ---------------------------------------------------------------------
# Recording module
def record():
    global record_sound_id
    # Define a block of data flow
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    # Recording time 5s
    RECORD_SECONDS = 5
    # The file name to write to
    # Do something about the audio storage path
    record_sound_id += 1
    # 1.Gets the directory where the os is located
    working_path = os.getcwd()
    # 3.Overlay to get a new path (file save path)
    tmp_file_path = os.path.join(working_path, 'client_photos', 'wav_output_'+ str(record_sound_id)+ '.wav')
    WAVE_OUTPUT_FILENAME = tmp_file_path
    # Create a PyAudio object
    p = pyaudio.PyAudio()
    # Open data stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("* recording")
    # Start recording
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    # Stop data flow
    stream.stop_stream()
    stream.close()
    # Close PyAudio
    p.terminate()
    # Write to recording file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    chat_send_sound(WAVE_OUTPUT_FILENAME)

# Read file
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
    # Determine whether the user is qualified to send messages
    if '【群发】' not in users:
        users.append('【群发】')
    if not judge_send_legal():
        return
    if not os.path.exists(file_path):
        tkinter.messagebox.showwarning('提示', '音频存盘失败!') # 'Prompt ',' Audio save failed! '
        return
    suffix = file_path.split(".")[-1]  # Gets the file suffix
    file = open(file_path, "rb")  # The difference between the reading method of pictures and text is that they are to be read by binary method
    data = file.read()
    print(type(data))
    if len(data) == 0:
        tkinter.messagebox.showwarning('提示', '该音频内容为空!') # 'Hint ',' The audio content is empty! '
        return
    send_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_real_name = os.path.basename(file_path)
    send_data = {'type': "音频", 'from_user': user, 'to_id': chat,
                 'send_date': send_date, 'file_length': len(data),
                 'file_suffix': suffix, 'file_name': file_path, 'real_file_name': file_real_name}
    s.send(json.dumps(send_data).encode())
    time.sleep(0.5) # Ensure that the message is delivered
    s.sendall(data)
    file.close()

#-------------------------------------------------------------------
# play music
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
# Create a multi-line text box to display online users
listbox1 = tkinter.Listbox(root)
listbox1.place(x=445, y=0, width=130, height=320)


def showUsers():
    global listbox1, ii
    if ii == 1:
        listbox1.place(x=445, y=0, width=130, height=320)
        ii = 0
    else:
        listbox1.place_forget()  # Hide button
        ii = 1

# View the online user button
button1 = tkinter.Button(root, text='用户列表', command=showUsers)
button1.place(x=485, y=320, width=90, height=30)

# Create input text boxes and associated variables
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
    # If no added message is sent, the message will indicate that there is no chat partner
    if '【群发】' not in users:
        users.append('【群发】')
    print(chat)
    if not judge_send_legal():
        return
    mes = entry.get() + ':;' + user + ':;' + chat  # Add the chat object tag
    s.send(mes.encode())
    a.set('')  # Clear the text box after sending


# Create send button
button = tkinter.Button(root, text='发送', command=send)
button.place(x=515, y=353, width=60, height=30)
root.bind('<Return>', send)  # Bind ENTER to send information


# Private chat function
def private(*args):
    global chat
    # Get the index of the click and get the content (user name)
    indexs = listbox1.curselection()
    print(indexs)
    index = indexs[0]
    if index > 0:
        chat = listbox1.get(index)
        # Example Change the client name
        if chat == '【群发】':
            root.title(user)
            return
        ti = user + '  -->  ' + chat
        root.title(ti)


# Set the binding event on the Display User list box
listbox1.bind('<ButtonRelease-1>', private)

def open_file(event, file_path):
    dir_path = os.path.dirname(file_path)
    name = os.path.basename(file_path)
    os.system('nautilus ' + dir_path)


def handlerAdaptor(fun, **kwds):
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


# It is used to receive and print the information sent by the server at any time
def recv():
    global users, ban_flag, link_cnt, photo_list
    while True:
        data = s.recv(1024)
        data = data.decode()
        print(type(data))
        # If no exception is caught, the online user list is received
        try:
            data = json.loads(data)
            print(data, 1)
            if isinstance(data, list):
                users = data
                listbox1.delete(0, tkinter.END)  # Clear list box
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
                time.sleep(0.5)  # Prevent messages from not arriving
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
                    # Set the message title and font
                    msg_title1 = '\n' * 2 + data['from_user'] + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【群发消息】' + '\n'
                    msg_title2 = '\n' * 2 + data['from_user'] + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【私聊消息】' + '\n'
                    listbox.my_font3 = font.Font(font=("微软雅黑", 8))
                    listbox.my_font4 = font.Font(font=("微软雅黑", 10))
                    if data['to_id'] == '【群发】' and data['from_user'] != user:
                        listbox.insert(tkinter.END, msg_title1, 'blue')  # Group messages are displayed in blue to other users
                        listbox.tag_configure(link_cnt, foreground='blue', underline=True)
                        listbox.insert(tkinter.END, data['real_file_name'], link_cnt)
                        link_cnt += 1
                    if data['to_id'] == user:
                        listbox.insert(tkinter.END, msg_title2, 'pink')  # Private chat messages show pink to private chat users
                        listbox.tag_configure(link_cnt, foreground='blue', underline=True)
                        listbox.insert(tkinter.END, '{}'.format(data['real_file_name']), link_cnt)
                        link_cnt += 1
                    if data['from_user'] == user:
                        listbox.insert(tkinter.END, msg_title1, 'blue')  # Group and private messages show blue to yourself
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
                data1 = data[0].strip()  # message
                data2 = data[1]  # The user name for sending the message
                data3 = data[2]  # Chat partner
                markk = data1.split('：')[1]
                # Determine whether it is a picture
                pic = markk.split('#')
                # Judge whether it is an expression
                # If there are stickers in the dictionary
                if (markk in dic) or pic[0] == '``':
                    if data3 == '【群发】':
                        data4 = '\n' * 2 + data2 + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【群发消息】' + '\n'
                        if data2 == user:  # If it is yourself, the font will turn blue
                            listbox.insert(tkinter.END, data4, 'green')
                        else:
                            listbox.insert(tkinter.END, data4, 'blue')  # END Adds the information to the last line
                    elif data2 == user or data3 == user:  # Display private chat
                        data4 = '\n' * 2 + data2 + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【私聊消息】' + '\n'
                        if data2 == user:
                            listbox.insert(tkinter.END, data4, 'green')  # END Adds the information to the last line
                        if data3 == user:
                            listbox.insert(tkinter.END, data4, 'pink')  # END Adds the information to the last line
                    listbox.image_create(tkinter.END, image=dic[markk])
                else:
                    data1 = '\n' + data1
                    if data3 == '【群发】':
                        data4 = '\n' * 2 + data2 + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【群发消息】' + '\n'
                        if data2 == user:  # If it is yourself, the font will turn blue
                            listbox.insert(tkinter.END, data4, 'green')
                            listbox.insert(tkinter.END, data1.split("：")[-1], 'blue')
                        else:
                            listbox.insert(tkinter.END, data4, 'blue')  # END Adds the information to the last line
                            listbox.insert(tkinter.END, data1.split("：")[-1], 'blue')
                        if len(data) == 4:
                            listbox.insert(tkinter.END, '\n' + data[3], 'pink')
                    elif data2 == user or data3 == user:  # Display private chat
                        if data1 == "\nserver：【禁言警告】" and data2 == 'server':  # If flag information is detected
                            data4 = '\n' * 2 + 'server' + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【禁言警告】' + '\n'
                            ban_flag = True
                            listbox.insert(tkinter.END, data4, 'red')  # END Adds the information to the last line
                            print(data1)
                        elif data1 == "\nserver：【解禁提示】" and data2 == 'server':
                            data4 = '\n' * 2 + 'server' + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【解禁提示】' + '\n'
                            ban_flag = False
                            listbox.insert(tkinter.END, data4, 'green')  # END Adds the information to the last line
                            print(data1)
                        else:
                            data4 = '\n' * 2 + data2 + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '【私聊消息】' + '\n'
                            if data2 == user:
                                listbox.insert(tkinter.END, data4, 'green')  # END Adds the information to the last line
                            if data3 == user:
                                listbox.insert(tkinter.END, data4, 'pink')  # END Adds the information to the last line
                            data1 = data1.split('：')[-1]
                            listbox.insert(tkinter.END, data1, 'blue')
                listbox.see(tkinter.END)  # Show at the end


r = threading.Thread(target=recv)
time.sleep(1)
r.start()  # The start thread receives information

root.mainloop()
s.close()  # Close the GUI and then close the TCP connection
