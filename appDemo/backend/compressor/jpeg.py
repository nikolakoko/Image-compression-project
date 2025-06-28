import cv2
import io


def compress_image(image, quality):
    output_stream = io.BytesIO()

    is_success, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])

    if is_success:
        output_stream.write(buffer)
    output_stream.seek(0)
    return output_stream
