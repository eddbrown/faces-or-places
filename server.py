from flask import Flask, request, redirect, url_for
import os
from PIL import Image
import PIL
import numpy as np
import pickle

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    # Open file and convert
    file = request.files['image']
    image_params = pickle.load(open("server/data/image_params.p", "rb"))
    img = Image.open(file)
    img = img.resize((image_params['width'], image_params['height']), PIL.Image.ANTIALIAS)
    image_array = np.asarray(img, dtype="int32" )
    converted_image = image_array.reshape((1,-1))

    # Load classifier and predict
    classifier = pickle.load(open("server/classifiers/classifier.p", "rb"))
    prediction = classifier.predict(converted_image)[0]

    if prediction == 1:
        return 'face'
    else:
        return 'place'

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)