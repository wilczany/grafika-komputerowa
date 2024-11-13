import struct
from PIL import Image
import numpy as np

class PPMLoader:
    def load(self, file_path):
        with open(file_path, 'rb') as f:
            # Read header
            magic = f.readline().decode().strip()
            if magic not in ['P3', 'P6']:
                raise ValueError("Unsupported PPM format")
                
            # Skip comments
            line = f.readline()
            while line.startswith(b'#'):
                line = f.readline()
                
            # Read dimensions
            width, height = map(int, line.decode().strip().split())
            max_val = int(f.readline().strip())
            

            if magic == 'P3':

                return self._load_p3(f, width, height, max_val)
            else:
                return self._load_p6(f, width, height, max_val)
                
    def _load_p3(self, f, width, height, max_val):
        data = np.zeros((height, width, 3), dtype=np.uint8)
        values = []
        
        # Read all numbers efficiently
        for line in f:
            values.extend(map(int, line.split()))
            
        idx = 0
        for y in range(height):
            for x in range(width):
                for c in range(3):
                    data[y, x, c] = int(values[idx] * 255 / max_val)
                    idx += 1
                     
        return data
        
    def _load_p6(self, f, width, height, max_val):
        data = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Read binary data in blocks
        block_size = width * 3
        for y in range(height):
            row_data = f.read(block_size)
            if max_val == 255:
                data[y] = np.frombuffer(row_data, dtype=np.uint8).reshape(width, 3)
            else:
                row_values = np.frombuffer(row_data, dtype=np.uint8)
                data[y] = (row_values * 255 / max_val).astype(np.uint8).reshape(width, 3)
                
        return data

class JPEGLoader:
    def load(self, file_path):
        with Image.open(file_path) as img:
            return np.array(img)
            
    def save(self, image_data, file_path, quality=85):
        Image.fromarray(image_data).save(file_path, quality=quality)

# image_processor.py
