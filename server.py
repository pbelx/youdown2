from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
import yt_dlp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def convert_bytes_to_mb(bytes_size):
    return round(bytes_size / (1024 * 1024), 2)

@app.route('/get_formats', methods=['POST'])
def get_formats():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        ydl = yt_dlp.YoutubeDL()
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])

        format_list = []
        for f in formats:
            filesize_bytes = f.get('filesize')
            filesize_mb = convert_bytes_to_mb(filesize_bytes) if filesize_bytes else None

            format_entry = {
                'format_id': f['format_id'],
                'resolution': f.get('resolution'),
                'url': f['url'],
                'filesize': filesize_mb,
            }
            format_list.append(format_entry)

        return jsonify({'formats': format_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
