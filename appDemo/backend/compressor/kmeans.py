import cv2
import numpy as np


def compress_image_with_kmeans(image, k=8):
    original_shape = image.shape
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    compressed_image = centers[labels.flatten()]
    compressed_image = compressed_image.reshape(original_shape)
    return compressed_image
