import os
import random
import json
from flask import Flask, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
MUSIC_FOLDER = './music/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def random_emotion():
    return random.choice(['positive', 'neutral', 'negative'])

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        language = request.form.get('language', 'english').lower()

        # สุ่มอารมณ์
        emotion = random_emotion()

        # หาไฟล์เพลงที่เหมาะสมกับอารมณ์และภาษา
        music_path = os.path.join(MUSIC_FOLDER, language, emotion, 'mp3')
        cover_path = os.path.join(MUSIC_FOLDER, language, emotion, 'png')
        description_path = os.path.join(MUSIC_FOLDER, language, emotion, 'description')

        if not os.path.exists(music_path) or not os.listdir(music_path):
            return jsonify({'error': 'No music available for this emotion'}), 500
        if not os.path.exists(cover_path):
            return jsonify({'error': 'No cover images available for this emotion'}), 500

        selected_song = random.choice(os.listdir(music_path))
        song_name = os.path.splitext(selected_song)[0]

        cover_image = f"{song_name}.png"
        cover_image_path = os.path.join(cover_path, cover_image)

        if not os.path.exists(cover_image_path):
            return jsonify({'error': f'Cover image for {song_name} not found'}), 500

        # หาไฟล์ JSON สำหรับรายละเอียดของเพลง
        description_file = f"{song_name}.json"
        description_file_path = os.path.join(description_path, description_file)

        if not os.path.exists(description_file_path):
            return jsonify({'error': 'Description file not found'}), 500

        with open(description_file_path, 'r') as f:
            song_details = json.load(f)

        # สร้าง URL สำหรับไฟล์เพลงและรูปภาพที่สามารถเข้าถึงได้
        song_url = url_for('get_file', folder='mp3', filename=selected_song, emotion=emotion, language=language, _external=True)
        cover_url = url_for('get_file', folder='png', filename=cover_image, emotion=emotion, language=language, _external=True)

        # ส่งข้อมูลรายละเอียดเพลงกลับไป
        return jsonify({
            'emotion': emotion,
            'song_url': song_url,
            'cover_url': cover_url,
            'description': song_details.get('description', ''),
            'links': {
                'youtube': song_details.get('youtube', ''),
                'spotify': song_details.get('spotify', '')
            }
        })

    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/file/<language>/<emotion>/<folder>/<filename>', methods=['GET'])
def get_file(language, emotion, folder, filename):
    folder_path = os.path.join(MUSIC_FOLDER, language, emotion, folder)
    file_path = os.path.join(folder_path, filename)

    if os.path.exists(file_path):
        if folder == 'mp3':
            return send_file(file_path, as_attachment=True, download_name=filename, mimetype='audio/mpeg')
        elif folder == 'png':
            return send_file(file_path, as_attachment=True, download_name=filename, mimetype='image/png')
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
