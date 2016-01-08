import os
from flask import Flask
from flask import render_template, request, redirect
from flask import send_from_directory, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
         	filename = secure_filename(file.filename)
         	return filename
        else:
			return 'There was a problem; please try again.'
	else:
    	return render_template('main.html', image=None)

if __name__ == '__main__':
	app.debug = True
	app.run()
