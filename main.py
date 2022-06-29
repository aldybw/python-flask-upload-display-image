import cv2
import numpy as np
from PIL import Image
from skimage import restoration, exposure
# import scipy.ndimage
from scipy import misc
from scipy import ndimage
from matplotlib import pyplot as plt
import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		# paling sih kalo mau ngesave foto yg baru diupload, terus ambil foto yg baru diupload pake cv2.imread, abis itu lakuin proses image enhancement, baru abis itu save output ke folder berbeda
		print("filename :")
		print(filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print(filename.rsplit('.', 1)[1].lower())
		img = cv2.imread("static/uploads/"+filename,0)
		print("img : ")
		print(img)
		equ = cv2.equalizeHist(img)
		# local_mean = ndimage.uniform_filter(equ, size=11)
		# gamma_corrected = np.array(255*(equ / 255) ** 2.2)
		
		# imbright = exposure.adjust_gamma(equ, 1, 1)

		imbright1 = exposure.adjust_log(equ, 1)
		print("imbright1 :")
		print(imbright1)
	
		# p2, p98 = np.percentile(img, (2, 98))
		# img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))
		# res = np.hstack((img,imbright1,img_rescale)) #stacking images side-by-side

		# file3 = str(imbright1)
		# print("file3 :")
		# print(file3)
		# file2 = secure_filename(file3)
		# print("file2 :")
		# print(file2)
		img1 = Image.fromarray(imbright1, 'L')
		print("img1 : ")
		print(img1)
		print("extension : ")
		# print(filename.rsplit('.', 1)[0].lower())
		# print(filename.rsplit('.', 1)[1].lower())
		print(filename.rsplit('.', 1)[0].lower()+"_output."+filename.rsplit('.', 1)[1].lower())
		img1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename.rsplit('.', 1)[0].lower()+"_output."+filename.rsplit('.', 1)[1].lower()))

		# file.save(os.path.join(app.config['UPLOAD_FOLDER'], img1))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		# return render_template('upload.html', filename="static/uploads/"+filename.rsplit('.', 1)[0].lower()+"_output."+filename.rsplit('.', 1)[1].lower())
		return render_template('upload.html', filename=filename.rsplit('.', 1)[0].lower()+"_output."+filename.rsplit('.', 1)[1].lower())
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()