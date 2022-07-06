import cv2
import numpy as np
from PIL import Image
from skimage import restoration, exposure
# import scipy.ndimage
from scipy import misc,  ndimage
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
	return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
	# Menampilkan pesan error jika file tidak berada dalam request.files
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	
	# Mengambil file gambar dari request.files
	file = request.files['file']

	# Menampilkan pesan error jika file tidak terpilih
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)

	# Kode program ketika file gambar ada
	if file and allowed_file(file.filename):
		# Langkah pertama adalah menyimpan gambar asli ke direktori penyimpanan
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		# Membaca gambar dan melakukan proses image enhancement
		img = cv2.imread("static/uploads/" + filename, 0)
		equ = cv2.equalizeHist(img)

		#Menampilkan Histogram
		plt.hist(img.ravel(),256,[0,256])
		plt.suptitle("Sebelum")
		plt.show()

		# local_mean = ndimage.uniform_filter(equ, size=11)
		# gamma_corrected = np.array(255*(equ / 255) ** 2.2)
		
		# imbright = exposure.adjust_gamma(equ, 1, 1)

		imbright1 = exposure.adjust_log(equ, 1)
	
		# p2, p98 = np.percentile(img, (2, 98))
		# img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))
		# res = np.hstack((img,imbright1,img_rescale)) #stacking images side-by-side

		# Menggabungkan gambar asli dengan gambar setelah diproses
		res = np.hstack((img, imbright1))
		imgOutput = Image.fromarray(res, 'L')
		
		# Menyimpan gambar gabungan ke direktori penyimpanan 
		processedFilename = filename.rsplit('.', 1)[0].lower() + "_output."
		processedExt = filename.rsplit('.', 1)[1].lower()
		imgOutput.save(os.path.join(app.config['UPLOAD_FOLDER'], processedFilename + processedExt))

		#Menampilkan Histogram
		plt.hist(imbright1.ravel(),256,[0,256])
		plt.suptitle("Sesudah")
		plt.show()

		# file.save(os.path.join(app.config['UPLOAD_FOLDER'], img1))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		# return render_template('upload.html', filename="static/uploads/"+filename.rsplit('.', 1)[0].lower()+"_output."+filename.rsplit('.', 1)[1].lower())
		return render_template('index.html', filename = processedFilename + processedExt)
	else:
		flash('Allowed image types are -> png, jpg, jpeg')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()