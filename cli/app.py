import base64
import json
import qrcode
import qrcode.constants
from flask import Flask, request, render_template
from io import BytesIO
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        url = request.form['url']
        
        # Create QR code with updated parameters
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(url)
        
        # Check if file was uploaded
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            
            # Validate file type
            allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp'}
            if not file.filename.lower().split('.')[-1] in allowed_extensions:
                return 'Invalid file type. Only PNG, JPG, and BMP are allowed.', 400
            
            # Read image into memory buffer
            image_buffer = BytesIO(file.read())
            
            # Generate QR code image with uploaded image embedded
            qr_img = qr.make_image(
                image_factory=StyledPilImage, 
                color_mask=SolidFillColorMask(), 
                embeded_image_path=image_buffer
            )
        else:
            # Generate QR code without image
            qr_img = qr.make_image()
        
        # Convert to base64 for embedding in HTML
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Render results page with embedded image
        return render_template('results.html', processed_image=image_base64)
    
    # Upload form
    return render_template('index.html')

# Vercel requires an app handler
def app(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('QR Code Generator')
    }