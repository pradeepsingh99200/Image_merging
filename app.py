from flask import Flask, request, render_template, send_from_directory, jsonify
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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

        # Merge images
        merged_path = merge_images(image1_path, image2_path)

        return render_template('index.html', merged_image=os.path.basename(merged_path))

    return render_template('index.html', merged_image=None)


@app.route('/static/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/api/merge', methods=['POST'])
def api_merge():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"error": "Both image1 and image2 are required"}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    # Save uploaded images
    image1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'api_image1.jpg')
    image2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'api_image2.jpg')
    image1.save(image1_path)
    image2.save(image2_path)

    # Merge images
    merged_path = merge_images(image1_path, image2_path)

    return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.basename(merged_path), as_attachment=True)


def merge_images(image1_path, image2_path):
    """Helper function to merge two images side by side."""
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # Calculate dimensions for the merged image
    max_height = max(img1.height, img2.height)
    total_width = img1.width + img2.width

    # Create a new image with a white background
    merged_image = Image.new('RGB', (total_width, max_height), (255, 255, 255))
    merged_image.paste(img1, (0, 0))
    merged_image.paste(img2, (img1.width, 0))

    # Save the merged image
    merged_path = os.path.join(app.config['UPLOAD_FOLDER'], 'merged.jpg')
    merged_image.save(merged_path)

    return merged_path


if __name__ == '__main__':
    app.run(debug=True)
