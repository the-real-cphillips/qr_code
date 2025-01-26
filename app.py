import os
import base64
import qrcode
import qrcode.constants
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from flask import Flask, request, render_template
from io import BytesIO
import serverless_wsgi

# Ensure absolute path for templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        url = request.form['url']
        
        qr = qrcode.QRCode(
            version=1, 
            box_size=10, 
            border=5, 
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(url)
        
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            
            allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp'}
            if not file.filename.lower().split('.')[-1] in allowed_extensions:
                return 'Invalid file type. Only PNG, JPG, and BMP are allowed.', 400
            
            image_buffer = BytesIO(file.read())
            
            qr_img = qr.make_image(
                image_factory=StyledPilImage, 
                color_mask=SolidFillColorMask(), 
                embeded_image_path=image_buffer
            )
        else:
            qr_img = qr.make_image()
        
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return render_template('results.html', processed_image=image_base64)
    
    return render_template('index.html')

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)