from google.cloud import texttospeech


class TTS():
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        self.gender = texttospeech.SsmlVoiceGender.NEUTRAL
        self.lang_code = 'ko-KR'
        self.voice_name = 'ko-KR-Wavenet-A'
        self.voice = texttospeech.VoiceSelectionParams(
            language_code=self.lang_code,
            name=self.voice_name,
            ssml_gender=self.gender
        )

    def run(self, text, output_path = 'output.wav'):
        voices = self.client.list_voices()
        input_text = texttospeech.SynthesisInput(text=text)

        response = self.client.synthesize_speech(
            request={"input": input_text, "voice": self.voice, "audio_config": self.audio_config}
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')
