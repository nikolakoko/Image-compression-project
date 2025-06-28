import io

import cv2
import numpy as np
from flask import request, send_file, jsonify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

from compressor import kmeans, rle, jpeg, png
from database import db
from models import CompressionLog


def register_routes(app):
    """Register all routes with the Flask app"""

    @app.route('/api/compress', methods=['POST'])
    @cross_origin()
    def compress():
        # Validate file upload
        file = request.files.get('file')
        if not file or not file.filename:
            return jsonify({"error": "No file provided"}), 400

        # Process file
        filename = secure_filename(file.filename)
        file_stream = io.BytesIO(file.read())
        file_stream.seek(0)

        # Decode image
        file_bytes = file_stream.read()
        image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_UNCHANGED)
        if image is None:
            return jsonify({"error": "Invalid image file"}), 400

        # Get compression parameters
        method = request.form.get('method')
        if not method:
            return jsonify({"error": "No compression method specified"}), 400

        quality = int(request.form.get('quality', 20))
        k = int(request.form.get('k', 8))

        # Log compression attempt
        log = CompressionLog(
            filename=filename,
            method=method,
            quality=quality if method in ['jpeg', 'png'] else None,
            k_value=k if method == 'kmeans' else None
        )
        db.session.add(log)
        db.session.commit()

        # Perform compression based on method
        try:
            if method == 'jpeg':
                output_stream = jpeg.compress_image(image, quality)
                return send_file(
                    output_stream,
                    as_attachment=True,
                    download_name='compressed.jpg',
                    mimetype='image/jpeg'
                )

            elif method == 'png':
                output_stream = png.compress_image(image, quality)
                return send_file(
                    output_stream,
                    as_attachment=True,
                    download_name='compressed.png',
                    mimetype='image/png'
                )

            elif method == 'kmeans':
                output_img = kmeans.compress_image_with_kmeans(image, k)
                is_success, buffer = cv2.imencode(".png", output_img)
                if not is_success:
                    return jsonify({"error": "Failed to encode K-means compressed image"}), 500
                output_stream = io.BytesIO(buffer)
                return send_file(
                    output_stream,
                    as_attachment=True,
                    download_name='compressed_kmeans.png',
                    mimetype='image/png'
                )

            elif method == 'rle':
                output_file = 'compressed_rle.txt'
                rle.compress_image_with_rle(image, output_file)
                return send_file(output_file, as_attachment=True)

            else:
                return jsonify({"error": "Unsupported compression method"}), 400

        except Exception as e:
            return jsonify({"error": f"Compression error: {str(e)}"}), 500
