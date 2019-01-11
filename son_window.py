# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/1/9 15:06'

import tkinter
import time
import json

class window():
    def __init__(self, connection, send_to):
        self.son_window = tkinter.Tk()
        self.son_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.son_window.title('')
        self.son_display_info = tkinter.Listbox(self.son_window, width=50)
        self.son_message_input = tkinter.Entry(self.son_window, width=30)
        self.son_send_bottem = tkinter.Button(self.son_window, command=self.send_message, text="发送")
        self.son_display_info.pack()
        self.son_message_input.bind('<Key-Return>', self.send_message)
        self.son_message_input.pack()
        self.son_send_bottem.pack()
        self.connection = connection
        self.send_to = send_to
        self.flag = True
        self.chat_data = []

    def pre_time_(self):
        pre_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return pre_time

    def return_flag(self):
        return self.flag

    def on_closing(self):
        # print(self.flag)
        self.chat_data = self.son_display_info.get(0, tkinter.END)
        self.son_window.destroy()
        print('销毁窗体对象')
        self.flag = False
        # print(self.flag)

    def send_message(self, *event):
        # self.display_info.insert('end', 'test')
        try:
            data = {}
            message = self.son_message_input.get()
            message_length = len(message)
            self.son_message_input.delete(0, tkinter.END)
            data['send_to'] = self.send_to
            data['message'] = message
            self.connection.send(json.dumps(data).encode())
            self.son_display_info.insert('end', '{0}'.format(self.pre_time_()))
            self.son_display_info.insert('end', '{0}: {1}'.format('我', message))
            self.son_display_info.insert('end', '')
        except Exception as e:
            self.son_display_info.insert('end', '{0}'.format(self.pre_time_()))
            self.son_display_info.insert('end', '发送消息失败，请重试')
            self.son_display_info.insert('end', '')
            print(e)



# window_class = window('asd','123')
# window_class.son_window.mainloop()

