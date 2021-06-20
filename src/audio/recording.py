# -*- coding: utf-8 -*-

import pyaudio
import wave
import pydub
import datetime


# rec -r 16000 -c 1 -b 16 -e signed-integer -t wav 2.wav trim 0 2
class Recorder:
    def __init__(self):
        now = datetime.datetime.now()
        self.form_1 = pyaudio.paInt16  # 16-bit resolution
        self.chans = 1  # 1 channel
        self.samp_rate = 16000  # 44.1kHz sampling rate
        self.chunk = 1024  # 2^12 samples for buffer
        self.record_secs = 5  # seconds to record
        self.dev_index = 1  # device index found by p.get_device_info_by_index(ii)<< 디바이스 위치 체크
        self.wav_output_filename = 'record_now_test.wav'  # name of .wav file

    def Recording_audio(self):
        audio = pyaudio.PyAudio()  # create pyaudio instantiation

        # create pyaudio stream
        stream = audio.open(format=self.form_1, rate=self.samp_rate, channels=self.chans,
                            input_device_index=self.dev_index, input=True, frames_per_buffer=self.chunk)
        print("recording")
        frames = []

        # loop through stream and append audio chunks to frame array
        for ii in range(0, int((self.samp_rate / self.chunk) * self.record_secs)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("finished recording")

        # stop the stream, close it, and terminate the pyaudio instantiation
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # save the audio frames as .wav file
        self.wavefile = wave.open(self.wav_output_filename, 'wb')
        self.wavefile.setnchannels(self.chans)
        self.wavefile.setsampwidth(audio.get_sample_size(self.form_1))
        self.wavefile.setframerate(self.samp_rate)
        self.wavefile.writeframes(b''.join(frames))

    def close_wav(self):
        self.wavefile.close()

    def convert_to_mp3(self):
        # .wav file into mp3 file
        now = datetime.datetime.now()
        sound = pydub.AudioSegment.from_wav(self.wav_output_filename)
        sound.export("/home/pi/" + now + "_recording.mp3", format="mp3")


if __name__ == '__main__':
    p = pyaudio.PyAudio()
    for ii in range(p.get_device_count()):
        print(p.get_device_info_by_index(ii).get('name'))  ## 헤드셋 디바이스 위치 체크
    record = Recorder()
    record.Recording_audio()
