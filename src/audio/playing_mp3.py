# -*- coding: utf-8 -*-
"""
Created on Thu May 20 07:43:38 2021
Pygame 패키지를 pip로 인스톨(콘솔창에서 > pip install pygame)하면 사용준비가 끝난다
@author: A
sudo apt-get install python3-mutagen
"""
import pygame
from pygame import mixer
from mutagen.mp3 import MP3
import time


class Player_mp3:
    def __init__(self, musicFile):
        self.isOn = True
        self.isPlaying = False
        self.isPaused = False

        mixer.init()
        print("MP3 Player initialized")
        self.musicVolume = round(mixer.music.get_volume(), 1)
        self.location = 0
        self.length = 0
        import glob
        # self.musicFiles = tuple(sorted(glob.glob("*.mp3")))  ## 추후 수정
        self.musicNum = 0
        self.musicTitle = musicFile
        # filename = self.musicFiles[self.musicNum]
        self.filename = musicFile
        print(self.filename + "\nReady")
        # self.play()  ##나중에 제거

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
        mixer.music.load(filename)
        self.musicTitle = filename
        audio_length = MP3(filename)
        print("length of audio : ", audio_length.info.length)
        self.length = audio_length.info.length
        self.isPlaying = True
        mixer.music.play()
        print(self.musicTitle + "\nPlaying")


    def pause(self):
        self.isPlaying = False
        mixer.music.pause()
        print(self.musicTitle + "\nPaused")
        self.isPaused = True

    def resume(self):
        self.isPlaying = True
        print(self.musicTitle + "\nResumed")
        print(self.musicTitle + "\nPlaying")
        self.isPaused = False
        mixer.music.unpause()


    # def prev(self):
    #     self.musicNum = (self.musicNum - 1) % len(self.musicFiles)
    #     self.play()
    #
    # def next(self):
    #     self.musicNum = (self.musicNum + 1) % len(self.musicFiles)
    #     self.play()

    def next_5s(self, change = 5000):
        self.location = self.location + mixer.music.get_pos()
        print("current location : ", self.location / 1000, "s")
        if (self.location < (self.length - change/5000) * 1000):
            mixer.music.play(0, (self.location + change) / 1000)
            self.location = self.location + change
            print(self.location)
            mixer.music.play(start=self.location / 1000)
        else:
            pass
        self.location = 0
        ##currenttime = oldsongtime+change+addedtime

    def previous_5s(self,change=5000):
        self.location = self.location + mixer.music.get_pos()
        print("current location : ", self.location / 1000, "s")
        if (self.location > change):
            mixer.music.play(0, (self.location - change) / 1000)
            self.location = self.location - change
            print(self.location)
            mixer.music.play(start=self.location / 1000)
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
        vol = mixer.music.get_volume()
        vol = round(vol, 1)

        if (action == "up") and vol < max:
            vol = round(vol + delta, 1)
            mixer.music.set_volume(vol)
            print(self.musicTitle + "\nvol: " + str(vol))
            self.musicVolume = vol
        elif (action == "down") and vol > min:
            vol = round(vol - delta, 1)
            mixer.music.set_volume(vol)
            print(self.musicTitle + "\nvol: " + str(vol))
            self.musicVolume = vol
        elif action == "mute":
            if vol == min:
                vol = self.musicVolume
                mixer.music.set_volume(vol)
                print(self.musicTitle + "\nvol: " + str(vol))
            else:
                vol = min
                mixer.music.set_volume(vol)
                print(self.musicTitle + "\nMuted")
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


