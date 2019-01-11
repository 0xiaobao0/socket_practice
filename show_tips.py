# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/1/10 16:49'

class show_tips():
    def __init__(self, display_info, time, message, chang_line):
        self.display_info = display_info
        self.time = time
        self.message = message
        self.change_line = chang_line

    def show(self):
        self.display_info.insert('end', '{0}'.format(self.time))
        self.display_info.insert('end', self.message)
        self.display_info.insert('end', self.change_line)