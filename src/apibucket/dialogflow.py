import os
from google.cloud import dialogflow


class DIALOGFLOW():
    def __init__(self):
        self.project_id = 'pi-reader-qt99'
        self.session_id = 'Pi_Reader'
        self.session_clinet = dialogflow.SessionsClient()
        self.audio_encoding = dialogflow.AudioEncoding.AUDIO_ENCODING_LINEAR_16
        self.sample_rate_hertz = 16000
        self.lang_code = 'en'
        self.session = self.session_clinet.session_path(self.project_id, self.session_id)

    def run(self, path):
        print('run')
        with open(path, "rb") as audio_file:
            input_audio = audio_file.read()

        audio_config = dialogflow.InputAudioConfig(
            audio_encoding=self.audio_encoding,
            language_code=self.lang_code,
            sample_rate_hertz=self.sample_rate_hertz,
        )
        query_input = dialogflow.QueryInput(audio_config=audio_config)

        request = dialogflow.DetectIntentRequest(
            session=self.session,
            query_input=query_input,
            input_audio=input_audio,
        )
        response = self.session_clinet.detect_intent(request=request)

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        return response.query_result.fulfillment_text

# def detect_intent_audio(project_id, session_id, audio_file_path, language_code):
#
#     """Returns the result of detect intent with an audio file as input.
#
#     Using the same `session_id` between requests allows continuation
#     of the conversation."""
#     os.environ[
#         "GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/joonkee/PycharmProjects/firebase_test/pi-reader-qt99-firebase-adminsdk-pjfom-846fa09d75.json"
#     session_client = dialogflow.SessionsClient()
#
#     # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
#     audio_encoding = dialogflow.AudioEncoding.AUDIO_ENCODING_LINEAR_16
#     sample_rate_hertz = 16000
#
#     session = session_client.session_path(project_id, session_id)
#     print("Session path: {}\n".format(session))
#
#     with open(audio_file_path, "rb") as audio_file:
#         input_audio = audio_file.read()
#
#     audio_config = dialogflow.InputAudioConfig(
#         audio_encoding=audio_encoding,
#         language_code=language_code,
#         sample_rate_hertz=sample_rate_hertz,
#     )
#     query_input = dialogflow.QueryInput(audio_config=audio_config)
#
#     request = dialogflow.DetectIntentRequest(
#         session=session,
#         query_input=query_input,
#         input_audio=input_audio,
#     )
#     response = session_client.detect_intent(request=request)
#
#     print("=" * 20)
#     print("Query text: {}".format(response.query_result.query_text))
#     print(
#         "Detected intent: {} (confidence: {})\n".format(
#             response.query_result.intent.display_name,
#             response.query_result.intent_detection_confidence,
#         )
#     )
#     print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))


# def detect_intent_texts(project_id, session_id, texts, language_code):
#     """Returns the result of detect intent with texts as inputs.
#
#     Using the same `session_id` between requests allows continuation
#     of the conversation."""
#     from google.cloud import dialogflow
#
#     session_client = dialogflow.SessionsClient()
#
#     session = session_client.session_path(project_id, session_id)
#     print("Session path: {}\n".format(session))
#
#     for text in texts:
#         text_input = dialogflow.TextInput(text=text, language_code=language_code)
#
#         query_input = dialogflow.QueryInput(text=text_input)
#
#         response = session_client.detect_intent(
#             request={"session": session, "query_input": query_input}
#         )
#
#         print("=" * 20)
#         print("Query text: {}".format(response.query_result.query_text))
#         print(
#             "Detected intent: {} (confidence: {})\n".format(
#                 response.query_result.intent.display_name,
#                 response.query_result.intent_detection_confidence,
#             )
#         )
#         print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
#
#
# if __name__ == '__main__':
#     detect_intent_audio('pi-reader-qt99', 'Pi_Reader', 'dialog2.wav', 'en')
#     # detect_intent_texts('pi-reader-qt99', 'Pi_Reader', 'decrease volume by 5', 'en')
