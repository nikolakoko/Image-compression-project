import cv2


def rle_encode(image):
    pixels = image.flatten()
    rle = []
    prev_pixel = pixels[0]
    count = 1
    for pixel in pixels[1:]:
        if pixel == prev_pixel:
            count += 1
        else:
            rle.append((prev_pixel, count))
            prev_pixel = pixel
            count = 1
    rle.append((prev_pixel, count))
    return rle


def save_rle(rle, filename):
    with open(filename, 'w') as f:
        for pixel, count in rle:
            f.write(f"{pixel} {count}\n")


def compress_image_with_rle(image, filename):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rle = rle_encode(image)
    output_file = f'{filename}'
    save_rle(rle, output_file)
    return output_file
