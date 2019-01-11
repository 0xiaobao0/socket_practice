# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/1/8 1:37'
import tkinter
import tkinter.font as tkFont
import socket
import threading
import json
import sys
import time
from show_tips import show_tips



class server_gui():
    def __init__(self):
        self.server_class = server()    #窗体类服务器对象，这种写法在窗体类创建时自动创建服务类
        self.server = self.server_class.start_server()  #窗体类创建时制动执行服务类中的start_server方法
        self.connection_dict = {}   #客户端连接字典，key为客户端(ip, 端口)组成的元组，value为服务端与对应客户端的socket对象

        # 窗体类绘制过程
        self.root = tkinter.Tk()
        self.root.title("服务端程序")

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
        logout_user_bottem = tkinter.Button(self.frame[1], text="强制下线", command=self.log_out_user, width=10)
        logout_user_bottem.pack()
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
        self.message_input.bind('<Key-Return>', self.send_message)  #绑定发送快捷键为回车，若敲击回车执行send_message函数
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

    # 显示当前时间函数
    def pre_time_(self):
        pre_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return pre_time

    # 终止主线程函数
    def close(self):
        sys.exit()

    # 强行下线函数
    def log_out_user(self):
        try:
            # print(self.connection_dict)
            user_index = self.user_info.curselection()[0] - 1   #在listbox组件中找到用户的索引
            user_address_list = [address for address in list(self.connection_dict.keys())]  #客户端连接字典中的key列表
            user_client = self.connection_dict[user_address_list[user_index]]   #用上面的索引和列表找到对应的哟用户socket对象
            user_client.close() #关闭该socket对象
            # self.connection_dict.pop(user_address[user_index])
            # print(self.connection_dict)
        except Exception as e:
            print(e)
            show_tips(self.display_info, self.pre_time_(), '当前操作失败，请选择左侧窗体的用户', '').show()  #若未选中用户的提示信息



    def chat_with(self):
        show_tips(self.display_info, self.pre_time_(), '该部分暂未写完', '').show()    #未写完提示信息

    def private_chat(self, son_window): #暂未写完
        pass

    # 发送消息函数，该函数用于服务器自身在窗口发送信息
    def send_message(self, *event):
        # self.display_info.insert('end', 'test')
        try:
            data = self.message_input.get('1.0', tkinter.END)   #获取输入栏中用户的输入信息
            data_length = len(data) #获取输入信息长度
            self.message_input.delete('1.0', tkinter.END)   #获取万必要信息后清空输入栏
            #对所有用户发送信息
            for connection in self.connection_dict: #遍历连接字典，只取其中的key
                message = {}
                message['sender'] = '服务器'
                message['message'] = data
                self.connection_dict[connection].send(json.dumps(message).encode()) #以json格式对所有用户发送输入的信息，此后所有信息都已json格式发送
            show_tips(self.display_info, self.pre_time_(), '{0}: {1}'.format('我', data), '').show() #在服务器窗体显示发送的信息
        except Exception as e:
            show_tips(self.display_info, self.pre_time_(),  '发送消息失败，请重试', '').show()   #发送失败提示信息
            print(e)

    # 该函数用来广播信息，即将服务器受到的一条用户信息发送给除发送者以外所有用户
    def broadcast_data(self, sender, data):
        for connection in self.connection_dict: #遍历连接的用户key
            # print(connection)
            if(sender != connection):   #出发送者以外
                message = {}
                message['sender'] = sender
                message['message'] = data
                self.connection_dict[connection].send(json.dumps(message).encode()) #发送信息

    # 该函数提供三个功能：
    # 1.显示已连接用户列表
    # 2、建立死循环监听用户的连接，有用户建立连接时则为其创建一个线程，并在用户建立连接时在服务器消息窗口显示
    # 3、遍历用户连接字典，将key值发送给所有用户，让用户得知当前在线用户
    def dispaly_message(self):
        s = self.server
        self.user_info.insert('end', '已连接的用户:')
        while True:
            # print('当前有{0}个线程_'.format(threading.activeCount()))
            # for i in threading.enumerate():
            #     print(i)
            client, address = s.accept()    #运行至此阻塞，监听用户连接，建立连接口执行下列步骤，执行完后在此处再次阻塞，监听新用户连接
            self.connection_dict[address] = client  #在用户连接字典中创建一个key为(ip,端口)，value为socket元素(将连接的用户对象加入到连接字典)
            # print(self.connection_dict)
            show_tips(self.display_info, self.pre_time_(), '用户: {0} 已连接，当前在线人数为{1}人'.format(address, len(self.connection_dict)), '').show() #在消息窗体显示提示信息
            self.user_info.insert('end', '用户 :{0}'.format(address)) #将用户插入到在线用户列表listbox组建中
            for connection in self.connection_dict:
                message = {}
                message['users'] = list(self.connection_dict.keys())
                self.connection_dict[connection].send(json.dumps(message).encode()) #对所有用户发送在线用户列表
            t = threading.Thread(target=self.receive_data, args=(address,)) #将为新加入用户建立新线程，监听用户信息
            # print(t.name)
            t.start()   #启动用户子线程
            # print('当前有{0}个线程'.format(threading.activeCount()))

    # 该函数用于接受用户信息，用户信息分为所有人信息和私聊信息
    def receive_data(self, address):
        while True:
            try:
                # 如果要写私聊消息的离线显示，应该创建一个离线用户字典，当用户下线时，在离线消息字典中创建key为用户的(ip, 端口)，value初始为空列表
                #当收到消息，并判断为私聊消息后，先遍历在线用户字典，检查私聊消息中的接受者是否在线，若不在线，则遍历离线用户字典，若在离线用户字典中找到
                #接受者，则在字典中接受者key对应的value中加入私聊消息
                # 每次在客户端建立连接时，遍历离线用户字典中value长度为非空的历史离线用户(这些用户存在私聊消息)，若匹配上，则将用户离线列表中的消息推送给该用户。
                client = self.connection_dict[address]
                data = client.recv(1024)
                # 私聊信息中含有send_to字段，而公开信息中没有，
                # 所以若为私聊信息则运行try中的转发私聊聊天信息代码块
                try:
                    receive_message = json.loads(data.decode())
                    send_to = receive_message['send_to']
                    send_to_tuple = tuple(send_to)
                    message = receive_message['message']
                    receive_message['sender'] = address
                    for connection in self.connection_dict:
                        if (connection == send_to_tuple):
                            self.connection_dict[connection].send(json.dumps(receive_message).encode()) #若在在线用户列表中找到了私聊对象，则将信息发送给他
                            break
                    self.display_info.insert('end', '{0}'.format(self.pre_time_()))
                    self.display_info.insert('end', '用户: {0}对用户: {1}发送了一条私聊消息:'.format(address, send_to_tuple)) #服务端回显
                    self.display_info.insert('end', '{0}'.format(message))
                    self.display_info.insert('end', '')

                # 未找到send_to字段，运行except，广播共公开信息
                except:
                    show_tips(self.display_info, self.pre_time_(), '用户: {0}: {1}'.format(address, data.decode()), '').show()
                    self.broadcast_data(address, data.decode()) #广播公开信息

            #连接过程中出错，断开对应用户连接，将其移出连接用户列表，将新的在线用户列表发送给所有人
            except Exception as e:
                print(e)
                address_list = list(self.connection_dict.keys())
                self.user_info.delete(address_list.index(address)+1)
                self.connection_dict.pop(address)
                show_tips(self.display_info, self.pre_time_(), '用户: {0} 已断开连接，当前在线人数为{1}人'.format(address, len(self.connection_dict)), '').show()
                for connection in self.connection_dict:
                    message = {}
                    message['users'] = list(self.connection_dict.keys())
                    self.connection_dict[connection].send(json.dumps(message).encode())
                break
            # finally:
                # print('当前有{0}个线程'.format(threading.activeCount()))

    # 开启显示信息和监听用户连接函数的线程
    def startNewThread(self):
        t = threading.Thread(target=self.dispaly_message, args=())
        # print(t.name)
        t.setDaemon(True)
        t.start()


# socket类
class server():
    def __init__(self):
        self.host = '127.0.0.1' #ip
        self.port = 8099    #端口
    def start_server(self):
        # BUF_SIZE = 1024
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #创建socket对象
        server.bind((self.host, self.port)) #绑定soket
        server.listen(20)  # 接收的连接数，最大允许多少个socket连接
        return server   #运行socket


def main():
    # 创建窗口实体类
    gui = server_gui()
    #执行窗体类中的启动线程方法
    gui.startNewThread()
    # 开始绘制窗口
    tkinter.mainloop()

if __name__ == '__main__':
    main()

# 断开连接后结束子进程
# 不给发送消息者推送消息
# 优化发送者显示
# 优化窗体