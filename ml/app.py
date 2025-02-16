
from flask import Flask, request, jsonify
import pandas as pd
import os
import chardet

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def detect_encoding(file_path, sample_size=100_000):
    """Detects file encoding using a sample."""
    with open(file_path, "rb") as f:
        raw_data = f.read(sample_size)
    result = chardet.detect(raw_data)
    encoding = result["encoding"] if result["encoding"] else "utf-8"

    if encoding.lower() in ["ascii", "unknown", None]:
        encoding = "latin1"

    return encoding

@app.route('/clean_csv', methods=['POST'])
def clean_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        encoding = detect_encoding(file_path)
        df = pd.read_csv(file_path, encoding=encoding, dtype=str)

        # Remove rows with null values
        df_cleaned = df.dropna()

        # Convert to JSON format
        cleaned_data = df_cleaned.to_dict(orient="records")

        return jsonify({"cleaned_data": cleaned_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__': 
    app.run(debug=True, port=5000) 

