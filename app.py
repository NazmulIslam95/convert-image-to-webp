from flask import Flask, request, send_file, jsonify
from PIL import Image
import io
import os
import zipfile
import tempfile

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_images():
    files = request.files.getlist('images')
    scale = float(request.form.get('scale', 1))

    if not files:
        return jsonify({'error': 'No files uploaded'}), 400

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, 'converted_images.zip')

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            try:
                img = Image.open(file.stream)
                # Resize image
                new_size = (int(img.width * scale), int(img.height * scale))
                img = img.resize(new_size, Image.ANTIALIAS).convert("RGB")

                # Prepare filename
                base_name = os.path.splitext(file.filename)[0]
                new_filename = f"{base_name}-converted-to-webp.webp"

                # Save to bytes buffer
                buffer = io.BytesIO()
                img.save(buffer, format="WEBP", quality=80)
                buffer.seek(0)

                # Add to zip
                zipf.writestr(new_filename, buffer.read())
            except Exception as e:
                print(f"Failed to process {file.filename}: {e}")
                continue

    return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name='converted_images.zip')


if __name__ == '__main__':
    app.run(debug=True)
# To run the app, use the command: python app.py
# To test the app, you can use a tool like Postman or curl to send a POST request with files.
# Make sure to install Flask and Pillow before running the app:
# pip install Flask Pillow
# Note: This code is for educational purposes and may require additional error handling and security measures for production use.