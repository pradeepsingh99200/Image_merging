from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if files are uploaded
        if 'image1' not in request.files or 'image2' not in request.files:
            return "Please upload both images", 400
        
        image1 = request.files['image1']
        image2 = request.files['image2']

        # Save uploaded images
        image1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
        image2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')
        image1.save(image1_path)
        image2.save(image2_path)

        # Open images using Pillow
        img1 = Image.open(image1_path)
        img2 = Image.open(image2_path)

        # Merge images side by side
        max_height = max(img1.height, img2.height)
        total_width = img1.width + img2.width

        merged_image = Image.new('RGB', (total_width, max_height), (255, 255, 255))
        merged_image.paste(img1, (0, 0))
        merged_image.paste(img2, (img1.width, 0))

        # Save merged image
        merged_path = os.path.join(app.config['UPLOAD_FOLDER'], 'merged.jpg')
        merged_image.save(merged_path)

        return render_template('index.html', merged_image='merged.jpg')

    return render_template('index.html', merged_image=None)

@app.route('/static/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
