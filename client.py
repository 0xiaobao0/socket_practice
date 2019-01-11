# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/1/8 1:37'
import tkinter
import tkinter.font as tkFont
import socket
import threading
import json
import time
import sys
import son_window
from show_tips import show_tips

class client_gui():
    def __init__(self):
        self.connection_class = connect()
        self.connection = self.connection_class.start_connect()
        self.ord_userlist = []
        self.userlist = []
        self.private_message = {}
        self.private_chat_window_dict = {}
        self.historydata = {}
        self.chat_historydata = {}
        self.new_message = {}

        self.root = tkinter.Tk()
        self.root.title("客户端程序")

        # 窗口面板,用4个frame面板布局
        self.frame = [tkinter.Frame(), tkinter.Frame(), tkinter.Frame(), tkinter.Frame()]

        # 显示消息Text右边的滚动条
        self.display_infoScrollBar = tkinter.Scrollbar(self.frame[0])
        self.display_infoScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # 显示消息Text，并绑定上面的滚动条
        ft = tkFont.Font(family='Fixdsys', size=11)
        self.display_info = tkinter.Listbox(self.frame[0], width=70, height=18, font=ft)
        self.display_info['yscrollcommand'] = self.display_infoScrollBar.set
        self.display_info.pack(expand=1, fill=tkinter.BOTH)
        self.display_infoScrollBar['command'] = self.display_info.yview()
        self.frame[0].pack(expand=1, fill=tkinter.BOTH)

        # 显示在线用户列表右边的滚动条
        self.user_infoScrollBar = tkinter.Scrollbar(self.frame[1])
        self.user_infoScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        #在线用户列表
        ft = tkFont.Font(family='Fixdsys', size=11)
        self.user_info = tkinter.Listbox(self.frame[1], width=60, height=10, font=ft)
        self.user_info['yscrollcommand'] = self.user_infoScrollBar.set
        self.user_info.pack(expand=1, fill=tkinter.BOTH, side=tkinter.LEFT)
        self.user_infoScrollBar['command'] = self.user_info.yview()

        # 操作列表
        ft2 = tkFont.Font(family='Fixdsys', size=11)
        chat_bottem = tkinter.Button(self.frame[1], text="私聊", command=self.chat_with, width=10)
        chat_bottem.pack()
        self.frame[1].pack(expand=1, fill=tkinter.BOTH)

        # 输入消息Text的滚动条
        self.message_inputScrollBar = tkinter.Scrollbar(self.frame[2])
        self.message_inputScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # 输入消息Text，并与滚动条绑定
        ft = tkFont.Font(family='Fixdsys', size=11)
        self.message_input = tkinter.Text(self.frame[2], width=70, height=8, font=ft)
        self.message_input['yscrollcommand'] = self.message_inputScrollBar.set
        self.message_input.bind('<Key-Return>', self.send_message)
        self.message_input.pack(expand=1, fill=tkinter.BOTH)
        self.message_inputScrollBar['command'] = self.display_info.yview()
        self.frame[2].pack(expand=1, fill=tkinter.BOTH)

        # 发送消息按钮
        self.sendButton = tkinter.Button(self.frame[3], text=' 发 送 ', width=10, command=self.send_message)
        self.sendButton.pack(expand=1, side=tkinter.BOTTOM and tkinter.RIGHT, padx=25, pady=5)

        # 关闭按钮
        self.closeButton = tkinter.Button(self.frame[3], text=' 关 闭 ', width=10, command=self.close)
        self.closeButton.pack(expand=1, side=tkinter.RIGHT, padx=25, pady=5)
        self.frame[3].pack(expand=1, fill=tkinter.BOTH)

    def display_private_message(self, user):
        try:
            for message in self.new_message[tuple(user)]:
                show_tips(self.private_chat_window_dict[tuple(user)].son_display_info,
                          self.pre_time_(), '用户:{0}:{1}'.format(user, message), '').show()
            self.new_message[tuple(user)] = []
        except Exception as e:
            print('显示消息出错')

    def create_display_window(self, user):
        print('创建窗口对象')
        # print(chat_data)
        self.private_chat_window_dict[tuple(user)] = son_window.window(self.connection, user)
        window_class = self.private_chat_window_dict[tuple(user)]
        new_window = window_class.son_window
        new_window.title('用户:{0}'.format(user))
        try:
            for message in self.chat_historydata[tuple(user)]:
                # window_class.son_display_info.insert('end', self.pre_time_())
                window_class.son_display_info.insert('end', message)
                # window_class.son_display_info.insert('end', '')
        except:
            pass
        new_window.mainloop()

    def chat_with(self):
        # print(self.private_message)
        try:
            user_index = self.user_info.curselection()[0] - 1
            user = self.userlist[user_index]
            if (tuple(user) == self.connection.getsockname()):
                show_tips(self.display_info, self.pre_time_(), '请选择非自己的私聊的对象', '').show()
            else:
                try:
                    chat_data = list(self.private_chat_window_dict[tuple(user)].chat_data)
                    print('之前窗口的消息记录为:{0}'.format(chat_data))
                    # 若读到了该用户的历史数据，将其放入对应的历史数据list
                    try:
                        self.chat_historydata[tuple(user)] = chat_data + self.new_message[tuple(user)]
                        print('更新历史聊天记录为:{0}'.format(self.chat_historydata[tuple(user)]))
                        self.new_message[tuple(user)] = []
                    except:
                        self.chat_historydata[tuple(user)] = chat_data
                    self.create_display_window(user)
                except Exception as e:
                    self.create_display_window(user)

        except Exception as e:
            # print(e)
            show_tips(self.display_info, self.pre_time_(), '请选择私聊的对象', '').show()

    def pre_time_(self):
        pre_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return pre_time

    def close(self):
        sys.exit()

    def send_message(self, *event):
        # self.display_info.insert('end', 'test')
        try:
            message = self.message_input.get('1.0', tkinter.END)
            message_length = len(message)
            self.message_input.delete('1.0', tkinter.END)
            self.connection.send(message.encode())
            show_tips(self.display_info, self.pre_time_(), '{0}: {1}'.format('我', message), '').show()
        except Exception as e:
            show_tips(self.display_info, self.pre_time_(), '发送消息失败，请重试', '').show()
            print(e)

    def dispaly_message(self):
        self.user_info.insert('end', '已连接的用户:')
        try:
            s = self.connection
            # self.display_info.insert('end', '{0}:{1}'.format(self.connection_class.host, 'test'))
            while True:
                receive_message = json.loads(s.recv(1024).decode())
                if(len(receive_message) == 3):
                    sender = receive_message['sender']
                    message = receive_message['message']
                    # self.new_message[tuple(sender)] = []
                    try:
                        self.private_message[tuple(sender)].append(message) #尝试在私聊字典中找到该用户的私聊列表，并将新的消息加入到这个列表
                        try:
                            if (self.private_chat_window_dict[tuple(sender)].flag == True): #如果通过选中用户创建了该用户的窗体类
                                print('用户已开启窗口')
                                try:
                                    self.new_message[tuple(sender)].append(message)
                                    print('新消息为:'.format(self.new_message[tuple(sender)]))
                                except:
                                    self.new_message[tuple(sender)] = [message]
                                self.display_private_message(sender)
                                # print(self.private_chat_window_dict[tuple(sender)])
                            else:
                                print('非第一次接收私聊消息，窗口激活过，现已关闭')
                                show_tips(self.display_info, self.pre_time_(), '收到用户:{0}一条私聊消息(如需回复，选中用户点击私聊): '.format(sender), '').show()
                                # print('尝试加入的消息为:{0}'.format(message))
                                # print('现在的消息列表为{0}'.format(self.private_message[tuple(sender)]))
                                # self.chat_historydata[tuple(sender)] = self.private_message[tuple(sender)]
                                try:
                                    self.new_message[tuple(sender)].append('{0}'.format(self.pre_time_()))
                                    self.new_message[tuple(sender)].append('用户:{0}:{1}'.format(sender, message))
                                    self.new_message[tuple(sender)].append('')
                                    # print('新消息为:'.format(self.new_message[tuple(sender)]))
                                except:
                                    self.new_message[tuple(sender)] = []
                                    self.new_message[tuple(sender)].append('{0}'.format(self.pre_time_()))
                                    self.new_message[tuple(sender)].append('用户:{0}:{1}'.format(sender, message))
                                    self.new_message[tuple(sender)].append('')
                                print('新数据为{0}'.format(self.new_message[tuple(sender)]))

                        except: #如果未选中用户创建该用户的窗体类
                            print('非第一次接收消息，用户任未点开私聊按钮')
                            show_tips(self.display_info, self.pre_time_(), '收到用户:{0}一条私聊消息(如需回复，选中用户点击私聊): '.format(sender), '').show()
                            # print(self.chat_historydata[tuple(sender)])
                            self.chat_historydata[tuple(sender)] = []
                            for msg in self.private_message[tuple(sender)]:
                                self.chat_historydata[tuple(sender)].append('{0}'.format(self.pre_time_()))
                                self.chat_historydata[tuple(sender)].append('用户:{0}:{1}'.format(sender, msg))
                                self.chat_historydata[tuple(sender)].append('')
                            # print(self.chat_historydata[tuple(sender)])
                    except Exception as e:  #如果尝试失败，则在用户私聊消息字典中新建该用户的私聊消息列表，并将新消息加入，同时初始化对应用户历史消息列表为空
                        self.private_message[tuple(sender)] = []
                        self.private_message[tuple(sender)].append(message)
                        self.historydata[tuple(sender)] = []
                        # print(self.private_message[tuple(sender)])
                        try:
                            if (self.private_chat_window_dict[tuple(sender)].flag == True): #之前创建了对应用户的窗体类，但是未创建对应用户的消息类
                                print('第一次收到私聊消息，用户已经点击过私聊按钮')
                                try:
                                    self.new_message[tuple(sender)].append(message)
                                    print('新消息为:'.format(self.new_message[tuple(sender)]))
                                except:
                                    self.new_message[tuple(sender)] = [message]
                                self.display_private_message(sender)
                            else:   #不存在未创建消息类的情况下将窗口关闭的情况。
                                print('程序不会走到这')
                        except:
                            print('第一次收到私聊消息，用户还未点击过私聊按钮')     #既未创建对应用户窗体类，又未创建对应用户消息类
                            show_tips(self.display_info, self.pre_time_(),'收到用户:{0}一条私聊消息(如需回复，选中用户点击私聊): '.format(sender), '').show()
                            # self.chat_historydata[tuple(sender)] = self.private_message[tuple(sender)]
                            self.chat_historydata[tuple(sender)] = []
                            # for msg in self.private_message[tuple(sender)]:
                            self.chat_historydata[tuple(sender)].append('{0}'.format(self.pre_time_()))
                            self.chat_historydata[tuple(sender)].append('用户:{0}:{1}'.format(sender, message))
                            self.chat_historydata[tuple(sender)].append('')
                            # print(self.chat_historydata[tuple(sender)])


                if(len(receive_message) == 2):
                    sender = receive_message['sender']
                    message = receive_message['message']
                    if (sender == '服务器'):
                        show_tips(self.display_info, self.pre_time_(), '{0}: {1}'.format(sender, message), '').show()
                    else:
                        show_tips(self.display_info, self.pre_time_(), '用户: {0}: {1}'.format(sender, message), '').show()
                if(len(receive_message) == 1):
                    users = receive_message['users']
                    if(len(self.userlist) <= len(users)):
                        #每次有新加入用户就将他加入到用户列表中，并且更新userlist
                        new_users = [u for u in users if u not in self.userlist]
                        for user in new_users:
                            if(tuple(user) == self.connection.getsockname()):
                                self.user_info.insert('end', '我 :{0}'.format(user))
                            else:
                                self.user_info.insert('end', '用户 :{0}'.format(user))
                        self.ord_userlist = self.userlist
                        self.userlist = users
                    if (len(self.userlist) >= len(users)):
                        # 每次有离线用户时在用户列表中删除离线用户，并且更新userlist
                        logout_users = [u for u in self.userlist if u not in users]
                        for user in logout_users:
                            self.user_info.delete(self.userlist.index(user)+1)
                        self.ord_userlist = self.userlist
                        self.userlist = users

        except Exception as e:
            show_tips(self.display_info, self.pre_time_(),  '连接服务器失败，请重试', '').show()
            self.user_info.delete(1, tkinter.END)
            print(e)

    def startNewThread(self):
        t = threading.Thread(target=self.dispaly_message, args=())
        t.setDaemon(True)
        t.start()

class connect():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8099
    def start_connect(self):
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
            connection.connect((self.host, self.port))
            return connection
        except Exception as  e:
            print(e)

def main():
    gui = client_gui()
    gui.startNewThread()
    tkinter.mainloop()

if __name__ == '__main__':
    main()