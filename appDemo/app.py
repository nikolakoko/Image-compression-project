import io

import cv2
import numpy as np
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename

import kmeans
import rle

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        secure_filename(file.filename)
        file_stream = io.BytesIO(file.read())

        compression_method = request.form['method']
        quality = int(request.form.get('quality', 20))
        k_value = int(request.form.get('k', 8))

        # Read the image from the in-memory file
        file_stream.seek(0)
        image = cv2.imdecode(np.frombuffer(file_stream.read(), np.uint8), cv2.IMREAD_UNCHANGED)

        if compression_method == 'jpeg':
            output_stream = io.BytesIO()

            is_success, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])

            output_stream.write(buffer)
            output_stream.seek(0)
            return send_file(output_stream, as_attachment=True, download_name='compressed_image.jpg',
                             mimetype='image/jpeg')

        elif compression_method == 'png':
            output_stream = io.BytesIO()

            is_success, buffer = cv2.imencode(".png", image, [cv2.IMWRITE_PNG_COMPRESSION, quality])

            output_stream.write(buffer)
            output_stream.seek(0)
            return send_file(output_stream, as_attachment=True, download_name='compressed_image.png',
                             mimetype='image/png')

        elif compression_method == 'kmeans':
            output_image = kmeans.compress_image_with_kmeans(image, k=k_value)
            is_success, buffer = cv2.imencode(".png", output_image)
            output_stream = io.BytesIO(buffer)
            output_stream.seek(0)
            return send_file(output_stream, as_attachment=True, download_name='compressed_image_kmeans.png',
                             mimetype='image/png')

        elif compression_method == 'rle':
            output_file = 'compressed_image_rle.txt'
            rle.compress_image_with_rle(image, output_file)
            return send_file(output_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
