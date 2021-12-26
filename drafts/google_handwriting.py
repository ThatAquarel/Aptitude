import io

import numpy as np
from google.cloud import vision_v1 as vision
from google.cloud.vision_v1 import AnnotateImageResponse

import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon


def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # response = client.document_text_detection(image=image)
    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


if __name__ == '__main__':
    # import os
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    #     "C:\\Users\\xia_t\\Desktop\\Projects\\aptitude-335516-23a026200da7.json"
    # detect_document("alice.jpg")

    with open("google_handwriting_response", "rb") as file:
        data = file.read()
        response = AnnotateImageResponse.deserialize(data)


    def get_vertices(element):
        return np.array([
            (vertex.x, vertex.y)
            for vertex in element.bounding_box.vertices
        ])


    patches = []
    colors = []
    paragraph_vertices = []
    for page in response.full_text_annotation.pages:
        # patches.append(Polygon(get_vertices(page), True))
        # colors.append(0)

        for block in page.blocks:
            # patches.append(Polygon(get_vertices(block), True))
            # colors.append(0.3)

            for paragraph in block.paragraphs:
                patches.append(Polygon((vertices := get_vertices(paragraph)), True))
                paragraph_vertices.append(vertices)
                colors.append(0.6)

                a = ""
                for word in paragraph.words:
                    patches.append(Polygon(get_vertices(word), True))
                    colors.append(0.9)
                    a += ''.join([symbol.text for symbol in word.symbols])
                    a += " "

                print(a)

    paragraph_vertices = np.array(paragraph_vertices)
    b = np.add.reduce(paragraph_vertices[:, [0, 3]], axis=1)
    c = np.add.reduce(paragraph_vertices[:, [1, 2]], axis=1)
    d = np.subtract.reduce(b - c)
    dx = c[:, 1] / c[:, 0]

    image = Image.open("alice.jpg")
    image = np.array(image)

    fig, ax = plt.subplots()
    ax.imshow(image)
    p = PatchCollection(patches, alpha=0.5)
    p.set_array(colors)
    ax.add_collection(p)

    plt.show()
    print()
