import cv2
import io


def compress_image(image, quality):
    output_stream = io.BytesIO()
    is_success, buffer = cv2.imencode(".png", image, [cv2.IMWRITE_PNG_COMPRESSION, quality])
    if is_success:
        output_stream.write(buffer)
    output_stream.seek(0)
    return output_stream
