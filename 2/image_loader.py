from PIL import Image

from PySide6.QtGui import QImage, QColor

class PPMLoader:
    def __init__(self, file_path):
        self.file = open(file_path, 'rb')

        # read magic number
        ppm_type = self.file.readline().strip()
        if ppm_type not in [b'P3', b'P6']:
            raise ValueError("Unsupported PPM format")
        self.ppm_type = ppm_type
        
        params = []
        while len(params) < 3:
            line = next(self.next_line_gen())
            params.extend(line.split())
        if len(params) > 3:
            raise ValueError("Error reading ppm header")

        self.width = int(params[0])
        self.height = int(params[1])
        self.max_val = int(params[2])

    def next_line_gen(self):
        while True:
            line = self.file.readline()
            if not line:
                break
            else:    
                line = line.split(b'#')[0].strip()
                if line:
                    yield line
    
    def get_image_data(self):
        x= 0
        y = 0
        tmp = []
        line_gen = self.next_line_gen()
        image = QImage(self.width, self.height, QImage.Format.Format_RGB888)
        # for w in range(1,5):
        #     test_image = QImage(w,10, QImage.Format_RGB888)
        #     print(f"expected : {w}*3={w*3};given {len(test_image.scanLine(y)[:])}")
        #  :'))
        if self.ppm_type == b'P3':
            # uses generator for lazy loading file
            for line in line_gen:
                values = line.split()
                tmp.extend(values)
                while len(tmp) >= 3:
                    r = int(tmp[0]) * 255 // self.max_val
                    g = int(tmp[1]) * 255 // self.max_val
                    b = int(tmp[2]) * 255 // self.max_val

                    image.setPixelColor(x, y, QColor(r, g, b))
                    tmp = tmp[3:]
                    x += 1
                    if x >= self.width:
                        x = 0
                        y += 1

        elif self.ppm_type == b'P6': 
            data = self.file.read()
            idx = 0
            if self.width < 4:
                for y in range(self.height):
                    for x in range(self.width):
                        r = data[idx]
                        g = data[idx + 1]
                        b = data[idx + 2]
                        image.setPixelColor(x, y, QColor(r, g, b))
                        idx += 3
    
            elif self.max_val == 255:
                # Direct copy if no scaling needed
                for y in range(self.height):
                    start = y * self.width * 3
                    end = start + self.width * 3
                    
                    image.scanLine(y)[:] = data[start:end]
            else:
                # Scale values 
                scaled_data = bytearray(self.width * self.height * 3)
                for i in range(0, len(data), 3):
                    scaled_data[i] = data[i] * 255 // self.max_val
                    scaled_data[i + 1] = data[i + 1] * 255 // self.max_val
                    scaled_data[i + 2] = data[i + 2] * 255 // self.max_val
                
                for y in range(self.height):
                    start = y * self.width * 3
                    end = start + self.width * 3
                    image.scanLine(y)[:] = scaled_data[start:end]
        
        return image
    
class JPEGLoader:
    def load(self, file_path):
        return QImage(file_path)
        
            
    def save(self, image_data, file_path, quality=85):
        Image.fromarray(image_data).save(file_path, quality=quality)