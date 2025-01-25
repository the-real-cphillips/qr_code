#!/usr/bin/env python3 

import qrcode
import qrcode.constants
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask

qr_fb = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr_fb.add_data('https://www.facebook.com/kookiesbykrista/')

qr_ig = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr_ig.add_data('https://www.instagram.com/kookiesbykrista/')

img_fb = qr_fb.make_image(image_factory=StyledPilImage, color_mask=SolidFillColorMask(), embeded_image_path="Facebook_Logo_Primary.png")
img_ig = qr_ig.make_image(image_factory=StyledPilImage, color_mask=SolidFillColorMask(), embeded_image_path="white-Instagram_Glyph_Gradient.png")

img_fb.save("fb-logo-qr.png")
img_ig.save("ig-logo-qr.png")