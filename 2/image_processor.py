import numpy as np

class ImageProcessor:
    @staticmethod
    def scale_colors(image_data, factor):
        """Linear color scaling"""
        scaled = image_data.astype(float) * factor
        return np.clip(scaled, 0, 255).astype(np.uint8)

