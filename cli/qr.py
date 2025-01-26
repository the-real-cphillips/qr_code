#!/usr/bin/env python3 

import logging
import random
import string
import qrcode
import qrcode.constants
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask

def setup_logger(logger_name, log_file, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

def generate_qr_code(url):
    qr_output = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr_output.add_data(url)
    qr = qr_output.make_image(image_factory=StyledPilImage, color_mask=SolidFillColorMask())
    return qr


def save_qr_code(qr, file_name=None, file_ext='png'):
    if not file_name:
        letters_and_digits = string.ascii_letters + string.digits
        file_name = f"{''.join(random.choice(letters_and_digits) for _ in range(5))}.{file_ext}"
    return qr.save(f'output/{file_name}')

    
def main():
    logger = setup_logger('qrg', 'logs/qrg.log',)
    qr_url = "https://google.com"

    qr_code = generate_qr_code(qr_url)
    save_qr_code(qr_code)
    logger.info("Created QR code for %s", qr_url)
    
if __name__ == '__main__':
    main()

#img_fb = qr_fb.make_image(image_factory=StyledPilImage, color_mask=SolidFillColorMask(), embeded_image_path="Facebook_Logo_Primary.png")
#img_ig = qr_ig.make_image(image_factory=StyledPilImage, color_mask=SolidFillColorMask(), embeded_image_path="white-Instagram_Glyph_Gradient.png")
#img_ig.save("ig-logo-qr.png")