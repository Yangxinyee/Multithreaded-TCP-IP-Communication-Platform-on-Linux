# 基于Linux系统的局域网聊天软件

## 设计内容

本聊天系统主要由客户端和服务器两部分组成。

（1）客户端

客户端由用户使用，负责用户间的交互，用户使用客户端登录聊天室进行聊天。

客户端具有以下功能：用户注册登录、用户输入消息、将消息发送至服务器、显示当前在线用户列表、显示当前其他用户发送的消息、发表情、发文件、自拍、语音输入、听音乐、游戏和截图等。

系统在 terminal 环境下通过输入命令python3 client.py运行。用户可以看到当前在线的所有用户，并选择群发或私发消息。

当初次打开客户端时会出现要求用户输入用户名的界面，在用户输入用户名后系统获取当前计算机的 IP 地址，并将用户名和 IP 地址发送至服务器。 当服务器发送更新当前在线用户的信息时，客户端系统需要对在线用户进行处理，更新当前在线用户的显示。客户端中需要将其他用户发送的信息显示出来，并且不断更新，本机发送的消息也将显示在用户发送的消息里。

（2）服务器端

服务器主要负责用户消息的处理和转发，所有用户消息必须经由服务器发送至其他用户。

服务器主要完成的功能有：处理用户的上线下线，保存上线用户的用户名和IP 地址，将客户端要群发的信息群发给所有用户，将客户端发送给特定用户的信息发给对应的 IP 地址以及对用户进行禁言与解禁等操作。

服务器和客户端使用 TCP 协议进行通信，同时使用特定的端口号。服务器有着固定的 IP 地址，每个客户端有不同的 IP 地址。首先需要保证服务器正在运行中，才可以处理客户的消息。用户通过客户端的界面进行操作，客户端与服务器进行通信，将要发送的聊天消息和相关信息使用 Socket 发送给服务器。服务器按照消息的发送设置（群聊、私聊等）将消息发送给特定的用户。

## 开发工具及运行环境

(1)采用 Linux 系统下的 Python 语言设计。
(2) 使用 Ubuntu 的 Linux 平台进行运行。
(3) 使用的库：
cvzone==1.5.6
numpy==1.24.2
opencv_contrib_python==4.7.0.72
pgzero==1.2.1
PyAutoGUI==0.9.53
PyQt5==5.15.9
pyscreenshot==3.0
PyAudio==0.2.13
Playsound==1.3.0
Fonttools==4. 25.0
Matplotlib==3.4.3

## 界面展示

<div align=center><img src="https://img-blog.csdnimg.cn/836b0c689f3744eb812e95995297056e.png" width="50%"></div>

<div align=center><img src="https://img-blog.csdnimg.cn/3be544b51cd54d6e9135caa6b725c301.png" width="50%"></div>

<div align=center><img src="https://img-blog.csdnimg.cn/8d1c6108ca2d4df4a56bd3c0c9030a1f.png" width="50%"></div>

<div align=center><img src="https://img-blog.csdnimg.cn/891b688bbbee47668189b7f1c7bdba68.png" width="50%"></div>

<div align=center><img src="https://img-blog.csdnimg.cn/9380716a7e5a4e4ea3103ff2875abded.png" width="50%"></div>

<div align=center><img src="https://img-blog.csdnimg.cn/13f1c9ea7006457e9451f107c1f524bb.png" width="50%"></div>

<div align=center><img src="https://img-blog.csdnimg.cn/9868daa0af274af59f0cecd98ce15d1a.png" width="50%"></div>

## 服务器设计原理

(1)实现 TCP 通信：服务器网络相交于客户端有所不同的地方在于，建立TCP 通信时，要创建一个专门的套接字绑定固定的端口和 IP 用于监听客户端的连接请求。
(2) 处理信息高效：保证服务器能同时处理接收不同客户端发来的消息，即
采取多线程的高效处理方式，保证客户端能够及时接收到消息。
(3) 保证消息的接收和发送同步：保证消息的先后顺序，即先收到的消息先
发送。
(4) 完成交互功能: 私聊功能、群聊功能、查看在线人数、禁言功能、文件转发功能。
服务器整体设计结构图：

<div align=center><img src="https://img-blog.csdnimg.cn/f378a6bfcbe24a26ae23860208795161.png" width="50%"></div>

建立 TCP 连接流程图：

<div align=center><img src="https://img-blog.csdnimg.cn/5417c2ed37d14bf080f38c7e16363fec.png" width="50%"></div>

## 客户端设计原理

(1) 用户注册：用户填写 ID 及密码信息进行注册。当用户再次确认密码输入错误或 ID 已存在时，系统返回注册错误及错误原因并要求用户重新注册。当用户正确输入情况下账户注册成功。
(2) 用户登录：用户正确填写 ID 和密码后进入功能界面。若用户密码输入错误同样得到密码错误提示并退出登录界面。在功能界面能完成以下任务：
(3) 发送表情：用户点击“表情”按钮，弹出 20 个预先绑定好的表情图片，用户点击其中一个即可发送表情。
(4) 发送文件：用户点击“文件”按钮，弹出文件窗口，用户可以在不同文件夹下选择自己想要发送的任意类型文件，双击该文件即可发送。
(5) 自拍：用户点击“自拍”按钮，即可打开摄像头，按下“ Q ”键，对当前摄像头进行捕获，并将截图保存在当前文件夹下，命名为“test.pna ”，用户可以通过选择该文件进行发送。
(6) 语音输入：用户点击“语音输入”按钮，系统便开始录音，当录音结束后，在当前文件夹下生成一个名为“output.wav ”的语音文件，并自动发送，接受用户直接点击即可播放语音。
(7) 播放音乐：用户点击“播放音乐”按钮，即可从原先存在本地的四首音乐当中选择一首进行播放，增加了聊天室的趣味性。
(8) 游戏：用户点击“拓展”按钮，将会弹出游戏选项。游戏Ⅰ为基础版游戏——像素版贪吃蛇，用户只需按“WASD ”即可控制贪吃蛇移动。游戏Ⅱ为进阶版游戏——摄像头贪吃蛇，系统将会调用本地摄像头，通过识别用户手指的移动来控制贪吃蛇的移动。
(9) 截图：用户点击“拓展”按钮，将会弹出截图选项。截图Ⅰ为当前窗口截图，截图Ⅱ为全屏截图，截下来的图将会存在专门存放截图的文件夹中。
(10) 用户列表：用户列表将会显示当前在线的所有用户，点击“用户列表”按钮，将会隐藏用户列表，再次点击“用户列表”按钮，则会再次显示用户列表。
(11) 输入与发送：用户在聊天框中输入文字后，点击右侧的“发送”按钮，即可将输入的文字通过私聊或群聊的方式发送出去。若在用户列表中点击“【群发】”，则为群聊；若点击某用户，则为私聊。
客户端架构图：

<div align=center><img src="https://img-blog.csdnimg.cn/5c7c65387a974165abc6426b0ba50de7.png" width="50%"></div>

建立 TCP 连接流程图：

<div align=center><img src="https://img-blog.csdnimg.cn/e774fc4d779646c7b6c46eedb906cd80.png" width="50%"></div>

## 系统使用方法

**(1) 配置 Python 编译环境：**

使用 Python3.8 或 3.9 均可，初次打开工程文件会自动检测到 requirements.txt 文件，依照指示安装其中的所有对应版本的库文件，或者在终端手动输入并运行命令： pip install -r requirements.txt

**(2)设置摄像头参数：**

在文件 VisionGameSnake.py 的第 15 行代码处：

将 cv2.VideoCapture() 函数中参数写为 0（如果调用内置摄像头）或者写为 1（如果调用外接摄像头）。在 zipai 函数（ client.py 文件中）中也是同样的操作。

**(3)运行服务器:**

启动后弹出的管理员界面：

<div align=center><img src="https://img-blog.csdnimg.cn/01f85a697eef4e6abbf673b47d001240.png" width="50%"></div>

**(4)运行客户端**

***ps:内置两款贪吃蛇小游戏，可以自行探索哦~***

<div align=center><img src="https://img-blog.csdnimg.cn/51c19df962014f44b9d8bbee314905f2.png" width="50%"></div>

<div align=center><img src="https://img-blog.csdnimg.cn/04a149d0649449dd9bfa4804035abd97.png" width="50%"></div>

## 软件著作权证书

<div align=center><img src="https://i.imgur.com/UwD1Plb.jpg" width="50%"></div>