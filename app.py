from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from google.cloud import storage

app = Flask(__name__)

# Configure this environment variable via your Cloud Run settings
bucket_name = os.environ.get('GCS_BUCKET_NAME', 'samyus2')  # Default to 'samyus2' if not set

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

@app.route('/')
def index():
    # Render the upload form HTML
    return render_template('upload_form.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    # Handle file uploads
    uploaded_files = request.files
    file_keys = ['fea_results_file', 'genes_of_interest_file', 'yaml_config_file', 'meta_input_file']
    file_paths = {}
    
    for key in file_keys:
        if key not in uploaded_files:
            return jsonify({'error': f'Missing file: {key}'}), 400

        file = uploaded_files[key]
        filename = secure_filename(file.filename)
        blob = bucket.blob(filename)
        blob.upload_from_file(file)
        file_paths[key] = blob.public_url

    return jsonify({'uploaded_files': file_paths}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)

