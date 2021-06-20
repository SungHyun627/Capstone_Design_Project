#!/usr/bin/env python3
import os
import json
from apibucket import ocr, tts, dialogflow, weather_api, firebase, oxford
from audio import playing, playing_mp3
import signal
import pvporcupine
import pyaudio
import time
import struct
import wave
from picamera import PiCamera
from gpiozero import Button
# add module
import firebase_admin
from firebase_admin import credentials, firestore
import datatime

stop_program = False


def signal_handler(signal, frame):
    global stop_program
    stop_program = True


class Main():
    def __init__(self, credential_json_path, config_json_path):
        # self.detector = hotword.hotword()
        print('!!')
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"] = credential_json_path
        self.project_id = 'pi-reader-qt99'
        self.session_id = 'Pi_Reader'
        self.audio_file = 'recording_now.wav'
        self.language_code = 'en'
        with open(config_json_path, 'r') as jj:
            self.config = json.load(jj)

        self.alarm_on = 'resources/dong.wav'
        self.alarm_off = 'resources/ding.wav'
        self.ocr = ocr.OCR()
        self.dialogflow = dialogflow.DIALOGFLOW()
        self.tts = tts.TTS()
        

        self.camera = PiCamera()
        self.form_1 = pyaudio.paInt16  # 16-bit resolution
        self.chans = 1  # 1 channel
        self.samp_rate = 16000  # 44.1kHz sampling rate
        self.chunk = 512  # 2^12 samples for buffer
        self.record_secs = 5  # seconds to record
        # device index found by p.get_device_info_by_index(ii)<< 디바이스 위치 체크
        self.dev_index = 1
        self.wav_output_filename = 'resources/record_now_test.wav'

        self.b1 = Button(17)
        self.b2 = Button(22)
        self.b3 = Button(27)
        self.b4 = Button(23)

        self.image_save_path = 'resources/output.jpg'
        self.audio_save_path = 'resources/output.mp3'
        self.player_beep = playing.Player(self.alarm_on,num=0)
        self.player_read = playing_mp3.Player_mp3(self.audio_save_path)

        # db transaction
        # self.cred = credentials.Certificate(credential_json_path)
        # self.admin_initialzie = firebase_admin.initialize_app(self.cred)
        # self.db = firestore.client()

        self.db, self.transaction = firebase.initialize()

    def recording(self):
        # stream = pa.open(format=self.form_1, rate=self.samp_rate, channels=self.chans,
        #                  input_device_index=self.dev_index, input=True, frames_per_buffer=self.chunk)
        frames = []
        for ii in range(0, int((self.samp_rate / self.chunk) * self.record_secs)):
            data = self.audio_stream.read(self.chunk)
            frames.append(data)

        print("finished recording")

        # stop the stream, close it, and terminate the pyaudio instantiation
        # pa.stop_stream()
        # pa.close()

        # save the audio frames as .wav file
        self.wavefile = wave.open(self.wav_output_filename, 'wb')
        self.wavefile.setnchannels(self.chans)
        self.wavefile.setsampwidth(self.pa.get_sample_size(self.form_1))
        self.wavefile.setframerate(self.samp_rate)
        self.wavefile.writeframes(b''.join(frames))
        self.wavefile.close()

    def capture(self):
        self.camera.start_preview()
        time.sleep(0.5)
        self.camera.capture(self.image_save_path)
        self.camera.stop_preview()

    def pic_read(self):
        self.capture()
        self.text = self.ocr.run(self.image_save_path)
        time.sleep(0.5)
        self.tts.run(self.text, self.audio_save_path)
        time.sleep(0.5)
        self.player_read.play()

    def main_flow(self, isMic, bnum=0):
        print('[Pireader] In Main flow..')
        # Firebase_admin initialize
        # transaction = self.db.transaction()

        if isMic:
            print('from Mic')
            self.player_read.pause()
            self.player_beep.filename = self.alarm_on
            self.player_beep.play()  # 말씀하세용
            self.recording()
            self.player_beep.filename = self.alarm_off
            self.player_beep.play()  # 끝났어용
            response = self.dialogflow.run(self.wav_output_filename)
            fulfill = response.split(':')

            if(fulfill[0] == 'reading_control'):
                if fulfill[0] == 'stop':
                    self.player_read.pause()
                elif fulfill[1] == 'start':
                    self.player_read.resume()

                # self.player_read.playPause()
                return
            elif(fulfill[0] == 'move_control'):
                print(len(fulfill))
                if len(fulfill) == 4:
                    amount = int(fulfill[2]) * 1000
                else:
                    amount = 5000  
                if fulfill[1] == 'ahead':
                    self.player_read.next_5s(amount)
                elif fulfill[1] == 'before':
                    self.player_read.previous_5s(amount)
            elif(fulfill[0] == 'volume_control'):
                if fulfill[1] == 'increase':


                    for _ in range(int(fulfill[2])):
                        self.player_read.volumeUp()
                elif fulfill[1] == 'decrease':
                    for _ in range(int(fulfill[2])):
                        self.player_read.volumeDown()
            elif(fulfill[0] == 'picture_control'):
                print('picture and read')
                self.pic_read()
            elif(fulfill[0] == 'mark_make'):
                error_text = firebase.mark_make_update(self.transaction, self.db, fulfill[1].lower())
                if error_text:
                    print(error_text)
                    self.tts.run(error_text, self.audio_save_path)
                    time.sleep(0.5)
                    self.player_read.play()
                    return 
            elif(fulfill[0] == 'mark_save'):
                error_text = firebase.mark_save_update(self.transaction, self.db, fulfill[1].lower(), self.text)
                if error_text:
                    print(error_text)
                    self.tts.run(error_text, self.audio_save_path)
                    time.sleep(0.5)
                    self.player_read.play()
                    return
            elif(fulfill[0] == 'mark_call'):
                if fulfill[2] == "" or "0":
                    value = 1
                else:
                    value = int(fulfill[2])
                text_list = firebase.mark_call_update(self.transaction, self.db, fulfill[1].lower(), value)
                # Error text
                if (text_list == "Index out of range") or (text_list == "There is no matching category"):
                    print(text_list)
                    self.tts.run(text_list, self.audio_save_path)
                    time.sleep(0.5)
                    self.player_read.play()
                    return
                
                called_texts = "" 
                for called_text in text_list:
                    called_texts += called_text + " "
                print(called_texts)
                self.tts.run(called_texts, self.audio_save_path)
                time.sleep(0.5)
                self.player_read.play()
                return
                
            elif(fulfill[0] == 'weather_control'):
                text = weather_api.weather_control_update()
                print(text)
                self.tts.run(text, self.audio_save_path)
                time.sleep(0.5)
                self.player_read.play()
                return

            elif(fulfill[0] == 'find_control'):
                oxford.Word.get(fulfill[1])
                self.tts.run(oxford.Word.definitions()[0], self.audio_save_path)
                time.sleep(0.5)
                self.player_read.play()
                
            elif(fulfill[0] == 'time'):
                self.tts.run(time.strftime('%c', time.localtime(time.time())),self.audio_save_path)
                time.sleep(0.5)
                self.player_read.play()
            # config.json
            # db건들수있는거
            print('[PiReader] Now transcribe the audioc buffer to text')
            self.player_read.resume()
        else:
            print('from button')
            if bnum == 17:
                self.player_read.pause()
                self.pic_read()
            elif bnum == 22:
                self.player_read.volumeUp()
            elif bnum == 27:
                self.player_read.volumeDown()
            elif bnum == 23:
                self.player_read.playPause()
        # Run app function
        # answer_text = self.response[response_number](words)
        # self.speaker.speak(answer_text)

    def porcu(self):
        # porcupine = pvporcupine.create(keywords=["picovoice", "blueberry"])
        porcupine = pvporcupine.create(keyword_paths=[
                                       '/home/pi/PiReader/resources/raspberry__en_raspberry-pi_2021-07-08-utc_v1_9_0.ppn'])

        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length)
        print(porcupine.sample_rate, pyaudio.paInt16, porcupine.frame_length)
        # pa.get_default_input_device_info()

        while True:
            pcm = self.audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Hotword Detected")
                # audio_stream.stop_stream()
                # audio_stream.close()
                self.main_flow(isMic=True)
            elif self.b1.is_pressed:
                print('green button')
                time.sleep(0.5)
                self.main_flow(isMic=False, bnum=17)

            elif self.b2.is_pressed:
                print('yellow button')
                time.sleep(0.5)
                self.main_flow(isMic=False, bnum=22)

            elif self.b3.is_pressed:
                print('red button')
                time.sleep(0.5)
                self.main_flow(isMic=False, bnum=27)

            elif self.b4.is_pressed:
                print('gray button')
                time.sleep(0.5)
                self.main_flow(isMic=False, bnum=23)


if __name__ == '__main__':
    print('PiReader is Running...')
    credential_json_path = '/home/pi/PiReader/src/apibucket/pi-reader-qt99-firebase-adminsdk-pjfom-846fa09d75.json'
    config_json_path = 'src/config.json'
    # model_path = 'detector/resources/models/pi_3.pmdl'
    pi = Main(credential_json_path=credential_json_path,
              config_json_path=config_json_path)
    pi.porcu()
