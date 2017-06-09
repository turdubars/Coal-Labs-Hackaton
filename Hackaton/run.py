import os
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
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect('/')
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect("/")
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			heads_counter = 5

		return render_template("counter.html", filename=filename, heads_counter=heads_counter)
	
	flash("Error")
	return redirect("/")

if __name__ == '__main__':
	app.run(debug=True)