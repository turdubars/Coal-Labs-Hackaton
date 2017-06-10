import cv2
import sys
import os
import random, string
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from flask import Flask, render_template, Response


app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = app.root_path + '/static'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
	return render_template("index.html")

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/counter', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect('/')
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect("/")
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(filepath)

			detected_img_name, heads_counter = detect_heads(filename)


		return render_template("counter.html", image=filename, heads_counter=heads_counter, detected_image=detected_img_name)
	
	flash("Error")
	return redirect("/")

def detect_heads(img_name):
	detected_img_name = '.'.join(img_name.split(".")[0:-1]) + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) + "_detected.jpg"

	cascPath = app.root_path + "/database.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)

	image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
	    gray,
	    scaleFactor=1.1,
	    minNeighbors=1,
	    minSize=(50, 50)
	)

	print("Found {0} people!".format(len(faces)))

	for (x, y, w, h) in faces:
	    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

	cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], detected_img_name), image)
	return detected_img_name, len(faces)

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')