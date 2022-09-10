import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pygame
import config



class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet,self).__init__()
        self.windowset()

        #添加事件
        self.tray()
        self.loadgif()

        #显示桌宠
        self.show()

    #创建窗体
    def windowset(self):
        self.setFixedSize(640, 360)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.repaint()

    #在任务栏中创建可操作菜单栏
    def tray(self):
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon(str('shime1.png')))
        menu = QMenu(self)

        menu.addAction(QAction(config.petname, self))
        menu.addAction(QAction(QIcon('shime1.png'), '显示', self, triggered=self.showwindow))
        menu.addAction(QAction(QIcon('shime1.png'), '隐藏', self, triggered=self.hidewindow))
        menu.addAction(QAction(QIcon('shime1.png'), '退出', self, triggered=self.quit))
        tray.setContextMenu(menu)
        tray.show()

    #加载gif
    def loadgif(self):
        self.movie = QMovie("./data/action/loop.gif")
        self.movie.setScaledSize(QSize(640, 360))
        self.label = QLabel(self)
        self.label.setMovie(self.movie)
        self.move(1400,540)
        self.movie.start()

    # 鼠标左键按下时, 宠物将和鼠标位置绑定
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        elif event.button() == Qt.RightButton:
            self.interact(event)
            event.accept()
        else:
            pass

    # 鼠标移动时调用，实现宠物随鼠标移动
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 鼠标移进时调用
    def enterEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

    #右键桌宠可互动（简洁）
    def interact(self, event):
        global action,musicdic
        action = {}
        musicdic = {}
        menu = QMenu(self)
        menu.addAction(QAction('退出',self, triggered=self.quit))
        menu.addAction(QAction('隐藏', self, triggered=self.hidewindow))

        another = menu.addMenu("其他")
        musicmenu = another.addMenu("音乐")

        musicop = musicmenu.addMenu("操作")
        musicop.addAction(QAction("停止音乐播放", self, triggered=self.stopmusic))
        musicop.addAction(QAction("暂停音乐播放", self, triggered=self.pausemusic))
        musicop.addAction(QAction("恢复暂停音乐", self, triggered=self.unpausemusic))

        for i in config.musiclist:
            musicdic[i] = QAction(i)
            musicmenu.addAction(musicdic[i])
            musicdic[i].triggered.connect(self.music)

        another.addAction(QAction('浏览器', self, triggered=self.net))

        actionmenu = menu.addMenu("动作")
        for item in config.action:
            action[item] = QAction(item)
            # print(action[item])
            actionmenu.addAction(action[item])
            action[item].triggered.connect(self.checkstatus)

        menu.popup(QCursor.pos())

    def checkstatus(self, checked):
        global item
        content = self.sender()
        # print(config.action)
        # print(content,action)
        for item in config.action:
            if content == action[item]:
                # print(item)

                self.movie = QMovie(config.actionpath+config.actiondic[item]+'.gif')
                self.movie.setScaledSize(QSize(640, 360))
                self.label.setMovie(self.movie)
                self.movie.start()
                # print(config.actionpath+config.actiondic[item]+'.gif')
                print("已开启" + item)

    def music(self, checked):
        global i
        content = self.sender()
        for i in config.music000:
            if content == musicdic[i]:
                print(i)

                pygame.mixer.init()
                pygame.mixer.music.load(i)
                pygame.mixer.music.set_volume(float(config.volume))
                # print(pygame.mixer.music.get_volume())
                pygame.mixer.music.play(1)
                pygame.mixer.music.get_busy()

                print("已开始播放" + i)

    #停止播放音乐
    def stopmusic(self):
        print("已停止播放音乐")
        pygame.mixer.init()
        pygame.mixer.music.stop()

    #暂停音乐
    def pausemusic(self):
        print("已暂停音乐")
        pygame.mixer.init()
        pygame.mixer.music.pause()

    #恢复暂停的音乐
    def unpausemusic(self):
        print("已恢复暂停的音乐")
        pygame.mixer.init()
        pygame.mixer.music.unpause()

    @staticmethod
    def net():
        try:
            os.startfile(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
            print("已打开浏览器")
        except:
            print('路径不正确')

    #退出
    def quit(self):
        self.close()
        print("窗口已关闭")
        sys.exit()

    #展示窗口
    def showwindow(self):
        self.setWindowOpacity(1)
        print("窗口已显示")

    #隐藏窗口
    def hidewindow(self):
        self.setWindowOpacity(0)
        print("窗口已隐藏")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DesktopPet()
    sys.exit(app.exec_())
