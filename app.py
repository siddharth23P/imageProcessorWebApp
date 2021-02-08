import imghdr
import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

def validate_image(stream):
    header = stream.read(4096)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    uploaded_file.filename = "input.jpg"
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/convertBinary/')
def convertBinary():
    image=cv2.imread('uploads/input.jpg')
    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    se=cv2.getStructuringElement(cv2.MORPH_RECT , (8,8))
    bg=cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
    out_gray=cv2.divide(image, bg, scale=255)
    out_binary=cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1]
    cv2.imwrite('uploads/out_binary.jpg',out_binary)   
    return render_template('convertBinary.html')

@app.route('/removeNoise/')
def removeNoise():
    image=cv2.imread('uploads/input.jpg')
    out_deNoise = cv2.bilateralFilter(image, 21,51,51)
    cv2.imwrite('uploads/out_deNoise.jpg',out_deNoise)
    return render_template('removeNoise.html')

@app.route('/histrogramEqualization/')
def histrogramEqualization():
    image=cv2.imread('uploads/input.jpg')
    channels = cv2.split(image)
    eq_channels = []
    for ch, color in zip(channels, ['B', 'G', 'R']):
        eq_channels.append(cv2.equalizeHist(ch))
    out_eqImage = cv2.merge(eq_channels)
    cv2.imwrite('uploads/out_eqImage.jpg',out_eqImage)
    return render_template('histrogramEqualization.html')

@app.route('/constrastStretching/')
def constrastStretching():
    img = cv2.imread('uploads/input.jpg')
    hist,bins = np.histogram(img.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')
    out_contrastStretching = cdf[img]
    cv2.imwrite('uploads/out_cS.jpg',out_contrastStretching)
    return render_template('constrastStretching.html')

@app.route('/imageNegative/')
def imageNegative():
    img_bgr=cv2.imread('uploads/input.jpg')
    img_rgb=cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    out_neg=1-img_rgb
    cv2.imwrite('uploads/out_neg.jpg',out_neg)
    return render_template('imageNegative.html')

@app.route('/powerLawTransform/')
def powerLawTransform():
    img_bgr=cv2.imread('uploads/input.jpg')
    img_rgb=cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    out_gamma=np.array(255*(img_bgr/255)**2.2, dtype='uint8')
    cv2.imwrite('uploads/out_gamma.jpg',out_gamma)
    return render_template('powerLawTransform.html')

@app.route('/goBack/')
def goBack():
    return redirect(url_for('index'))

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
    