import sys
import os
import configparser
import pygame

fp_dir = os.getcwd()

config = configparser.ConfigParser()
configpath = fp_dir + '/config.ini'
config.read(configpath, encoding="utf-8-sig")
petname = config.get("config", "petID")
traypath = config.get("config", "traypath")

count = config.get("config", "count")

actionraw = config.get("config", "action")
action = actionraw.split(',')

actionEnraw = config.get("config", "actionEn")
actionEn = actionEnraw.split(',')

actiondic = {}
beginnum = 0

while (beginnum < int(count)):
    actiondic[action[beginnum]] = actionEn[beginnum]
    beginnum += 1

actionnumraw = config.get("config", "actionnum")
actionnum = actionnumraw.split(',')

actionpath = config.get("config", "actionpath")

#获取播放音乐的音量
volume = config.get("config", "volume")

#获取音乐总数
musictotal = int(config.get("config", "musictotal"))

playnum = 0

#音乐播放索引
index = int(config.get("config", "index"))
print(index)


musicnameraw = config.get("config", "musicname")
musicname = musicnameraw.split(',')



def music(index):
    pygame.mixer.init()
    pygame.mixer.music.load(musiclist1[index])
    pygame.mixer.music.set_volume(float(volume))
    print(pygame.mixer.music.get_volume())
    pygame.mixer.music.play(1)
    pygame.mixer.music.get_busy()
    # print(pygame.mixer.music.get_busy())

musiclist = []
musiclist1 = {}
number = 0
for i in os.listdir('data/music/'):
    musiclist.append('data/music/'+i)
    musiclist1[number] = 'data/music/'+i
    number += 1

# print(musicname)
# print(musiclist1)


music000 = []
music000dic = {}
m = 0
for item in os.listdir('data/music/'):
    music000dic[int(musicname[m])] = 'data/music/' + item
    music000.append('data/music/' + item)
    m += 1

# print(music000)
# print(music000dic)