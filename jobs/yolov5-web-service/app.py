import io
import os
import shutil
import json
from PIL import Image

import torch
import flask
from flask import Flask, jsonify, url_for, render_template, request, redirect

app = Flask(__name__)

RESULT_FOLDER = os.path.join('static')
app.config['RESULT_FOLDER'] = RESULT_FOLDER

model_yolov5s = torch.hub.load('ultralytics/yolov5', 'custom', path='models/yolov5s1.pt')  # default
model_yolov5m = torch.hub.load('ultralytics/yolov5', 'custom', path='models/yolov5m1.pt')  # default

# yolov5s
def get_prediction_yolov5s(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    imgs = [img]  # batched list of images
    # Inference
    results = model_yolov5s(imgs, size=640) 
    return results

# yolov5m
def get_prediction_yolov5m(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    imgs = [img]  # batched list of images
    # Inference
    results = model_yolov5m(imgs, size=640) 
    return results

@app.route('/', methods=['GET'])
def get():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    print(f'User selected model : {request.form.get("model_choice")}')

    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files.get('file')
    if not file:
        return
    
    img_bytes = file.read()
    if request.form.get("model_choice") == 'yolov5s':
        results = get_prediction_yolov5s(img_bytes)
    if request.form.get("model_choice") == 'yolov5m':
        results = get_prediction_yolov5m(img_bytes)
    results.save("static/")  # save the results


    full_filename = os.path.join(app.config['RESULT_FOLDER'], 'image0.jpg')
    return redirect('static/image0.jpg')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
