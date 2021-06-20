from google.cloud import vision
import io


class OCR():
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def run(self, path):
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        price_candidate = []
        card_number_candidate = []
        date_candidate = []

        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        text = texts[0].description.replace(',','')

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        return text

if __name__ == '__main__':
    