# -*- coding: utf-8 -*-

import pygame
from pygame import mixer
from mutagen.mp3 import MP3
import time


class Player:
    def __init__(self, musicFile,num):
        self.isOn = True
        self.isPlaying = False
        self.isPaused = False
        self.num = num
        mixer.init()
        print("MP3 Player initialized")
        self.musicVolume = round(mixer.music.get_volume(), 1)
        self.location = 0
        self.length = 0
        import glob
        # self.musicFiles = tuple(sorted(glob.glob("*.mp3")))  ## 추후 수정
        self.musicNum = 0
        # filename = self.musicFiles[self.musicNum]
        self.filename = musicFile
        print(self.filename + "\nReady")
        # self.play()  ##나중에 제거
        self.musicTitle = self.filename
        self.music = pygame.mixer.Sound(self.filename)

    def playPause(self):
        if self.isPlaying:
            self.pause()
        else:
            if self.isPaused:
                self.resume()
            else:
                self.play()

    def play(self):
        # filename = self.musicFiles[self.musicNum]
        filename = self.filename
        # mixer.music.load(filename)
        self.music = pygame.mixer.Sound(filename)
        self.length = self.music.get_length()
        self.musicTitle = filename
        self.isPlaying = True
        mixer.Channel(self.num).play(self.music)
        print(self.musicTitle + "\nPlaying")

    def pause(self):
        self.isPlaying = False
        mixer.Channel(self.num).pause()
        print(self.musicTitle + "\nPaused")
        self.isPaused = True

    def resume(self):
        self.isPlaying = True
        print(self.musicTitle + "\nResumed")
        print(self.musicTitle + "\nPlaying")
        self.isPaused = False
        mixer.Channel(self.num).unpause()

    # def prev(self):
    #     self.musicNum = (self.musicNum - 1) % len(self.musicFiles)
    #     self.play()
    #
    # def next(self):
    #     self.musicNum = (self.musicNum + 1) % len(self.musicFiles)
    #     self.play()

    def next_5s(self,change=5000):
        self.location = self.location + mixer.music.get_pos()
        print("current location : ", self.location / 1000, "s")
        if (self.location < (self.length - 5) * 1000):
            mixer.Channel(self.num).play(self.music,0, int((self.location + change) / 1000))
            self.location = self.location + 5000
            print(self.location)
            mixer.Channel(self.num).play(self.music,start=self.location / 1000)
        else:
            pass
        self.location = 0
        ##currenttime = oldsongtime+change+addedtime

    def previous_5s(self,change = 5000):

        self.location = self.location + mixer.music.get_pos()
        print("current location : ", self.location / 1000, "s")
        if (self.location > 5000):
            mixer.Channel(self.num).play(self.music,0, (self.location - change) / 1000)
            self.location = self.location - change
            print(self.location)
            mixer.Channel(self.num).play(start=self.location / 1000)
        else:
            pass
        self.location = 0
        ##currenttime = oldsongtime+change+addedtime

    def restart(self):
        mixer.music.rewind()

    def volumeUp(self):
        self.setVolume("up")
        print("volumn up!")

    def volumeDown(self):
        self.setVolume("down")
        print("volumn down!")

    def setVolume(self, action):
        min, max, delta = 0.0, 1.0, 0.1
        vol = mixer.Channel(self.num).get_volume()
        vol = round(vol, 1)

        if (action == "up") and vol < max:
            vol = round(vol + delta, 1)
            mixer.Channel(self.num).set_volume(vol)
            print(self.musicTitle + "\nvol: " + str(vol))
            self.musicVolume = vol
        elif (action == "down") and vol > min:
            vol = round(vol - delta, 1)
            mixer.Channel(self.num).set_volume(vol)
            print(self.musicTitle + "\nvol: " + str(vol))
            self.musicVolume = vol
        else:
            pass

    def mute(self):
        self.setVolume("mute")

    def onOff(self):
        if self.isOn:
            if self.isPlaying:
                mixer.music.stop()
            print('Bye...')
            time.sleep(2)
            self.isOn = False
        else:
            self.__init__()



