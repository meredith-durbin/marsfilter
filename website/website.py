# external libraries
import base64
import matplotlib.image as mpimg
import numpy as np
import os
import StringIO
from flask import Flask, render_template, request, send_from_directory, url_for
from PIL import Image
from werkzeug import secure_filename

# local import
from marsfilter import marsfilter

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
			filetype = filename.split('.')[1].lower()
			proc_filename = filename.split('.')[0] + '_mars.' + filetype
			if filetype == 'jpg':
				filetype = 'jpeg' # do i look like i know what a jpeg is
			orig_image_array = mpimg.imread(file) #cv2.imdecode(np.fromstring(file.read(), np.uint8),
				#cv2.CV_LOAD_IMAGE_UNCHANGED)
			proc_image_array = marsfilter(orig_image_array)
			proc_image_PIL = Image.fromarray(proc_image_array)
			image_buffer = StringIO.StringIO()
			proc_image_PIL.save(image_buffer, format=filetype.upper())
			proc_image = base64.b64encode(image_buffer.getvalue())
			return render_template('main.html', proc_image = proc_image,
				proc_filename = proc_filename, filetype=filetype.lower())
		else:
			return 'There was a problem; please try again.'
	else:
		static_file = url_for('static', filename='mars_filter.jpg')
		proc_image = open(static_file).read().encode('base64').replace('\n', '')
		return render_template('main.html', proc_image = proc_image, filetype='jpg')

if __name__ == '__main__':
	app.debug = False
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
