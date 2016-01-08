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

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			filetype = filename.split('.')[1]
			proc_filename = filename.split('.')[0] + '_processed.' + filetype
			orig_image = file.read().encode('base64').replace('\n', '')
			# proc_image = file.read().encode('base64').replace('\n', '')
			# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# orig_image = url_for('uploaded_file', filename=filename)
			# proc_image = url_for('uploaded_file', filename=proc_filename)
			return render_template('main.html',
				orig_image=orig_image)#, proc_image = proc_image)
		else:
			return 'There was a problem; please try again.'
	else:
		orig_image = open('static/orig_image.jpg').read().encode('base64').replace('\n', '')
#		proc_image = url_for('static', filename='proc_image.jpg')
		return render_template('main.html', orig_image=orig_image)#, proc_image = proc_image)

if __name__ == '__main__':
	app.debug = True
	app.run()
