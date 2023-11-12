# Development of a Multithreaded TCP/IP Communication Platform on Linux

## Content Overview

This chat system mainly consists of two parts: **Client and Server.**

**（1）Client**

The client is used by users and is responsible for the interaction between users. Users log in to the chat room using the client to chat.
The client has the following functions: user registration and login, user input messages, send messages to the server, display the current online user list, display the current message sent by other users, express emotions, send files, selfie, voice input, listen to music, games, and screenshots.

In the terminal environment, run the python3 client.py command. Users can view all online users and choose to send group or private messages.

When the client is opened for the first time, a screen is displayed asking the user to enter the user name. After the user enters the user name, the system obtains the IP address of the current computer and sends the user name and IP address to the server. When the server sends an update message about the current online user, the client system needs to process the online user and update the display of the current online user. The client needs to display the information sent by other users, and constantly updated, the message sent by the machine will also be displayed in the message sent by the user.

**（2）Server**

The server is mainly responsible for the processing and forwarding of user messages, and all user messages must be sent to other users through the server.

The main functions of the server include: processing the user online and offline, saving the user name and IP address of the online user, sending the information to be sent by the client to all users, sending the information sent by the client to a specific user to the corresponding IP address, and performing operations such as blocking and unblocking the user.

The server and the client communicate using the TCP protocol, while using a specific port number. The server has a fixed IP address, and each client has a different IP address. It is necessary to ensure that the server is running before it can process the client's messages. Users operate through the interface of the client, the client communicates with the server, and the chat messages and related information to be sent are sent to the server using the Socket. The server sends the message to a specific user according to the message delivery Settings (group chat, private chat, etc.).

## Development Tools and Environment

(1)Using Python language design under Linux system.

(2) Run on the Linux platform with Ubuntu.

(3) Libraries：

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

## Demonstrate

<img src="https://img-blog.csdnimg.cn/836b0c689f3744eb812e95995297056e.png" width="50%">

***地址 address：127.0.0.1:8888***

***昵称 user name：***

***密码 password：***

***登录Login      注册registration***

<img src="https://img-blog.csdnimg.cn/3be544b51cd54d6e9135caa6b725c301.png" width="50%">

***Registration interface***

<img src="https://img-blog.csdnimg.cn/01f85a697eef4e6abbf673b47d001240.png" width="50%">

***Admin window.***

<img src="https://img-blog.csdnimg.cn/8d1c6108ca2d4df4a56bd3c0c9030a1f.png" width="50%">

***operation of Banning to post interface and banning success prompt.***

<img src="https://img-blog.csdnimg.cn/891b688bbbee47668189b7f1c7bdba68.png" width="50%">

<img src="https://img-blog.csdnimg.cn/2e44d5ecfc394284a23b679292dd4a4e.png" width="50%">

***Welcome to the chat room!***  ***Sending emoji!***

<img src="https://img-blog.csdnimg.cn/9380716a7e5a4e4ea3103ff2875abded.png" width="50%">

<img src="https://img-blog.csdnimg.cn/13f1c9ea7006457e9451f107c1f524bb.png" width="50%">

***You can see the number of online users on the right.***

<img src="https://img-blog.csdnimg.cn/9868daa0af274af59f0cecd98ce15d1a.png" width="50%">

***【群发消息】：Group chat message  【私聊消息】：Private message***



## Principles of Server Design

**(1) Implement TCP communication:** The difference between the server network and the client is that when establishing TCP communication, a special socket is created to bind a fixed port and IP for listening to the connection request of the client.

**(2) Efficient processing of information:** ensure that the server can simultaneously process and receive messages from different clients, that is, adopt a multi-threaded efficient processing mode to ensure that the client can receive messages in time.

**(3) Ensure that messages are received and sent synchronously:** ensure the sequence of messages, that is, the first received message is sent first.

**(4) Complete interactive functions:** private chat function, group chat function, viewing online number, gag function, file forwarding function.

**Overall server design structure：**

<div align=center><img src="https://i.imgur.com/mXkFcLP.png" width="70%"></div>

**Flowchart for establishing TCP connections：**

<div align=center><img src="https://i.imgur.com/QTToTCQ.png" width="80%"></div>

## Principles of Client Design

**(1) User registration:** The user fills in the ID and password information to register. When the user reconfirms that the password is incorrect or the ID already exists, the system returns the registration error and the cause of the error and asks the user to re-register. Account registration is successful when the user enters correctly.

**(2) User login:** The user enters the function interface after correctly filling in the ID and password. If the user enters the wrong password, the user will also get a password error message and exit the login page. The following tasks can be completed on the function screen:

**(3) Send the expression:** The user clicks the "expression" button, 20 pre-bound expression pictures pop up, and the user clicks one of them to send the expression.

**(4) Send files:** The user clicks the "File" button, the file window pops up, the user can select any type of file they want to send under different folders, double-click the file to send.

**(5) Selfie:** The user can click the "selfie" button to turn on the camera, press the "Q" key, capture the current camera, and save the screenshot in the current folder, named "test.pna", the user can select the file to send.

**(6) Voice input:** When the user clicks the "voice input" button, the system will start recording. When the recording is over, a voice file named "output.wav" will be generated in the current folder and automatically sent, and the voice can be played by the user's direct click.

**(7) Play music:** Users click the "Play music" button, you can choose one of the four music that originally existed locally to play, increasing the interest of the chat room.

**(8) Games:** Users click the "Expand" button, the game option will pop up. Game I is the basic version of the game - pixel version of Snake, users only need to press "WASD" to control snake movement. Game II for the advanced version of the game - camera snake, the system will call the local camera, by recognizing the user's finger movement to control the snake's movement.

**(9) Screenshot:** When the user clicks the "Expand" button, the screenshot option will pop up. Screenshot Ⅰ is a screenshot of the current window, and screenshot Ⅱ is a full-screen screenshot. The screenshot is saved in a folder dedicated to storing snapshots.

**(10) User list:** The user list will display all users currently online, click the "User list" button, the user list will be hidden, click the "user list" button again, the user list will be displayed again.

**(11) Input and send:** After the user enters the text in the chat box, click the "send" button on the right side to send the input text through private chat or group chat. If you click "[group post]" in the user list, it is a group chat; If you click on a user, it is a private chat.

**Client architecture diagram：**

<div align=center><img src="https://i.imgur.com/qGRMdHw.png" width="80%"></div>

**Flowchart for establishing TCP connections：**

<div align=center><img src="https://i.imgur.com/1FmHPg0.png" width="80%"></div>

## Get Started

**(1) Configure the Python compilation environment：**

Python3.8 or 3.9 can be used, the first time you open the project file will automatically detect the requirements.txt file, follow the instructions to install all the corresponding versions of the library file, or manually enter and run the command from the terminal:  

```
pip install -r requirements.txt
```

**(2)Set camera parameters：**

At line 15 of the file visiongamesnaake.py:

Set the argument x in 

```
cv2.VideoCapture(x)
```

 function as 0 (if calling the built-in camera) or 1 (if calling the external camera). The same thing happens in the zipai function (in the client.py file).

**(3)Run server:**

**The administrator page that is displayed after startup：**

<div align=center><img src="https://img-blog.csdnimg.cn/01f85a697eef4e6abbf673b47d001240.png" width="50%"></div>

**(4)Run client**

***ps: The system has two built-in snake games, you can explore them on your own~***

<div align=center><img src="https://img-blog.csdnimg.cn/51c19df962014f44b9d8bbee314905f2.png" width="50%"></div>

<div align=center><img src="https://img-blog.csdnimg.cn/04a149d0649449dd9bfa4804035abd97.png" width="50%"></div>

## Chinese Software Copyright Certificate

<div align=center><img src="https://i.imgur.com/UwD1Plb.jpg" width="50%"></div>
